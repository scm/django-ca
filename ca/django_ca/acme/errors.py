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

from .responses import AcmeResponseBadCSR
from .responses import AcmeResponseError
from .responses import AcmeResponseMalformed
from .responses import AcmeResponseUnauthorized


class AcmeException(Exception):
    response = AcmeResponseError

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.kwargs = kwargs

    def get_response(self):
        return self.response(*self.args, **self.kwargs)


class AcmeMalformed(AcmeException):
    response = AcmeResponseMalformed


class AcmeUnauthorized(AcmeException):
    response = AcmeResponseUnauthorized


class AcmeBadCSR(AcmeException):
    """Exception raised when a CSR is not acceptable."""

    response = AcmeResponseBadCSR
