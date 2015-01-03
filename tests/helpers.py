from __future__ import absolute_import

from django.test.client import RequestFactory
from django.test.testcases import TestCase

try:
    from django.utils.translation import LANGUAGE_SESSION_KEY
except ImportError:  # backwards compatible with django 1.6
    LANGUAGE_SESSION_KEY = "django_language"

class DebugToolbarMultiLangTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def get_host_url(self, request):
        """
        Returns the host url (and ignores ports!).

        :param request: HttpRequest
        :return: str
        """

        # Django 1.6 does not support schemes properly.
        # The RequestFactory does not know anything about
        # schemes, as well.

        # values = {
        #     "schema": "https" if request.is_secure() else "http", or
        #     "schema": request.get_scheme
        #     "host": request.get_host()
        # }
        # return "%(schema)s://%(host)s/" % values

        return "http://%s/" % request.get_host()