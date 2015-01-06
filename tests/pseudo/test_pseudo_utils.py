import ddt
import os
from django.utils import six
from debug_toolbar_multilang.pseudo import STR_FORMAT_PATTERN, \
    bSTR_FORMAT_PATTERN

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
