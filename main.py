"""Developer Excuses entry for make.fun.

Writes one funny single-line excuse a developer gives when code
breaks in production to entry.txt in the output directory.
"""

import os

TEXT = "It worked in staging because staging has never met a real user."


def validated_text() -> str:
    """Check the entry against the sealed gate before writing it.

    Gate: UTF-8 text of 1 to 200 characters, not only white space,
    exactly one line.
    """
    raw = TEXT.encode("utf-8")
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text:
        raise ValueError("entry must be a single line")
    return text


def main() -> None:
    text = validated_text()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    # Read the bytes back to prove what was written is what we validated.
    with open(path, "rb") as f:
        written = f.read().decode("utf-8")
    if written != text + "\n":
        raise ValueError("written entry does not match validated text")


if __name__ == "__main__":
    main()
