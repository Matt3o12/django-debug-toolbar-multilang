from __future__ import absolute_import
import types
from debug_toolbar.toolbar import DebugToolbar

try:
    from unittest import mock
    from unittest.mock import patch, MagicMock, call
except ImportError:
    import mock
    from mock import patch, MagicMock, call


from debug_toolbar_multilang.panels.multilang import MultiLangPanel
from tests.helpers import DebugToolbarMultiLangTestCase


class TestMultiLangPanel(DebugToolbarMultiLangTestCase):
    _transPatch = "debug_toolbar_multilang.panels.multilang.translation"

    def setUp(self):
        super(TestMultiLangPanel, self).setUp()

        self.toolbarMock = MagicMock(DebugToolbar)
        self.panel = MultiLangPanel(self.toolbarMock)

    def testNavTitle(self):
        self.assertEqual("Languages", self.panel.nav_title())

    def testNavtitle(self):
        self.assertEqual("Languages", self.panel.title)

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
