import ddt
from django.utils import six
from os.path import join

from debug_toolbar_multilang.pseudo import utils, STR_FORMAT_NAMED_PATTERN, \
    bSTR_FORMAT_NAMED_PATTERN
from debug_toolbar_multilang.pseudo import STR_FORMAT_PATTERN, \
    bSTR_FORMAT_PATTERN
from debug_toolbar_multilang.pseudo.pseudo_language import PseudoLanguage

from tests.helpers import MagicMock
from debug_toolbar_multilang.pseudo.utils import patch_check_function
from tests.helpers import DebugToolbarMultiLangTestCase, patch
from tests.pseudo import RESOURCE_PATCH


@ddt.ddt
class TestPatchCheckFunction(DebugToolbarMultiLangTestCase):
    @ddt.data("en", "en-gb", "de")
    def testOriginal(self, lang):
        arg = MagicMock()
        checkPatch = patch_check_function(arg)
        self.assertEqual(checkPatch(lang), arg.return_value)
        arg.assert_called_once_with(lang)

    @ddt.data("pse", "pse-bidi", "pse-acc")
    def testPseudoLanguage(self, lang):
        arg = MagicMock()
        checkPatch = patch_check_function(arg)

        # When using pseudo languages, checkPatch will
        # always return True
        self.assertTrue(checkPatch(lang))


class TestRegisterPseudoLanguageFunction(DebugToolbarMultiLangTestCase):
    def testRegister(self):
        lang = MagicMock(PseudoLanguage)
        lang.code = "pse-mock"
        lang.get_info_dict.return_value = {
            'bidi': False,
            'code': "pse-mock",
            'name': "Pseudo Language (Mocked)",
            'name_local': "Pseudo Language (Mocked)"
        }

        langInfo = utils.LANG_INFO
        langDict = utils._languages
        with patch.dict(utils._languages, clear=True), \
             patch.dict(utils.LANG_INFO, clear=True):
            utils.register_pseudo_language(lang)

            self.assertEqual(lang, langDict["pse-mock"])
            self.assertEqual(lang.get_info_dict(), langInfo["pse-mock"])

# There is no better place for this test.
@ddt.ddt
class TestStrRegex(DebugToolbarMultiLangTestCase):
    @ddt.file_data(join(RESOURCE_PATCH, "strFormatPatterns.json"))
    def testMatches(self, value):
        self.assertTrue(STR_FORMAT_PATTERN.match(value))
        self.assertTrue(bSTR_FORMAT_PATTERN.match(six.b(value)))

    @ddt.data("test", "test%s", "bar%(total)s")
    def testDoesNotMatch(self, value):
        self.assertFalse(STR_FORMAT_PATTERN.match(value))
        self.assertFalse(bSTR_FORMAT_PATTERN.match(six.b(value)))


@ddt.ddt
class TestSimpleStringRegex(DebugToolbarMultiLangTestCase):
    def __formatMsg(self, msg, value):
        return msg.format(
            value=value,
            regex=STR_FORMAT_NAMED_PATTERN,
        )

    @ddt.file_data(join(RESOURCE_PATCH, "simpleStringPatternMatches.json"))
    def testMatches(self, value):
        msg = self.__formatMsg("{value} does not match {regex}", value)
        self.assertTrue(STR_FORMAT_NAMED_PATTERN.match(value), msg)
        self.assertTrue(bSTR_FORMAT_NAMED_PATTERN.match(six.b(value)), msg)

    @ddt.file_data(join(RESOURCE_PATCH, "simpleStringPatternNoMatches.json"))
    def testDoesNotMatch(self, value):
        msg = self.__formatMsg("{value} does match {regex}", value)
        self.assertFalse(STR_FORMAT_NAMED_PATTERN.match(value), msg)
        self.assertFalse(bSTR_FORMAT_NAMED_PATTERN.match(six.b(value)), msg)

