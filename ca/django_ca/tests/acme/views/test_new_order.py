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

"""Test creating a new order."""

from datetime import timedelta, timezone as tz
from http import HTTPStatus
from typing import Any

import acme
import acme.jws
import pyrfc3339

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse_lazy
from django.utils import timezone

from freezegun import freeze_time

from django_ca import ca_settings
from django_ca.acme.messages import NewOrder
from django_ca.models import AcmeAuthorization, AcmeOrder
from django_ca.tests.acme.views.base import AcmeWithAccountViewTestCaseMixin
from django_ca.tests.base.constants import CERT_DATA, TIMESTAMPS
from django_ca.tests.base.utils import override_tmpcadir


@freeze_time(TIMESTAMPS["everything_valid"])
class AcmeNewOrderViewTestCase(AcmeWithAccountViewTestCaseMixin[NewOrder], TestCase):
    """Test creating a new order."""

    url = reverse_lazy("django_ca:acme-new-order", kwargs={"serial": CERT_DATA["root"]["serial"]})
    message_cls = NewOrder

    def get_message(self, **kwargs: Any) -> NewOrder:
        """Return a  message that can be sent to the server successfully."""
        kwargs.setdefault("identifiers", [{"type": "dns", "value": self.SERVER_NAME}])
        return super().get_message(**kwargs)  # type: ignore[return-value] # base has union

    @override_tmpcadir()
    def test_basic(self, accept_naive: bool = False) -> None:
        """Basic test for creating an account via ACME."""
        with self.mock_slug() as slug:
            resp = self.acme(self.url, self.message, kid=self.kid)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED, resp.content)

        expires = timezone.now() + ca_settings.ACME_ORDER_VALIDITY
        self.assertEqual(
            resp.json(),
            {
                "authorizations": [
                    self.absolute_uri(":acme-authz", serial=self.ca.serial, slug=slug),
                ],
                "expires": pyrfc3339.generate(expires, accept_naive=accept_naive),
                "finalize": self.absolute_uri(":acme-order-finalize", serial=self.ca.serial, slug=slug),
                "identifiers": [{"type": "dns", "value": self.SERVER_NAME}],
                "status": "pending",
            },
        )

        order = AcmeOrder.objects.get(account=self.account)
        self.assertEqual(order.account, self.account)
        self.assertEqual(order.slug, slug)
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.expires, expires)
        self.assertIsNone(order.not_before)
        self.assertIsNone(order.not_after)

        # Test the autogenerated AcmeAuthorization object
        authz = order.authorizations.all()
        self.assertEqual(len(authz), 1)
        self.assertEqual(authz[0].order, order)
        self.assertEqual(authz[0].type, "dns")
        self.assertEqual(authz[0].value, self.SERVER_NAME)
        self.assertEqual(authz[0].status, AcmeAuthorization.STATUS_PENDING)
        self.assertFalse(authz[0].wildcard)

    @override_settings(USE_TZ=False)
    def test_basic_without_timezone_support(self) -> None:
        """Basic test with timezone support enabled."""
        self.test_basic(accept_naive=True)

    @override_tmpcadir()
    def test_not_before_not_after(self, accept_naive: bool = False) -> None:
        """Test the notBefore/notAfter properties."""
        not_before = timezone.now() + timedelta(seconds=10)
        not_after = timezone.now() + timedelta(days=3)

        if timezone.is_naive(not_before):
            not_before = timezone.make_aware(not_before, timezone=tz.utc)
        if timezone.is_naive(not_after):
            not_after = timezone.make_aware(not_after, timezone=tz.utc)

        msg = self.get_message(not_before=not_before, not_after=not_after)

        with self.mock_slug() as slug:
            resp = self.acme(self.url, msg, kid=self.kid)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED, resp.content)

        expires = timezone.now() + ca_settings.ACME_ORDER_VALIDITY
        self.assertEqual(
            resp.json(),
            {
                "authorizations": [
                    self.absolute_uri(":acme-authz", serial=self.ca.serial, slug=slug),
                ],
                "expires": pyrfc3339.generate(expires, accept_naive=accept_naive),
                "finalize": self.absolute_uri(":acme-order-finalize", serial=self.ca.serial, slug=slug),
                "identifiers": [{"type": "dns", "value": self.SERVER_NAME}],
                "status": "pending",
                "notBefore": pyrfc3339.generate(not_before, accept_naive=accept_naive),
                "notAfter": pyrfc3339.generate(not_after, accept_naive=accept_naive),
            },
        )

        order = AcmeOrder.objects.get(account=self.account)
        self.assertEqual(order.account, self.account)
        self.assertEqual(order.slug, slug)
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.expires, expires)

        if settings.USE_TZ:
            self.assertEqual(order.not_before, not_before)
            self.assertEqual(order.not_after, not_after)
        else:
            self.assertEqual(order.not_before, timezone.make_naive(not_before))
            self.assertEqual(order.not_after, timezone.make_naive(not_after))

        # Test the autogenerated AcmeAuthorization object
        authz = order.authorizations.all()
        self.assertEqual(len(authz), 1)
        self.assertEqual(authz[0].order, order)
        self.assertEqual(authz[0].type, "dns")
        self.assertEqual(authz[0].value, self.SERVER_NAME)
        self.assertEqual(authz[0].status, AcmeAuthorization.STATUS_PENDING)
        self.assertFalse(authz[0].wildcard)

    @override_settings(USE_TZ=False)
    def test_not_before_not_after_with_tz(self) -> None:
        """Test the notBefore/notAfter properties, but with timezone support."""
        self.test_not_before_not_after(accept_naive=True)

    @override_tmpcadir()
    def test_no_identifiers(self) -> None:
        """Test sending no identifiers."""
        resp = self.acme(self.url, acme.messages.NewOrder(), kid=self.kid)
        self.assertMalformed(resp, "The following fields are required: identifiers")

        # try empty tuple too
        resp = self.acme(
            self.url,
            acme.messages.NewOrder(identifiers=tuple()),
            kid=self.kid,
            payload_cb=lambda d: dict(d, identifiers=()),
        )
        self.assertMalformed(resp, "The following fields are required: identifiers")

        self.assertEqual(AcmeOrder.objects.all().count(), 0)

    @override_tmpcadir()
    def test_invalid_not_before_after(self) -> None:
        """Test invalid not_before/not_after dates."""
        past = timezone.now() - timedelta(days=1)
        resp = self.acme(self.url, self.get_message(not_before=past), kid=self.kid)
        self.assertMalformed(resp, "Certificate cannot be valid before now.")

        far_future = timezone.now() + timedelta(days=3650)
        resp = self.acme(self.url, self.get_message(not_after=far_future), kid=self.kid)
        self.assertMalformed(resp, "Certificate cannot be valid that long.")

        not_before = timezone.now() + timedelta(days=10)
        not_after = timezone.now() + timedelta(days=1)

        resp = self.acme(self.url, self.get_message(not_before=not_before, not_after=not_after), kid=self.kid)
        self.assertMalformed(resp, "notBefore must be before notAfter.")
