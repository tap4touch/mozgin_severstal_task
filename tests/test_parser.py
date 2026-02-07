import pytest  # type: ignore # noqa: F401

from src.helpers.parser import process_lines


def test_process_lines_counts_ok_and_bad_and_total() -> None:
    """Tests the process_lines function to ensure it correctly counts records."""
    lines = [
        '1,"Valid Name",10\n',  # ok
        "2,Another,20\n",  # ok
        "\n",  # bad
        "x,BadId,30\n",  # bad
        "3,,40\n",  # bad
        "4,Name,\n",  # bad
        "5,OnlyTwoFields\n",  # bad
    ]

    report = process_lines(lines)

    assert report.total_records == 7
    assert report.ok_records == 2
    assert report.bad_records == 5
    assert len(report.errors) == 5


def test_process_lines_error_reasons_and_line_numbers() -> None:
    """Tests the process_lines function to ensure it correctly identifies error reasons."""
    lines = [
        "\n",  # Empty line
        "x,Name,1\n",  # ID parsing error
        "1,,1\n",  # Empty name field
        "1,Name,\n",  # Value parsing error
        "1,Name\n",  # Not enough fields
    ]

    report = process_lines(lines)

    errors = {e.line_number: e.reason for e in report.errors}

    assert errors[1] == "Empty line"
    assert errors[2].startswith("ID parsing error:")
    assert errors[3] == "Empty name field"
    assert errors[4].startswith("Value parsing error:")
    assert errors[5] == "Not enough fields, expected 3"


def test_process_lines_quotes_and_commas_in_name() -> None:
    """Tests the process_lines function to ensure it correctly handles quoted fields with commas."""
    lines = [
        '1,"Name, With Comma",12.5\n',
    ]

    report = process_lines(lines)

    assert report.total_records == 1
    assert report.ok_records == 1
    assert report.bad_records == 0
    assert report.errors == []


def test_process_lines_value_with_decimal_comma_is_valid() -> None:
    """Tests the process_lines function to ensure it correctly parses values with decimal commas."""
    lines = [
        '1,"Name","12,5"\n',
    ]
    report = process_lines(lines)

    assert report.ok_records == 1
    assert report.bad_records == 0


def test_process_lines_value_with_comma_and_dot_is_invalid() -> None:
    """Tests the process_lines function to ensure it correctly identifies invalid value formats."""
    lines = [
        '1,"Name","1,2.3"\n',
    ]
    report = process_lines(lines)

    assert report.ok_records == 0
    assert report.bad_records == 1
    assert len(report.errors) == 1
    assert report.errors[0].reason.startswith("Value parsing error:")


def test_process_lines_all_empty_lines() -> None:
    """Tests the process_lines function to ensure it correctly handles a list of all empty lines."""
    lines = ["\n", "   \n", "\t\n"]
    report = process_lines(lines)

    assert report.total_records == 3
    assert report.ok_records == 0
    assert report.bad_records == 3
    assert all(e.reason == "Empty line" for e in report.errors)
