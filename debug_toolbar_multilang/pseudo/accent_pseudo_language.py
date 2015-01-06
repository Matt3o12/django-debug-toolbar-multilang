from django.utils import six

# Static character map used for converting ASCI characters
# pseudo unicode string.
# Character codes are taken from Java-pseudolocalizaion
# https://code.google.com/p/pseudolocalization-tool/source/browse/trunk/java/com/google/i18n/pseudolocalization/methods/Accenter.java
from debug_toolbar_multilang.pseudo import PseudoLanguage

_chars = {
    " ": six.u("\u2003"),
    "!": six.u("\u00a1"),
    "\"": six.u("\u2033"),
    "#": six.u("\u266f"),
    "$": six.u("\u20ac"),
    "%": six.u("\u2030"),
    "&": six.u("\u214b"),
    "'": six.u("\u00b4"),
    ")": six.u("}"),
    "(": six.u("{"),
    "*": six.u("\u204e"),
    "+": six.u("\u207a"),
    ",": six.u("\u060c"),
    "-": six.u("\u2010"),
    ".": six.u("\u00b7"),
    "/": six.u("\u2044"),
    "0": six.u("\u24ea"),
    "1": six.u("\u2460"),
    "2": six.u("\u2461"),
    "3": six.u("\u2462"),
    "4": six.u("\u2463"),
    "5": six.u("\u2464"),
    "6": six.u("\u2465"),
    "7": six.u("\u2466"),
    "8": six.u("\u2467"),
    "9": six.u("\u2468"),
    ":": six.u("\u2236"),
    ";": six.u("\u204f"),
    "<": six.u("\u2264"),
    "=": six.u("\u2242"),
    ">": six.u("\u2265"),
    "?": six.u("\u00bf"),
    "@": six.u("\u055e"),
    "A": six.u("\u00c5"),
    "B": six.u("\u0181"),
    "C": six.u("\u00c7"),
    "D": six.u("\u00d0"),
    "E": six.u("\u00c9"),
    "F": six.u("\u0191"),
    "G": six.u("\u011c"),
    "H": six.u("\u0124"),
    "I": six.u("\u00ce"),
    "J": six.u("\u0134"),
    "K": six.u("\u0136"),
    "L": six.u("\u013b"),
    "M": six.u("\u1e40"),
    "N": six.u("\u00d1"),
    "O": six.u("\u00d6"),
    "P": six.u("\u00de"),
    "Q": six.u("\u01ea"),
    "R": six.u("\u0154"),
    "S": six.u("\u0160"),
    "T": six.u("\u0162"),
    "U": six.u("\u00db"),
    "V": six.u("\u1e7c"),
    "W": six.u("\u0174"),
    "X": six.u("\u1e8a"),
    "Y": six.u("\u00dd"),
    "Z": six.u("\u017d"),
    "[": six.u("\u2045"),
    "\\": six.u("\u2216"),
    "]": six.u("\u2046"),
    "^": six.u("\u02c4"),
    "_": six.u("\u203f"),
    "`": six.u("\u2035"),
    "a": six.u("\u00e5"),
    "b": six.u("\u0180"),
    "c": six.u("\u00e7"),
    "d": six.u("\u00f0"),
    "e": six.u("\u00e9"),
    "f": six.u("\u0192"),
    "g": six.u("\u011d"),
    "h": six.u("\u0125"),
    "i": six.u("\u00ee"),
    "j": six.u("\u0135"),
    "k": six.u("\u0137"),
    "l": six.u("\u013c"),
    "m": six.u("\u0271"),
    "n": six.u("\u00f1"),
    "o": six.u("\u00f6"),
    "p": six.u("\u00fe"),
    "q": six.u("\u01eb"),
    "r": six.u("\u0155"),
    "s": six.u("\u0161"),
    "t": six.u("\u0163"),
    "u": six.u("\u00fb"),
    "v": six.u("\u1e7d"),
    "w": six.u("\u0175"),
    "x": six.u("\u1e8b"),
    "y": six.u("\u00fd"),
    "z": six.u("\u017e"),
    "{": six.u("("),
    "}": six.u(")"),
    "|": six.u("\u00a6"),
    "~": six.u("\u02de"),
}


def get_char(char):
    return _chars[char]


class AccentPseudoLanguage(PseudoLanguage):
    def make_pseudo(self, message):
        from debug_toolbar_multilang.pseudo import STR_FORMAT_PATTERN
        nonReplacements = []
        for match in STR_FORMAT_PATTERN.finditer(message):
            nonReplacements.append(match)

        string = six.u("")
        currentMatch = self._getNextMatch(nonReplacements)
        for i, char in enumerate(message):
            start, end = currentMatch.span() if currentMatch else (0, 0)
            if currentMatch and i > end:
                currentMatch = self._getNextMatch(nonReplacements)

            if not (currentMatch and start <= i < end):
                try:
                    string += get_char(char)
                except KeyError:
                    string += char
            else:
                string += char

        return string

    def _getNextMatch(self, matches):
        return matches.pop(0) if matches else None

    def language(self):
        return "pse-accent"

    @property
    def name(self):
        return "Accented-Pseudo Language"
