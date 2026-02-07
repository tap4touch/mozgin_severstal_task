from pathlib import Path


def pick_format_from_output(output: Path) -> str:
    suff = output.suffix.lower()
    res = "txt"
    if suff == ".md":
        res = "md"
    elif suff == ".adoc":
        res = "adoc"
    return res
