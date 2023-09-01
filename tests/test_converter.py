import pytest

import morsecode
from morsecode import converter


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("SOS", "...   ---   ..."),
        ("MORSE", "--   ---   .-.   ...   ."),
        ("CODE", "-.-.   ---   -..   ."),
        ("", ""),
    ],
)
def test_string_to(test_input, expected):
    actual = converter.string_to(test_input)
    assert actual == expected, "Conversion failure"


@pytest.mark.parametrize("test_input,error_message", [("|", "'|'"), ("BAD*", "'*'")])
def test_string_to_negative(test_input, error_message):
    with pytest.raises(KeyError) as e_info:
        converter.string_to(test_input)
    raised = e_info.value
    assert str(raised) == error_message
