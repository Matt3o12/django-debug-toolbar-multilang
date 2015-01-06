import os

import ddt
from django.utils import six

from debug_toolbar_multilang.pseudo import utils
from debug_toolbar_multilang.pseudo import STR_FORMAT_PATTERN, \
    bSTR_FORMAT_PATTERN
from debug_toolbar_multilang.pseudo.pseudo_language import PseudoLanguage

from tests.helpers import MagicMock
from debug_toolbar_multilang.pseudo.utils import patch_check_function
from tests.helpers import DebugToolbarMultiLangTestCase, patch


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
    @ddt.file_data(os.path.join("..", "resources", "strFormatPatterns.json"))
    def testMatches(self, value):
        self.assertTrue(STR_FORMAT_PATTERN.match(value))
        self.assertTrue(bSTR_FORMAT_PATTERN.match(six.b(value)))

    @ddt.data("test", "test%s", "bar%(total)s")
    def testDoesNotMatch(self, value):
        self.assertFalse(STR_FORMAT_PATTERN.match(value))
        self.assertFalse(bSTR_FORMAT_PATTERN.match(six.b(value)))
