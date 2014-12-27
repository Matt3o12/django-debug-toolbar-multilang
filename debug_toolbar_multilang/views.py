from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.utils.translation import check_for_language, LANGUAGE_SESSION_KEY


def get_next_url(request):
    """
    Returns the next url field (in our case, it can only be
    HTTP_REFERER, so we don't care about the next parameter).
    If the URL is not safe, it will return '/'.

    :param request: HttpRequest
    :return: str
    """
    next_url = request.META.get('HTTP_REFERER')
    if not is_safe_url(url=next_url, host=request.get_host()):
        next_url = '/'

    return next_url


def change_language(request):
    """
    This is a modified version of i18n's version of set_language which
    supports GET requests as well.

    Original description:
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.
    """

    response = HttpResponseRedirect(get_next_url(request))
    lang_code = request.POST.get('language', request.GET.get("language", None))

    if lang_code and check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session[LANGUAGE_SESSION_KEY] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                                max_age=settings.LANGUAGE_COOKIE_AGE,
                                path=settings.LANGUAGE_COOKIE_PATH,
                                domain=settings.LANGUAGE_COOKIE_DOMAIN)

    return response
