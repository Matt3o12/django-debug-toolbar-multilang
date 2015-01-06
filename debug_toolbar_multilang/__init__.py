from django.conf import settings

from debug_toolbar_multilang.pseudo.utils import enable_pseudo_localization, \
    register_pseudo_language
from debug_toolbar_multilang.pseudo.accent_pseudo_language import \
    AccentPseudoLanguage
from debug_toolbar_multilang.pseudo.upper_pseudo_language import \
    UpperPseudoLanguage


if getattr(settings, "ENABLE_PSEUDO_LOCALIZATION", False):  # pragma: no cover
    enable_pseudo_localization()
    register_pseudo_language(AccentPseudoLanguage())
    register_pseudo_language(UpperPseudoLanguage())

__all__ = ["enable_pseudo_localization", "register_pseudo_language"]