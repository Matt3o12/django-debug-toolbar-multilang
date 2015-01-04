import ddt

from tests.helpers import MagicMock
from debug_toolbar_multilang.pseudo.utils import patch_check_function
from tests.helpers import DebugToolbarMultiLangTestCase


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
