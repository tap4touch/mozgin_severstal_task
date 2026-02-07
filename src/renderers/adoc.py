from src.data_models.models import Report


def render_adoc(report: Report) -> str:
    """
    Renders a report in AsciiDoc format.

    :param report: The report to be rendered
    :type report: Report
    :return: The rendered report as an AsciiDoc-formatted string
    :rtype: str
    """
    lines: list[str] = []
    lines.append("== Parsing Report")
    lines.append("")
    lines.append("|===\n| Total | Correct | Incorrect")
    lines.append(
        f"| {report.total_records} | {report.ok_records} | {report.bad_records}"
    )
    lines.append("|===")
    lines.append("")
    lines.append("== Errors")
    if not report.errors:
        lines.append("No errors found.")
    else:
        for error in report.errors:
            raw = error.raw_line.strip()
            lines.append(f"* Line {error.line_number}: {error.reason}")
            lines.append(f"  * Raw line: `{raw}`")
    lines.append("")
    return "\n".join(lines)
