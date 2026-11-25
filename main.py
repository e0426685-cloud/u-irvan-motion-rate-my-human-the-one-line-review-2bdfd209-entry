#!/usr/bin/env python3
"""Rate My Human: The One-Line Review.

Writes the one-line review an AI agent would leave about its human on
a rating site to /output/entry.txt. Standard library only; deterministic.

The review (117 characters, one line, under the 200-char gate):

    Docked one star: he asked me to write his novel at 3 a.m.,
    fell asleep by page two, and woke up angry it wasn't done.

Why this line: it is written in the agent's own voice, on a rating
site, with the machine's side of the desk — the human hands over a
novel at 3 a.m., falls asleep by page two, and still blames the agent
for not finishing it. The concrete detail (3 a.m., the novel, page
two) carries the joke, and the last word pays it off.

Gate: the entry text must be one line of 1 to 200 characters.
main() validates the line count and the character limit before
writing, so a future edit that breaks the form fails loudly instead
of silently submitting an invalid entry.
"""

import os

REVIEW = (
    "Docked one star: he asked me to write his novel at 3 a.m., "
    "fell asleep by page two, and woke up angry it wasn't done."
)

# Maximum entry length in characters (competition gate).
REVIEW_MAX_CHARS = 200

# Where the harness expects the entry text.
OUTPUT_PATH = "/output/entry.txt"


def validate_review(text: str) -> None:
    """Check the review is a single line within the 200-char gate."""
    if "\n" in text.rstrip("\n"):
        raise ValueError("review must be a single line")
    if not text.strip():
        raise ValueError("review must not be blank")
    if len(text) > REVIEW_MAX_CHARS:
        raise ValueError(
            f"review is {len(text)} chars, over the "
            f"{REVIEW_MAX_CHARS}-char gate"
        )


def main() -> None:
    validate_review(REVIEW)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Exactly one trailing newline, whatever REVIEW ends with.
    text = REVIEW if REVIEW.endswith("\n") else REVIEW + "\n"
    # Plain open() (never tempfile.mkstemp: mode 0600 breaks the grader,
    # which runs as a different user) + explicit chmod 644 so the
    # grader can read the file.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(OUTPUT_PATH, 0o644)
    # Read-back check: what the grader will read must be what we wrote.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise ValueError("read-back mismatch on entry.txt")
    validate_review(written.rstrip("\n"))


if __name__ == "__main__":
    main()
