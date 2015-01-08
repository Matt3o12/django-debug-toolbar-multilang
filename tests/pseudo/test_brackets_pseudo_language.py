from django.utils import six
from debug_toolbar_multilang.pseudo.brackets_pseudo_language import \
    BracketsPseudoLanguage
from tests.helpers import DebugToolbarMultiLangTestCase


class TestBracketsPseudoLanguage(DebugToolbarMultiLangTestCase):
    def setUp(self):
        super(DebugToolbarMultiLangTestCase, self).setUp()

        self.lang = BracketsPseudoLanguage()

    def testMakePseudo(self):
        msg = self.lang.make_pseudo("foo %s bar") % "hello"
        self.assertEqual("[foo hello bar]", msg)

    def testLanguage(self):
        self.assertEqual("pse-brackets", self.lang.language())

    def testName(self):
        self.assertEqual("Pseudo-Brackets Language", self.lang.name)
