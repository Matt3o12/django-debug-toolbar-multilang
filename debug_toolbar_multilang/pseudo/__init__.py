import re
from django.utils import six

from debug_toolbar_multilang.pseudo.pseudo_language import PseudoLanguage
from debug_toolbar_multilang.pseudo.upper_pseudo_language import \
    UpperPseudoLanguage
from debug_toolbar_multilang.pseudo.accent_pseudo_language import \
    AccentPseudoLanguage
from debug_toolbar_multilang.pseudo.utils import enable_pseudo_localization

_regexString = r"(?:\%(?:\([^\(\)]+\))?[0-9]*\.?[0-9]*[a-z]+)|(?:\{[^\{\}]*\})"
bSTR_FORMAT_PATTERN = re.compile(six.b(_regexString))
STR_FORMAT_PATTERN = re.compile(six.u(_regexString))


__all__ = [
    "PseudoLanguage",
    "UpperPseudoLanguage",
    "enable_pseudo_localization",
    "STR_FORMAT_PATTERN",
    "AccentPseudoLanguage"
]
