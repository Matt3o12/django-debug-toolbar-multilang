import re

from django.utils import six

from debug_toolbar_multilang.pseudo.pseudo_language import PseudoLanguage
from debug_toolbar_multilang.pseudo.upper_pseudo_language import \
    UpperPseudoLanguage
from debug_toolbar_multilang.pseudo.accent_pseudo_language import \
    AccentPseudoLanguage
from debug_toolbar_multilang.pseudo.utils import enable_pseudo_localization


_regexString = r"(?:\%(?:\([^\(\)]+\))?[0-9]*\.?[0-9]*[a-z]+)|(?:\{[^\{\}]*\})"
STR_FORMAT_PATTERN = re.compile(six.u(_regexString))
bSTR_FORMAT_PATTERN = re.compile(six.b(_regexString))

_regexStringSimple = "(?:\{\w+[^\}]*\})|(?:\%\([^\)]+\)\w)"
STR_FORMAT_NAMED_PATTERN = re.compile(six.u(_regexStringSimple))
"""
Only matches string format patterns that are named
e.g. matches %(test)s or {test} but not %s or {}
"""

bSTR_FORMAT_NAMED_PATTERN = re.compile(six.b(_regexStringSimple))
"""
Binary version of STR_FORMAT_NAMED_PATTERN
"""

__all__ = [
    "PseudoLanguage",
    "UpperPseudoLanguage",
    "enable_pseudo_localization",
    "STR_FORMAT_PATTERN",
    "AccentPseudoLanguage"
]
