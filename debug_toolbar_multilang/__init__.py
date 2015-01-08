from django.conf import settings
from debug_toolbar_multilang.pseudo.brackets_pseudo_language import \
    BracketsPseudoLanguage

from debug_toolbar_multilang.pseudo.utils import enable_pseudo_localization, \
    register_pseudo_language
from debug_toolbar_multilang.pseudo.accent_pseudo_language import \
    AccentPseudoLanguage
from debug_toolbar_multilang.pseudo.upper_pseudo_language import \
    UpperPseudoLanguage


if getattr(settings, "ENABLE_PSEUDO_LOCALIZATION", False):  # pragma: no cover
    enable_pseudo_localization()
    langs = [
        AccentPseudoLanguage(),
        UpperPseudoLanguage(),
        BracketsPseudoLanguage(),
    ]

    for theLang in langs:
        register_pseudo_language(theLang)

__all__ = ["enable_pseudo_localization", "register_pseudo_language"]