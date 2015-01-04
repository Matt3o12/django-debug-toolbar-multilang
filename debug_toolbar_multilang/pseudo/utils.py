from django.utils import translation as dj_translation, lru_cache
from django.utils.translation import trans_real

from debug_toolbar_multilang.pseudo import UpperPseudoLanguage


def patch_check_function(org):
    """
    Patches the check_for_language function so that it always returns
    true for pseudo localizations.

    :param org: the original function.
    :return: the patched function.
    """

    @lru_cache.lru_cache(maxsize=1000)
    def check_for_language(lang):
        if lang.startswith("pse"):
            return True

        return org(lang)

    return check_for_language


# Unit testing this method is hard because it messes with
# the global namespace and thus it might influence the
# results of other tests.
def enable_pseudo_localization():  # pragma: no cover
    """
    Patches django translation functions so that they accept pseudo
    localizations and generates pseudo (human) languages accordingly.

    :return: None
    """

    dj_check_bck = dj_translation.check_for_language
    dj_translation.check_for_language = patch_check_function(dj_check_bck)
    trans_real_bck = trans_real.check_for_language
    trans_real.check_for_language = patch_check_function(trans_real_bck)

    trans_bck = trans_real.translation
    def translation(language, *args, **kwargs):
        if language.startswith("pse"):
            return UpperPseudoLanguage()

        return trans_bck(language, *args, **kwargs)

    test = trans_bck
    trans_real.translation = translation
