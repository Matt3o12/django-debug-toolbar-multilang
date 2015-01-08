from django.utils import six
from debug_toolbar_multilang.pseudo.pseudo_language import PseudoLanguage


class BracketsPseudoLanguage(PseudoLanguage):
    """
    Wraps the message in [brackets]. This is useful
    for showing where messages were contradicted.
    Translators often need to reorder phrases.
    """

    def make_pseudo(self, message):
        return six.u("[%s]" % message)

    def language(self):
        return "pse-brackets"

    @property
    def name(self):
        return "Pseudo-Brackets Language"
