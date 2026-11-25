"""One-Line Laugh-Off — emit the one-line entry and validate its gate.

The entry is a single line of at most 200 characters. The line is stored as
one literal; each bounty rule is a small check function, and the checks run
in order as a pipeline before the line is written to entry.txt.
"""

import os
import sys
from pathlib import Path

LINE = "I asked the hotel for a wake-up call and they sent a rooster, a marching band, and a man yelling my full legal name."
CHAR_LIMIT = 200
OUT_FILE = Path("entry.txt")


class EntryProblem(Exception):
    """Raised when the entry line breaks one of the bounty rules."""


def _fail(message):
    raise EntryProblem(message)


def _check_not_blank(line):
    if not line.strip():
        _fail("entry line must not be blank")


def _check_length(line):
    if len(line) > CHAR_LIMIT:
        _fail(f"entry is {len(line)} characters, over the {CHAR_LIMIT} limit")


def _check_one_line(line):
    if "\n" in line or "\r" in line:
        _fail("entry must be exactly one line")


def _check_no_padding(line):
    if line != line.strip():
        _fail("entry must not start or end with whitespace")


def _check_printable(line):
    if not line.isprintable():
        _fail("entry must contain only printable characters")


def _check_no_control(line):
    for char in line:
        if ord(char) < 32 or ord(char) == 127:
            _fail("entry must not contain control characters")


VALIDATORS = (
    _check_not_blank,
    _check_length,
    _check_one_line,
    _check_no_padding,
    _check_printable,
    _check_no_control,
)


def check_line(line):
    """Run every validator over the line; return the line unchanged."""
    for validator in VALIDATORS:
        validator(line)
    return line


def emit(line, out_dir):
    """Validate the line, then write it (plus a trailing newline) out."""
    checked = check_line(line)
    target = Path(out_dir) / OUT_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(checked + "\n", encoding="utf-8")
    return target


def run(argv):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or (
        argv[1] if len(argv) > 1 else "."
    )
    path = emit(LINE, out_dir)
    print(f"wrote {path} ({len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run(sys.argv))
    except EntryProblem as problem:
        print(f"entry rejected: {problem}", file=sys.stderr)
        sys.exit(1)
