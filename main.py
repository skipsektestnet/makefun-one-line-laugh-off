"""One-Line Laugh-Off: writes the entry text to /output/entry.txt.

Why this line: one joke that lands on a cold read -- a simple request
escalates absurdly in three beats (rooster, marching band, a man yelling
the full legal name), with the punch on the final detail.
"""

import os

# The entry itself: exactly one funny line, 116 characters, no setup notes.
ENTRY = "I asked the hotel for a wake-up call and they sent a rooster, a marching band, and a man yelling my full legal name."

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def main():
    # Guard: never submit a blank entry to the sealed gate.
    assert ENTRY and not ENTRY.isspace(), "entry must not be empty"
    assert len(ENTRY) <= 200, "entry exceeds 200 characters"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote", OUTPUT_PATH, len(ENTRY), "chars")


if __name__ == "__main__":
    main()
