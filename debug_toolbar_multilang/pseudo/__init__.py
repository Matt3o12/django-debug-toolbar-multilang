import re

from debug_toolbar_multilang.pseudo.pseudo_language import PseudoLanguage
from debug_toolbar_multilang.pseudo.upper_pseudo_language import \
    UpperPseudoLanguage
from debug_toolbar_multilang.pseudo.utils import enable_pseudo_localization

_regexString = r"(?:\%(?:\([^\(\)]+\))?[0-9]*\.?[0-9]*[a-z]+)|(?:\{[^\{\}]*\})"
STR_FORMAT_PATTERN = re.compile(_regexString.encode())


__all__ = [
    "PseudoLanguage",
    "UpperPseudoLanguage",
    "enable_pseudo_localization",
    "STR_FORMAT_PATTERN"
]
