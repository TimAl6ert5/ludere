import pytest

import morsecode
from morsecode import lexer


def check_tokens(actual_tokens, expected_tokens):
    assert len(actual_tokens) == len(
        expected_tokens
    ), "Conversion failure: Incorrect number of tokens"

    for i in range(len(actual_tokens)):
        actual = actual_tokens[i]
        expected = expected_tokens[i]
        assert actual == expected, "Conversion failure: mismatched token"


@pytest.mark.parametrize(
    "test_input,expected_tokens",
    [
        ("SOS", [lexer.Token(lexer.TOKEN_PLAIN_TEXT, "SOS", 0, 3)]),
        (
            "MORSE CODE",
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "MORSE", 0, 5),
                lexer.Token(lexer.TOKEN_PLAIN_SPACE, " ", 5, 6),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "CODE", 6, 10),
            ],
        ),
        (
            "ONE\nTWO",
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "ONE", 0, 3),
                lexer.Token(lexer.TOKEN_PLAIN_SPACE, "\n", 3, 4),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "TWO", 4, 7),
            ],
        ),
        (
            "alpha \tbeta",
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "alpha", 0, 5),
                lexer.Token(lexer.TOKEN_PLAIN_SPACE, " \t", 5, 7),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "beta", 7, 11),
            ],
        ),
    ],
)
def test_lexer_to_strict_positive(test_input, expected_tokens):
    lxr = lexer.Lexer(test_input)
    actual_tokens = lxr.tokenize()
    check_tokens(actual_tokens, expected_tokens)


@pytest.mark.parametrize(
    "test_input,error_message",
    [
        ("|", "Unhandled character | at index 0."),
        ("fail *", "Unhandled character * at index 5."),
    ],
)
def test_lexer_to_strict_negative(test_input, error_message):
    lxr = lexer.Lexer(test_input)
    with pytest.raises(lexer.UnhandledCharacterException) as e_info:
        lxr.tokenize()
    raised = e_info.value
    assert str(raised) == error_message


@pytest.mark.parametrize(
    "test_input,expected_tokens",
    [
        ("|", [lexer.Token(lexer.TOKEN_UNSUPPORTED, "|", 0, 1)]),
        (
            "S~OS",
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "S", 0, 1),
                lexer.Token(lexer.TOKEN_UNSUPPORTED, "~", 1, 2),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "OS", 2, 4),
            ],
        ),
        (
            "SO***S",
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "SO", 0, 2),
                lexer.Token(lexer.TOKEN_UNSUPPORTED, "***", 2, 5),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "S", 5, 6),
            ],
        ),
        (
            "ABC\n#123",
            [
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "ABC", 0, 3),
                lexer.Token(lexer.TOKEN_PLAIN_SPACE, "\n", 3, 4),
                lexer.Token(lexer.TOKEN_UNSUPPORTED, "#", 4, 5),
                lexer.Token(lexer.TOKEN_PLAIN_TEXT, "123", 5, 8),
            ],
        ),
    ],
)
def test_lexer_to_loose(test_input, expected_tokens):
    lxr = lexer.Lexer(test_input, True, False)
    actual_tokens = lxr.tokenize()
    check_tokens(actual_tokens, expected_tokens)


@pytest.mark.parametrize(
    "test_input,expected_tokens",
    [
        (
            ".",
            [
                lexer.Token(lexer.TOKEN_MC_TEXT, ".", 0, 1),
            ],
        ),
        (
            "...   ---   ...",
            [
                lexer.Token(lexer.TOKEN_MC_TEXT, "...", 0, 3),
                lexer.Token(lexer.TOKEN_MC_SPACE, "   ", 3, 6),
                lexer.Token(lexer.TOKEN_MC_TEXT, "---", 6, 9),
                lexer.Token(lexer.TOKEN_MC_SPACE, "   ", 9, 12),
                lexer.Token(lexer.TOKEN_MC_TEXT, "...", 12, 15),
            ],
        ),
    ],
)
def test_lexer_from_strict_positive(test_input, expected_tokens):
    lxr = lexer.Lexer(test_input, False)
    actual_tokens = lxr.tokenize()
    check_tokens(actual_tokens, expected_tokens)


@pytest.mark.parametrize(
    "test_input,error_message",
    [
        ("|", "Unhandled character | at index 0."),
        ("...   ---   ...x", "Unhandled character x at index 15."),
        (".---\n..---", "Unhandled character \n at index 4."),
    ],
)
def test_lexer_from_strict_negative(test_input, error_message):
    lxr = lexer.Lexer(test_input, False)
    with pytest.raises(lexer.UnhandledCharacterException) as e_info:
        lxr.tokenize()
    raised = e_info.value
    assert str(raised) == error_message


@pytest.mark.parametrize(
    "test_input,expected_tokens",
    [
        ("|", [lexer.Token(lexer.TOKEN_UNSUPPORTED, "|", 0, 1)]),
        (
            "...   ---   ...x",
            [
                lexer.Token(lexer.TOKEN_MC_TEXT, "...", 0, 3),
                lexer.Token(lexer.TOKEN_MC_SPACE, "   ", 3, 6),
                lexer.Token(lexer.TOKEN_MC_TEXT, "---", 6, 9),
                lexer.Token(lexer.TOKEN_MC_SPACE, "   ", 9, 12),
                lexer.Token(lexer.TOKEN_MC_TEXT, "...", 12, 15),
                lexer.Token(lexer.TOKEN_UNSUPPORTED, "x", 15, 16),
            ],
        ),
        (
            ".-\n-...",
            [
                lexer.Token(lexer.TOKEN_MC_TEXT, ".-", 0, 2),
                lexer.Token(lexer.TOKEN_UNSUPPORTED, "\n", 2, 3),
                lexer.Token(lexer.TOKEN_MC_TEXT, "-...", 3, 7),
            ],
        ),
    ],
)
def test_lexer_from_loose(test_input, expected_tokens):
    lxr = lexer.Lexer(test_input, False, False)
    actual_tokens = lxr.tokenize()
    check_tokens(actual_tokens, expected_tokens)
