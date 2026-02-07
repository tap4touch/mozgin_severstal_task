import argparse
from pathlib import Path
from typing import Any

from src.helpers.cli import pick_format_from_output
from src.helpers.parser import process_lines
from src.renderers.txt import render_txt
from src.renderers.md import render_md
from src.renderers.adoc import render_adoc


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="severstal-tool", description="Process data and generate a report."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input file")
    parser.add_argument(
        "-o",
        "--output",
        default="result.txt",
        help="Path to the output file. Default is 'result.txt', must be .txt, .md, or .adoc",
    )
    parser.add_argument(
        "-c", "--console", action="store_true", help="Print the report to console"
    )
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.")
        return 2

    try:
        text = input_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"Error reading input file: {e}")
        return 2

    lines = text.splitlines(keepends=True)
    report = process_lines(lines)
    out: str | dict[Any, Any] = ""

    if args.console:
        fmt = "txt"
        out = render_txt(report)
        print(out)

    output = Path(args.output)
    fmt = pick_format_from_output(output)

    if output.suffix == "":
        output = output.with_suffix(f".{fmt}")

    if fmt == "txt" and not args.console:
        out = render_txt(report)
    elif fmt == "md":
        out = render_md(report)
    elif fmt == "adoc":
        out = render_adoc(report)

    try:
        output.write_text(out, encoding="utf-8")  # type: ignore
        print(f"Report successfully written to '{output}'")
    except Exception as e:
        print(f"Error writing output file: {e}")
        return 2

    return 0
