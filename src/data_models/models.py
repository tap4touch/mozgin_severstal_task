from dataclasses import dataclass


@dataclass
class ErrorRecord:
    """
    Represents an error encountered during the parsing of a line in the input file.
    """

    line_number: int
    raw_line: str
    reason: str


@dataclass
class Report:
    """
    Report of the parsing process, containing statistics and details about errors.
    """

    total_records: int
    ok_records: int
    bad_records: int
    errors: list[ErrorRecord]
