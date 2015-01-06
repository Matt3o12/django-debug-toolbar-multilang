import os

import ddt

from debug_toolbar_multilang.pseudo.accent_pseudo_language import \
    AccentPseudoLanguage
from tests.helpers import DebugToolbarMultiLangTestCase


@ddt.ddt
class TestAccentPseudoLanguage(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(TestAccentPseudoLanguage, self).setUp()
        self.lang = AccentPseudoLanguage()

    def testLanguage(self):
        self.assertEqual("pse-accent", self.lang.language())

    @ddt.file_data(os.path.join("..", "resources", "accentStrings.json"))
    def testMakePseudo(self, values):
        message, accented = values
        self.assertEqual(accented, self.lang.make_pseudo(message))

    def testName(self):
        self.assertEqual("Accented-Pseudo Language", self.lang.name)
