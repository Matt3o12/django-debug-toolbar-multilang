from debug_toolbar_multilang.pseudo import PseudoLanguage


class UpperPseudoLanguage(PseudoLanguage):
    """
    Uppercases every messages it gets.
    """

    def make_pseudo(self, message):
        # Import here in order to avoid a circular import on rare
        # circumstances.
        from debug_toolbar_multilang.pseudo import STR_FORMAT_PATTERN
        result = list(message.upper())
        for theMatch in STR_FORMAT_PATTERN.finditer(message):
            start, end = theMatch.span()
            result[start:end] = theMatch.group()

        return "".join(result)

    def language(self):
        return "pse-upper"

    @property
    def name(self):
        return "Upper-Pseudo Language"
