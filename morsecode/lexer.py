import re

TOKEN_UNSUPPORTED = 0
TOKEN_MC_TEXT = 1
TOKEN_MC_SPACE = 2
TOKEN_MC_WORD = 3
TOKEN_PLAIN_TEXT = 4
TOKEN_PLAIN_SPACE = 5

PATTERNS_TO = [
    (r"[a-zA-Z0-9\.\,?\'\!\/\(\)\&\:\;\=\+\-\_\\\$\@]+", TOKEN_PLAIN_TEXT),
    (r"[\s]+", TOKEN_PLAIN_SPACE),
]

PATTERNS_FROM = [
    (r"[\.-]+", TOKEN_MC_TEXT),
    (
        r" {7}",
        TOKEN_MC_WORD,
    ),  # order matters, look for the longer word, before the shorter space sequence
    (r" {3}", TOKEN_MC_SPACE),
]


class Token:
    def __init__(
        self, tkn_type: int, value: str, begin: int = None, end: int = None
    ) -> None:
        self.type = tkn_type
        self.value = value
        self.begin = begin
        self.end = end

    def __repr__(self) -> str:
        return "<Token type({}) value({}) begin({}), end({})>".format(
            self.type, self.value, self.begin, self.end
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Token):
            return False
        else:
            return (
                self.type == __value.type
                and self.value == __value.value
                and self.begin == __value.begin
                and self.end == __value.end
            )


class Cursor:
    def __init__(self, index: int = 0) -> None:
        self.index: int = index

    def advance(self) -> None:
        self.index += 1

    def advance_to(self, location: int) -> None:
        self.index = location

    def __str__(self) -> str:
        return str(self.index)


class UnhandledCharacterException(Exception):
    def __init__(self, character: str, position: int) -> None:
        super().__init__()
        self.character = character
        self.position = position

    def __str__(self) -> str:
        return "Unhandled character {} at index {}.".format(
            self.character, self.position
        )


class Lexer:
    def __init__(self, text: str, to_mc: bool = True, strict_mode: bool = True) -> None:
        self.text = text
        self.to_mc = to_mc
        self.strict_mode = strict_mode
        self.cursor = Cursor()

    def tokenize(self):
        tokens = []

        if self.to_mc:
            patterns = PATTERNS_TO
        else:
            patterns = PATTERNS_FROM

        while self.cursor.index < len(self.text):
            match = None
            for pattern in patterns:
                expression, tkn_type = pattern
                regex = re.compile(expression)
                match = regex.match(self.text, self.cursor.index)
                if match:
                    value = match.group(0)
                    token = Token(tkn_type, value, self.cursor.index, match.end(0))
                    tokens.append(token)
                    break
            if not match:
                if self.strict_mode:
                    raise UnhandledCharacterException(
                        self.text[self.cursor.index], self.cursor
                    )
                else:
                    # If the last token was unsupported, update it
                    last_token = None
                    nmbr_tokens = len(tokens)
                    if nmbr_tokens > 0:
                        last_token = tokens[nmbr_tokens - 1]
                    if last_token is not None and last_token.type == TOKEN_UNSUPPORTED:
                        last_token.value = (
                            last_token.value + self.text[self.cursor.index]
                        )
                        last_token.end = self.cursor.index + 1
                    else:
                        token = Token(
                            TOKEN_UNSUPPORTED,
                            self.text[self.cursor.index],
                            self.cursor.index,
                            self.cursor.index + 1,
                        )
                        tokens.append(token)
                    self.cursor.advance()
            else:
                self.cursor.advance_to(match.end(0))

        return tokens
