import ddt
from django.utils import six
import os
from debug_toolbar_multilang.pseudo.brackets_pseudo_language import \
    BracketsPseudoLanguage
from debug_toolbar_multilang.pseudo.expander_pseudo_language import \
    ExpanderPseudoLanguage
from tests.helpers import DebugToolbarMultiLangTestCase
from tests.pseudo import RESOURCE_PATCH


@ddt.ddt
class TestExpanderPseudoLanguage(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(DebugToolbarMultiLangTestCase, self).setUp()

        self.lang = ExpanderPseudoLanguage()

    @ddt.file_data(os.path.join(RESOURCE_PATCH, "expanderTestStrings.json"))
    def testMakePseudo(self, values):
        got, expected = values
        self.assertEqual(expected, self.lang.make_pseudo(got))

    def testLanguage(self):
        self.assertEqual("pse-expander", self.lang.language())

    def testName(self):
        self.assertEqual("Pseudo-Expander Language", self.lang.name)
