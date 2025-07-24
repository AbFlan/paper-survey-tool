from datetime import datetime
from constants import *
from validation import validation_inputs
import pytest


def test_valid_inputs():

    errors, warnings, start_year, end_year = validation_inputs("AI", "1234-5678", "2024", "2025", "sample@test.com")
    assert errors == []
    assert warnings == []
    assert start_year == "2024"
    assert end_year == "2025"

def test_future_end_year():
    future_year = datetime.now().year + 1
    _, warnings, _, end_year = validation_inputs("AI", "1234-5678", "2024", str(future_year), "sample@test.com")
    assert any(FUTURE_YEAR_WARNING in warning for warning in warnings)
    assert end_year == str(datetime.now().year)


@pytest.mark.parametrize(
        "query, issn, start_year, end_year, user_email, expected_error",
        [
            ("AI", "1234-5678", "20XX", "2025", "sample@test.com", INVALID_YEAR_FORMAT),
            ("AI", "1234-5678", "2025", "2024", "sample@test.com", YEAR_ORDER_ERROR),
            ("AI", "12345678", "2024", "2025", "sample@test.com", ISSN_FORMAT_ERROR),
            ("AI", "1234-5678", "2024", "2025", "samplemail", EMAIL_FORMAT_ERROR),
            ("", "1234-5678", "2024", "2025", "sample@test.com", EMPTY_QUERY_ERROR),
        ],
        ids=[
            "bad start year",
            "start > end",
            "bad issn",
            "bad email",
            "empty query"
        ]

)
def test_input_validation_errors(query, issn, start_year, end_year, user_email, expected_error):
    errors, _, _, _ = validation_inputs(query, issn, start_year, end_year, user_email)
    assert any(expected_error in error for error in errors)