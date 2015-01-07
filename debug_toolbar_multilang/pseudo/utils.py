import django
from django.conf.locale import LANG_INFO

from django.utils import translation as dj_translation
from django.utils.translation import trans_real

_languages = {}


def patch_check_function(org):
    """
    Patches the check_for_language function so that it always returns
    true for pseudo localizations.

    :param org: the original function.
    :return: the patched function.
    """

    def check_for_language(lang):
        if lang.startswith("pse"):
            return True

        return org(lang)

    if django.VERSION < (1, 7):
        from django.utils.functional import memoize
        check_for_language = memoize(check_for_language, {}, 1)
    else:
        from django.utils import lru_cache
        check_for_language = lru_cache.lru_cache(1000)(check_for_language)

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
        if language in _languages:
            return _languages[language]

        return trans_bck(language, *args, **kwargs)

    trans_real.translation = translation


def register_pseudo_language(language):
    """
    Registers a new pseudo language to django.conf.locale.LANG_INFO and
    to djdt-multilang's own register of pseudo languages. Adding a language
    to LANG_INFO is not enough.

    :param language: PseudoLanguage
    """
    LANG_INFO[language.code] = language.get_info_dict()
    _languages[language.code] = language

