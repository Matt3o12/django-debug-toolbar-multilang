import ddt
from django.utils import translation, six
from django.utils.translation import trans_real
from django.utils.translation.trans_real import CONTEXT_SEPARATOR
from debug_toolbar_multilang.pseudo.accent_pseudo_language import \
    AccentPseudoLanguage

from debug_toolbar_multilang.pseudo.upper_pseudo_language import \
    UpperPseudoLanguage

from tests.helpers import MagicMock, patch, FUNCTIONAL_TEST
from debug_toolbar_multilang.pseudo import PseudoLanguage, STR_FORMAT_PATTERN, \
    bSTR_FORMAT_PATTERN
from tests.helpers import DebugToolbarMultiLangTestCase


@ddt.ddt
class TestPseudoLanguage(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(TestPseudoLanguage, self).setUp()
        self.lang = PseudoLanguage()

    def _patchMakePseudo(self, value=False, *args, **kwargs):
        if value:
            kwargs.setdefault("new", lambda m: m)

        patcher = patch.object(self.lang, "make_pseudo", *args, **kwargs)
        self.addCleanup(lambda: patcher.stop())

        return patcher.start()

    @ddt.data("foo", "bar", "foobar")
    def testPatchMakePseudo_usingValue(self, value):
        self._patchMakePseudo(value=True)
        self.assertEqual(value, self.lang.make_pseudo(value))

    def testPatchMakePseudo_noValue(self):
        mock = self._patchMakePseudo()
        arg = MagicMock()

        self.assertEqual(mock.return_value, self.lang.make_pseudo(arg))
        mock.assert_called_once_with(arg)

    def testMakePseudo(self):
        with self.assertRaises(NotImplementedError):
            self.lang.make_pseudo(None)

    def testGetPseudo(self):
        makePseudoMock = self._patchMakePseudo()
        argMock = MagicMock()
        result = self.lang.get_pseudo(argMock)

        self.assertEqual(makePseudoMock.return_value, result)
        makePseudoMock.assert_called_once_with(argMock)

    def testGettext(self):
        self._patchMakePseudo(value=True)
        text = self.lang.gettext("Hello")
        self.assertEqual("Hello", text)

        # gettext always returns str type, even on python 2.
        self.assertIsInstance(text, str)

    def testLgettext(self):
        self._patchMakePseudo(value=True)
        text = self.lang.lgettext("Test")
        self.assertEqual("Test", text)

    def testNgettext_singular(self):
        self._patchMakePseudo(value=True)
        text = self.lang.ngettext("Test1", None, 1)
        self.assertEqual("Test1", text)

    @ddt.data(0, 2, 3)
    def testNgettext_plural(self, n):
        # I don't trust ddt.data using ints.
        self.assertIn(n, (0, 2, 3))

        self._patchMakePseudo(value=True)
        text = self.lang.ngettext(None, "Test2", n)
        self.assertEqual("Test2", text)

    def testLNgettext_singular(self):
        self._patchMakePseudo(value=True)
        text = self.lang.lngettext("Test1", None, 1)
        self.assertEqual("Test1", text)

    @ddt.data(0, 2, 3)
    def testLNgettext_plural(self, n):
        # I don't trust ddt.data using ints.
        self.assertIn(n, (0, 2, 3))

        self._patchMakePseudo(value=True)
        text = self.lang.lngettext(None, "Test2", n)
        self.assertEqual("Test2", text)

    def testContentSeparator(self):
        text = "foo%sbar" % CONTEXT_SEPARATOR
        makePatch = self._patchMakePseudo()
        result = self.lang.get_pseudo(text)

        makePatch.assert_called_once_with("bar")

    def testUgettext(self):
        self._patchMakePseudo(value=True)
        text = self.lang.ugettext("test")
        self.assertEqual(six.u("test"), text)

    def testUngettext_singular(self):
        self._patchMakePseudo(value=True)
        text = self.lang.ungettext("foo", "bar", 1)
        self.assertEqual(six.u("foo"), text)

    @ddt.data(0, 2, 3, 4)
    def testUngettext_plural(self, n):
        self._patchMakePseudo(value=True)
        text = self.lang.ungettext("foo", "bar", n)

        self.assertEqual(six.u("bar"), text)

    def testGetLanguage(self):
        with self.assertRaises(NotImplementedError):
            self.lang.language()

    def testToLanguage(self):
        with patch.object(self.lang, "language") as langMock:
            result = self.lang.to_language()

        self.assertEqual(langMock.return_value, result)
        langMock.assert_called_once_with()

@ddt.ddt
class TestPseudoLanguageFunctional(DebugToolbarMultiLangTestCase):
    TEST_TYPE = FUNCTIONAL_TEST

    def setUp(self):
        super(TestPseudoLanguageFunctional, self).setUp()
        self.lang = PseudoLanguage()

        # most simple implementation: just upper the message.
        self.lang.make_pseudo = lambda m: m.upper()

        self._patchLang()

    def _patchLang(self):
        patcher = patch.object(trans_real, "_active")
        self.addCleanup(lambda: patcher.stop())

        mock = patcher.start()
        mock.value = self.lang

    def testGettext(self):
        self.assertEqual("TEST", translation.gettext("Test"))

    def testUgettext(self):
        self.assertEqual(six.u("TEST"), translation.ugettext("Test"))

    def testUngettext_singular(self):
        text = translation.ungettext("Test1", "test2", 1)
        self.assertEqual(six.u("TEST1"), text)

    @ddt.data(0, 2, 3)
    def testUngettext_plular(self, value):
        text = translation.ungettext("Test1", "Test2", value)
        self.assertEqual(six.u("TEST2"), text)

    def testPgettext(self):
        text = translation.pgettext("Context", "Test123")
        self.assertEqual("TEST123", text)

    def testNgettext_singular(self):
        text = translation.ngettext("Test1", "Test2", 1)
        self.assertEqual("TEST1", text)

    @ddt.data(0, 2, 3)
    def testNgettext_plural(self, value):
        text = translation.ngettext("Test1", "Test2", value)
        self.assertEqual("TEST2", text)

@ddt.ddt
class TestStrRegex(DebugToolbarMultiLangTestCase):
    @ddt.file_data("strFormatPatterns.json")
    def testMatches(self, value):
        self.assertTrue(STR_FORMAT_PATTERN.match(value))
        self.assertTrue(bSTR_FORMAT_PATTERN.match(six.b(value)))

    @ddt.data("test", "test%s", "bar%(total)s")
    def testDoesNotMatch(self, value):
        self.assertFalse(STR_FORMAT_PATTERN.match(value))
        self.assertFalse(bSTR_FORMAT_PATTERN.match(six.b(value)))

@ddt.ddt
class TestUpperPseudoLanguage(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(TestUpperPseudoLanguage, self).setUp()
        self.lang = UpperPseudoLanguage()

    @ddt.file_data("makeUpperString.json")
    def testMakePseudo(self, values):
        message, expected = values

        self.assertEqual(expected, self.lang.make_pseudo(message))

    def testLanguage(self):
        self.assertEqual("pse", self.lang.language())


@ddt.ddt
class TestAccentPseudoLanguage(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(TestAccentPseudoLanguage, self).setUp()
        self.lang = AccentPseudoLanguage()

    def testLanguage(self):
        self.assertEqual("pse-accent", self.lang.language())

    @ddt.file_data("accentStrings.json")
    def testMakePseudo(self, values):
        message, accented = values
        self.assertEqual(accented, self.lang.make_pseudo(message))
