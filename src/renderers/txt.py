from src.data_models.models import Report


def render_txt(report: Report) -> str:
    """
    Renders the parsing report in plain text format.

    :param report: The Report object containing parsing statistics and error details
    :type report: Report
    :return: A string representation of the report in plain text format
    :rtype: str
    """
    lines: list[str] = []
    lines.append("Parsing Report")
    lines.append("")
    lines.append(f"Total records: {report.total_records}")
    lines.append(f"Correct: {report.ok_records}")
    lines.append(f"Incorrect: {report.bad_records}")
    lines.append("")
    lines.append("Errors:")
    if not report.errors:
        lines.append("  No errors found.")
    else:
        for error in report.errors:
            raw = error.raw_line.strip()
            lines.append(f"  Line {error.line_number}: {error.reason}")
            lines.append(f"    Raw line: {raw}")
    lines.append("")
    return "\n".join(lines)
