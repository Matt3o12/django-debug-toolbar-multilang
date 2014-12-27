from debug_toolbar.panels import Panel
from django.conf import settings
from django.conf.urls import url
from django.utils import translation
from debug_toolbar_multilang import views
from django.utils.translation import ugettext as _


class MultiLangPanel(Panel):
    template = "debug_toolbar_multilang/multilang.html"

    @property
    def title(self):
        return _("Languages")

    def nav_title(self):
        return _("Languages")

    def nav_subtitle(self):
        values = {
            "current": self.current_lang["name_local"],
            "total": len(settings.LANGUAGES)
        }

        return _("Current: %(current)s; total: %(total)d") % values

    def get_stats(self):
        stats = super(MultiLangPanel, self).get_stats().copy()
        stats["languages"] = self.get_available_languages()
        stats["current_lang"] = self.current_lang

        return stats

    def get_available_languages(self):
        """
        Yields all languages with its info (e.g. name, localized name, tag).
        """

        for lang in settings.LANGUAGES:
            yield translation.get_language_info(lang[0])

    @property
    def current_lang(self):
        """
        Returns a dict of the current language. The dict contains
        code, the name, localized name, and whether its bidi.

        :return: dict
        """

        return translation.get_language_info(translation.get_language())

    @classmethod
    def get_urls(cls):
        return [url(
            r"^multilang_change/$",
            views.change_language,
            name="multilang_change"
        )]