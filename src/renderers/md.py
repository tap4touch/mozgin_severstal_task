from src.data_models.models import Report


def render_md(report: Report) -> str:
    """
    Renders the parsing report in Markdown format.

    :param report: The Report object containing parsing statistics and error details
    :type report: Report
    :return: A string representation of the report in Markdown format
    :rtype: str
    """
    lines: list[str] = []
    lines.append("## Parsing Report")
    lines.append("")
    lines.append(f"{"Total":^10} | {"Correct":^10} | {"Incorrect":^10}")
    lines.append(f"{'-'*10} | {'-'*10} | {'-'*10}")
    lines.append(
        f"{report.total_records:^10} | {report.ok_records:^10} | {report.bad_records:^10}"
    )
    lines.append("")
    lines.append("## Errors")
    if not report.errors:
        lines.append("No errors found.")
    else:
        for error in report.errors:
            raw = error.raw_line.strip()
            lines.append(f"- **Line {error.line_number}**: {error.reason}")
            lines.append(f"  - Raw line: `{raw}`")
    lines.append("")
    return "\n".join(lines)
