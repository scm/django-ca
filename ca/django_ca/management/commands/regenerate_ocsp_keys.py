# This file is part of django-ca (https://github.com/mathiasertl/django-ca).
#
# django-ca is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# django-ca is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with django-ca.  If not,
# see <http://www.gnu.org/licenses/>.

"""Management command to regenerate keys used for OCSP signing.

.. seealso:: https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
"""

from datetime import timedelta
from typing import Any, Iterable, Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from django.core.management.base import CommandError, CommandParser

from django_ca import ca_settings
from django_ca.management.actions import ExpiresAction
from django_ca.management.base import BaseCommand
from django_ca.models import CertificateAuthority
from django_ca.tasks import generate_ocsp_key, run_task
from django_ca.typehints import ParsableKeyType
from django_ca.utils import add_colons, validate_private_key_parameters


class Command(BaseCommand):  # pylint: disable=missing-class-docstring
    help = "Regenerate OCSP keys."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "serials",
            metavar="serial",
            nargs="*",
            help="Generate OCSP keys only for the given CA. If omitted, generate keys for all CAs.",
        )

        parser.add_argument(
            "--expires",
            default=timedelta(days=2),
            action=ExpiresAction,
            help="Sign the certificate for DAYS days (default: %(default)s)",
        )
        parser.add_argument("--quiet", action="store_true", default=False, help="Do not output warnings.")

        self.add_algorithm(parser)
        self.add_key_size(parser)
        self.add_key_type(parser, default=None)
        self.add_ecc_curve(parser)
        self.add_password(parser)

        self.add_profile(
            parser, 'Override the profile used for generating the certificate. By default, "ocsp" is used.'
        )

    def handle(
        self,
        serials: Iterable[str],
        profile: Optional[str],
        expires: timedelta,
        algorithm: Optional[hashes.HashAlgorithm],
        ecc_curve: Optional[ec.EllipticCurve],
        key_size: int,
        key_type: Optional[ParsableKeyType],
        password: Optional[bytes],
        quiet: bool,
        **options: Any,
    ) -> None:
        profile = profile or "ocsp"

        # Check if the profile exists. Note that this shouldn't really happen, since valid parameters match
        # existing profiles. The only case is when the user undefines the "ocsp" profile, which is the
        # default.
        if profile not in ca_settings.CA_PROFILES:
            raise CommandError(f"{profile}: Undefined profile.")

        if not serials:
            serials = CertificateAuthority.objects.all().order_by("serial").values_list("serial", flat=True)

        ecc_curve_name: Optional[str] = None
        if ecc_curve is not None:
            ecc_curve_name = ecc_curve.name.lower()

        for serial in serials:
            serial = serial.replace(":", "").strip().upper()
            hr_serial = add_colons(serial)
            try:
                ca = CertificateAuthority.objects.get(serial=serial)
            except CertificateAuthority.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"{hr_serial}: Unknown CA."))
                continue

            if not ca.key_exists:
                if quiet is False:  # pragma: no branch
                    # NOTE: coverage falsely identifies the above condition to always be false.
                    self.stderr.write(self.style.WARNING(f"{hr_serial}: CA has no private key."))

                continue

            if key_type is None:
                ca_key_type = ca.key_type
            else:
                ca_key_type = key_type

            ca_key_size, ca_ecc_curve = validate_private_key_parameters(ca_key_type, key_size, ecc_curve)

            algorithm_name: Optional[str] = None
            if algorithm is not None:
                algorithm_name = algorithm.name

            run_task(
                generate_ocsp_key,
                ca.serial,
                profile=profile,
                expires=expires.total_seconds(),
                algorithm=algorithm_name,
                key_size=ca_key_size,
                key_type=ca_key_type,
                elliptic_curve=ecc_curve_name,
                password=password,
            )
