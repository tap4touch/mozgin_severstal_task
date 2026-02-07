import csv
from typing import Optional, Sequence

from src.data_models.models import ErrorRecord, Report


def _parse_id(s: str) -> int:
    """
    Parses a string and converts it to an integer. Raises a ValueError if the string is empty.

    :param s: Input string to be parsed as an integer
    :type s: str
    :return: The integer value of the string
    :rtype: int
    """
    s = s.strip()
    if s == "":
        raise ValueError("Emtpy ID")
    return int(s)


def _parse_value(s: str) -> float:
    """
    Parses a string and converts it to a float. Raises a ValueError if the string is empty.

    :param s: Input string to be parsed as a float
    :type s: str
    :return: The float value of the string
    :rtype: float
    """
    s = s.strip()
    if s == "":
        raise ValueError("Empty value")
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    if "," in s and "." in s:
        raise ValueError("Invalid value with both comma and dot")
    return float(s)


def _detect_dialect(sample: str) -> Optional[csv.Dialect]:
    """
    Detects the CSV dialect of a given sample string. If the dialect cannot be detected, returns None.

    :param sample: A sample string from the input file to analyze for dialect detection
    :type sample: str
    :return: Dialect object if detected, otherwise None
    :rtype: Optional[csv.Dialect]
    """
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample)
        return dialect  # type: ignore
    except csv.Error:
        return None


def process_lines(lines: Sequence[str]) -> Report:
    """
    Processes a sequence of lines from an input file, parsing each line according to the expected format and collecting
    statistics about the parsing results. It returns a Report object containing the total number of records, the number of
    successfully parsed records, the number of bad records, and a list of errors encountered during parsing.

    :param lines: A sequence of strings representing lines from an input file
    :type lines: Sequence[str]
    :return: A Report object containing statistics about the parsing results
    :rtype: Report
    """
    errors: list[ErrorRecord] = []
    total = 0
    ok = 0
    not_empty_lines = [line for line in lines if line.strip() != ""]
    sample = "".join(not_empty_lines[:10]) if not_empty_lines else ""
    dialect = _detect_dialect(sample)

    for idx, line in enumerate(lines, start=1):
        total += 1
        raw_line = line.rstrip("\n")
        if raw_line.strip() == "":
            errors.append(
                ErrorRecord(line_number=idx, raw_line=raw_line, reason="Empty line")
            )
            continue

        try:
            reader = csv.reader([raw_line], dialect=dialect or csv.excel)
            fields = next(reader, [])  # type: ignore
        except Exception as e:
            errors.append(
                ErrorRecord(
                    line_number=idx,
                    raw_line=raw_line,
                    reason=f"CSV parsing error: {str(e)}",
                )
            )
            continue

        if len(fields) < 3:
            errors.append(
                ErrorRecord(
                    line_number=idx,
                    raw_line=raw_line,
                    reason="Not enough fields, expected 3",
                )
            )
            continue

        try:
            id = _parse_id(fields[0])  # type: ignore  # noqa: F841
        except Exception as e:
            errors.append(
                ErrorRecord(
                    line_number=idx,
                    raw_line=raw_line,
                    reason=f"ID parsing error: {str(e)}",
                )
            )
            continue

        try:
            value = _parse_value(fields[-1])  # type: ignore  # noqa: F841
        except Exception as e:
            errors.append(
                ErrorRecord(
                    line_number=idx,
                    raw_line=raw_line,
                    reason=f"Value parsing error: {str(e)}",
                )
            )
            continue

        name_parts = [p.strip() for p in fields[1:-1]]
        name = " ".join(name_parts).strip()
        if name == "":
            errors.append(
                ErrorRecord(
                    line_number=idx, raw_line=raw_line, reason="Empty name field"
                )
            )
            continue
        ok += 1
    bad = total - ok
    return Report(total_records=total, ok_records=ok, bad_records=bad, errors=errors)
