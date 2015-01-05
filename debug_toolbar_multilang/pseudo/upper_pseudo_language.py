from debug_toolbar_multilang.pseudo import PseudoLanguage


class UpperPseudoLanguage(PseudoLanguage):
    def make_pseudo(self, message):
        # Import here in order to avoid a circular import on rare
        # circumstances.
        from debug_toolbar_multilang.pseudo import STR_FORMAT_PATTERN

        messageArray = bytearray(message.upper(), encoding="UTF-8")
        for theMatch in STR_FORMAT_PATTERN.finditer(message.encode()):
            start, end = theMatch.span()
            messageArray[start:end] = theMatch.group()

        return messageArray.decode("UTF-8")

    def language(self):
        return "pse"