# coding=UTF-8
from gettext import NullTranslations

from django.utils import six
from django.utils.translation.trans_real import CONTEXT_SEPARATOR


class PseudoLanguage(NullTranslations):
    def get_pseudo(self, message):
        # remove the context seperator (added when using pgettext).
        if CONTEXT_SEPARATOR in message:
            message = message.split(CONTEXT_SEPARATOR)[1]

            # on python 2 we get a unicode unconditional due to the
            # magic character. We need to cast it back to a
            # Python 2 string (bytes).
            if six.PY2:
                message = six.binary_type(message)

        return self.make_pseudo(message)

    def make_pseudo(self, message):
        raise NotImplementedError()

    def gettext(self, message):
        return self.get_pseudo(message)

    def lgettext(self, message):
        """
        Returns the message using UTF-8 encoding (not the default one.
        Implementing it is not worth it since peseudo localization should
        only be used for testing. If you feel you need the exact behavior,
        please open an issue on Github).

        :param message: str
        :return: str
        """

        return self.get_pseudo(message)

    def ngettext(self, msgid1, msgid2, n):
        """
        n = 1: Singular
        n ≠ 1: Plurar

        :param msgid1: str
        :param msgid2: str
        :param n: int
        :return: str
        """
        if n == 1:
            return self.gettext(msgid1)
        else:
            return self.gettext(msgid2)

    def lngettext(self, msgid1, msgid2, n):
        if n == 1:
            return self.lgettext(msgid1)
        else:
            return self.lgettext(msgid2)

    def ugettext(self, message):
        return six.u(self.gettext(message))

    def ungettext(self, msgid1, msgid2, n):
        if n == 1:
            return self.ugettext(msgid1)
        else:
            return self.ugettext(msgid2)
