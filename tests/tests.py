import inspect
from time import sleep
import types
from unittest.case import skip
from debug_toolbar.toolbar import DebugToolbar
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.cookie import SimpleCookie
from django.http.request import HttpRequest
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.testcases import LiveServerTestCase
from django.utils.translation import LANGUAGE_SESSION_KEY
from debug_toolbar_multilang import views
from debug_toolbar_multilang.panels.multilang import MultiLangPanel

try:
    from unittest import mock
    from unittest.mock import patch, MagicMock, call
except ImportError:
    import mock
    from mock import patch, MagicMock, call


class DebugToolbarMultiLangTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def get_host_url(self, request):
        """
        Returns the host url (and ignores ports!).

        :param request: HttpRequest
        :return: str
        """
        values = {
            "schema": request.scheme,
            "host": request.get_host()
        }
        return "%(schema)s://%(host)s/" % values


class TestDebugToolbarMultiLangTestCase(DebugToolbarMultiLangTestCase):
    def testGetHostURLHTTPs(self):
        request = self.factory.get("/test/", secure=True, SERVER_NAME="test")
        self.assertEqual("https://test/", self.get_host_url(request))

    def testGetHostURLHTTP(self):
        request = self.factory.get("/test/", secure=False, SERVER_NAME="test")
        self.assertEqual("http://test/", self.get_host_url(request))

    def testGetHostURLDefault(self):
        request = self.factory.get("/test/")
        self.assertEqual("http://testserver/", self.get_host_url(request))

    def testGetHostURLCustomName(self):
        request = self.factory.get("test", SERVER_NAME="serverName.tld")
        self.assertEqual("http://serverName.tld/", self.get_host_url(request))


class TestMultiLangPanel(DebugToolbarMultiLangTestCase):
    _transPatch = "debug_toolbar_multilang.panels.multilang.translation"

    def setUp(self):
        super(TestMultiLangPanel, self).setUp()

        self.toolbarMock = MagicMock(DebugToolbar)
        self.panel = MultiLangPanel(self.toolbarMock)

    def testNavTitle(self):
        self.assertEqual("Languages", self.panel.nav_title())

    def testNavSubtitle(self):
        newLang = {"name_local": "foo"}
        with patch.object(MultiLangPanel, "current_lang", new=newLang):
            with self.settings(LANGUAGES=[None, None, None]):
                subTitle = self.panel.nav_subtitle()

        self.assertEqual("Current: foo; total: 3", subTitle)

    def testGetCurrentLang(self):
        with patch(self._transPatch) as transMock:
            currentLang = self.panel.current_lang

        transMock.get_language.assert_called_with()
        getLangValue = transMock.get_language.return_value
        langInfo = transMock.get_language_info
        langInfo.assert_called_with(getLangValue)
        self.assertIs(langInfo.return_value, currentLang)

    def testHasContent(self):
        self.assertTrue(self.panel.has_content)

    def testTemplate(self):
        t = "debug_toolbar_multilang/multilang.html"
        self.assertEqual(t, self.panel.template)

    def testGetStats_noMonkeyPatching(self):
        # just assert that the dependencies are called correctly.
        tb = self.toolbarMock
        tb.stats = MagicMock()
        stats = self.panel.get_stats()
        tb.stats.get().copy.assert_called_with()
        self.assertIs(stats, tb.stats.get().copy.return_value)
        stats.__setitem__.assert_called_with("current_lang", mock.ANY)
        
    def testGetStats(self):
        # assert that it actually returns the expected values.
        self.toolbarMock.stats = MagicMock()
        self.toolbarMock.stats.get.return_value = {}
        with patch.object(self.panel, "get_available_languages") as mock:
            stats = self.panel.get_stats()

        self.assertEqual(mock.return_value, stats["languages"])
        mock.assert_called_once_with()

    def testGetAvailableLanguages(self):
        langs = list(map(lambda l: (l,), ["English", "Russian", "German"]))
        with patch(self._transPatch) as transMock:
            with self.settings(LANGUAGES=langs):
                result = self.panel.get_available_languages()
                resultList = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        exp = [transMock.get_language_info.return_value for t in range(3)]
        self.assertEqual(exp, resultList)
        calls = [call(*l) for l in langs]
        self.assertEqual(3, len(calls))
        transMock.get_language_info.assert_has_calls(calls, any_order=True)


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
