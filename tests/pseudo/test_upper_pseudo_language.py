import os

import ddt

from debug_toolbar_multilang.pseudo.upper_pseudo_language import \
    UpperPseudoLanguage
from tests.helpers import DebugToolbarMultiLangTestCase


@ddt.ddt
class TestUpperPseudoLanguage(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(TestUpperPseudoLanguage, self).setUp()
        self.lang = UpperPseudoLanguage()

    @ddt.file_data(os.path.join("..", "resources", "makeUpperString.json"))
    def testMakePseudo(self, values):
        message, expected = values

        self.assertEqual(expected, self.lang.make_pseudo(message))

    def testLanguage(self):
        self.assertEqual("pse", self.lang.language())
