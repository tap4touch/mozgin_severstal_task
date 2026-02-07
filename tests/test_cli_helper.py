from pathlib import Path
import pytest

from src.helpers.cli import pick_format_from_output


@pytest.mark.parametrize(
    "output, expected",
    [
        (Path("result.txt"), "txt"),
        (Path("result"), "txt"),
        (Path("result.md"), "md"),
        (Path("RESULT.MD"), "md"),
        (Path("out.adoc"), "adoc"),
        (Path("OUT.ADOC"), "adoc"),
        (Path("out.json"), "txt"),
        (Path("out"), "txt"),
        (Path("path/to/out.md"), "md"),
    ],
)
def test_pick_format_from_output(output: Path, expected: str) -> None:
    """
    Tests the pick_format_from_output function to ensure it correctly identifies
    the output format based on the file extension.

    :param output: The output file path to test
    :type output: Path
    :param expected: The expected format string that should be returned by the function
    :type expected: str
    """
    assert pick_format_from_output(output) == expected
