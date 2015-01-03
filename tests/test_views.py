from __future__ import absolute_import

from django.conf import settings
from tests.helpers import LANGUAGE_SESSION_KEY

try:
    from unittest import mock
    from unittest.mock import patch, MagicMock, call
except ImportError:
    import mock
    from mock import patch, MagicMock, call

from debug_toolbar_multilang import views
from tests.helpers import DebugToolbarMultiLangTestCase
from django.core.urlresolvers import reverse


class TestSetKey(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(TestSetKey, self).setUp()
        self.container = {}

    def testSettingNotFound(self):
        views._set_key(self.container, "foo", "bar")
        self.assertNotIn("foo", self.container)
        self.assertNotIn("bar", self.container)

    def testSettingsExists(self):
        with self.settings(SECRET_KEY="foobar"):
            views._set_key(self.container, "secret", "SECRET_KEY")

        self.assertIn("secret", self.container)
        self.assertEqual("foobar", self.container["secret"])


class TestChangeLanguageView(DebugToolbarMultiLangTestCase):
    @property
    def request(self):
        return self.factory.get(reverse("djdt:multilang_change"))

    def testRedirect(self):
        with patch.object(views, "get_next_url", new=lambda r: "/foo/bar/"):
            response = views.change_language(self.request)

        self.assertEqual(302, response.status_code)
        self.assertEqual("/foo/bar/", response["LOCATION"])

    def testGetNextURLNoRefererHeader(self):
        url = views.get_next_url(self.request)
        self.assertEqual("/", url)

    def testGetNextURLUnsafeRefererHeader(self):
        request = self.request
        request.META["HTTP_REFERER"] = "http://google.com/"
        url = views.get_next_url(self.request)
        self.assertEqual("/", url)

    def testGetNextURL(self):
        request = self.request
        referer = self.get_host_url(request) + "refer_url/test/"
        request.META["HTTP_REFERER"] = referer
        self.assertEqual(referer, views.get_next_url(request))

    def testChangeLanguage(self):
        request = self.factory.get("/test/", {"language": "de"})
        request.session = MagicMock()

        views.change_language(request)

        key = LANGUAGE_SESSION_KEY
        request.session.__setitem__.assert_called_once_with(key, "de")

    def testChangeLanguageCookies(self):
        request = self.factory.get("/test/", {"language": "de"})
        response = views.change_language(request)
        self.assertIn(settings.LANGUAGE_COOKIE_NAME, response.cookies)

        cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]
        self.assertEqual("de", cookie.value)

    def testChangeLanguageNoCode(self):
        request = self.request
        request.session = MagicMock()

        views.change_language(request)
        response = views.change_language(request)
        self.assertNotIn(settings.LANGUAGE_COOKIE_NAME, response.cookies)
        self.assertFalse(request.session.__setitem__.called)

    def testAssertInvalidLanguage(self):
        request = self.request
        request.session = MagicMock()

        views.change_language(request)
        response = views.change_language(request)
        self.assertNotIn(settings.LANGUAGE_COOKIE_NAME, response.cookies)
        self.assertFalse(request.session.__setitem__.called)

