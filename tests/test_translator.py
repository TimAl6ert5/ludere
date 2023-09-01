import pytest

import morsecode
from morsecode import lexer, translator


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([lexer.Token(lexer.TOKEN_PLAIN_TEXT, "SOS", 0, 3)], "...   ---   ..."),
        (
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "MORSE", 0, 5),
                lexer.Token(lexer.TOKEN_PLAIN_SPACE, " ", 5, 6),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "CODE", 6, 10),
            ],
            "--   ---   .-.   ...   .       -.-.   ---   -..   .",
        ),
        (
            [lexer.Token(lexer.TOKEN_PLAIN_TEXT, "alpha", 0, 5)],
            ".-   .-..   .--.   ....   .-",
        ),
        (
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "S", 0, 1),
                lexer.Token(lexer.TOKEN_UNSUPPORTED, "*", 1, 2),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "OS", 2, 4),
            ],
            "...   ---   ...",
        ),
    ],
)
def test_tokens_to_mc(test_input, expected):
    t = translator.Translator(test_input)
    actual = t.translate()
    assert actual == expected, "Conversion failure"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            [
                lexer.Token(lexer.TOKEN_MC_TEXT, ".", 0, 1),
            ],
            "E",
        ),
        (
            [
                lexer.Token(lexer.TOKEN_MC_TEXT, "...", 0, 3),
                lexer.Token(lexer.TOKEN_MC_SPACE, "   ", 3, 6),
                lexer.Token(lexer.TOKEN_MC_TEXT, "---", 6, 9),
                lexer.Token(lexer.TOKEN_MC_SPACE, "   ", 9, 12),
                lexer.Token(lexer.TOKEN_MC_TEXT, "...", 12, 15),
            ],
            "SOS",
        ),
    ],
)
def test_tokens_from_mc(test_input, expected):
    t = translator.Translator(test_input, False)
    actual = t.translate()
    assert actual == expected, "Conversion failure"
