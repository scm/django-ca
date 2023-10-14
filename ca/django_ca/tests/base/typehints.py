# This file is part of django-ca (https://github.com/mathiasertl/django-ca).
#
# django-ca is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# django-ca is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with django-ca. If not, see
# <http://www.gnu.org/licenses/>.

"""Shared typehints for tests."""

import typing
from typing import Any, Dict

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric.types import CertificateIssuerPrivateKeyTypes

from django_ca.models import DjangoCAModel

if typing.TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser as User
    from django.test.client import _MonkeyPatchedWSGIResponse as HttpResponse
else:
    from django.contrib.auth import get_user_model
    from django.http import HttpResponse

    User = get_user_model()

DjangoCAModelTypeVar = typing.TypeVar("DjangoCAModelTypeVar", bound=DjangoCAModel)


CertFixtureData = Dict[str, Any]


class _OcspFixtureData(typing.TypedDict):
    name: str
    filename: str


class OcspFixtureData(_OcspFixtureData, total=False):
    """Fixture data for OCSP requests.

    Keys:

    * name (str): name of the fixture
    * filename (str): name of the file of the stored request
    * nonce (str, optional): Nonce used in the request
    """

    nonce: str


class FixtureData(typing.TypedDict):
    """Fixture data loaded/stored from JSON."""

    certs: Dict[str, CertFixtureData]


KeyDict = typing.TypedDict("KeyDict", {"pem": str, "parsed": CertificateIssuerPrivateKeyTypes, "der": bytes})
PubDict = typing.TypedDict("PubDict", {"pem": str, "parsed": x509.Certificate, "der": bytes})
CsrDict = typing.TypedDict("CsrDict", {"pem": str, "parsed": x509.CertificateSigningRequest})


__all__ = ["HttpResponse", "User"]
