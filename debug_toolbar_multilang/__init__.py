from django.conf.locale import LANG_INFO
from django.conf import settings

from debug_toolbar_multilang.pseudo.utils import enable_pseudo_localization


if getattr(settings, "ENABLE_PSEUDO_LOCALIZATION", False):  # pragma: no cover
    LANG_INFO["pse"] = {
        'bidi': False,
        'code': "pse",
        'name': "Pseudolanguage",
        'name_local': "Pseudolanguage"

    }

    enable_pseudo_localization()
