from . import converter, lexer


class Translator:
    def __init__(self, tokens, to_mc: bool = True) -> None:
        self.tokens = tokens
        self.to_mc = to_mc

    def translate(self):
        if self.to_mc:
            return self._translateTo()
        else:
            return self._translateFrom()

    def _translateTo(self):
        result = ""
        for token in self.tokens:
            match token.type:
                case lexer.TOKEN_PLAIN_TEXT:
                    result += converter.string_to(token.value.upper())

                case lexer.TOKEN_PLAIN_SPACE:
                    result += converter.WORD_SPACE

                case lexer.TOKEN_UNSUPPORTED:
                    result += converter.LETTER_SPACE

                case _:
                    pass
        return result

    def _translateFrom(self):
        result = ""
        for token in self.tokens:
            match token.type:
                case lexer.TOKEN_MC_TEXT:
                    result += converter.from_morse_code(token.value)

                case lexer.TOKEN_MC_WORD:
                    result += " "

                case lexer.TOKEN_MC_SPACE:
                    pass

                case lexer.TOKEN_UNSUPPORTED:
                    pass

                case _:
                    pass
        return result
