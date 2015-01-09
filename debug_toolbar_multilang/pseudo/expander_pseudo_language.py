from django.utils import six
from debug_toolbar_multilang.pseudo import STR_FORMAT_PATTERN, \
    STR_FORMAT_NAMED_PATTERN
from debug_toolbar_multilang.pseudo.pseudo_language import PseudoLanguage


class ExpanderPseudoLanguage(PseudoLanguage):
    """
    Pseudo Language for expanding the strings. This is useful
    for verifying that the message still fits on the screen.
    Remember that some words are much more longer in other
    languages than in English. For instance, German words
    that 30% more space in average.
    """

    def make_pseudo(self, message):
        # message without %s or {} in it.
        # {test} or %(test)s is allowed, though.
        safeMessage = list(message)

        # find every matching string
        for match in reversed(list(STR_FORMAT_PATTERN.finditer(message))):
            # Check if string uses the "named format".
            # If not, the string will be replaced and saved
            # into safeMessage
            if not STR_FORMAT_NAMED_PATTERN.match(match.group()):
                start, end = match.span()
                safeMessage[start:end] = "???"

        # create complete message by using the original, appending
        # a space and finally converting the safeMessage to a string
        # again.
        return "%s %s" % (message, "".join(safeMessage))

    def language(self):
        return "pse-expander"

    @property
    def name(self):
        return "Pseudo-Expander Language"
