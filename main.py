#!/usr/bin/env python3
"""Write the 3 AM commit message entry to /output/entry.txt.

Stdlib only, deterministic. Writes via a temp file in the same
directory as the destination, chmods it world-readable, then
atomically replaces the destination. No trailing newline.
"""

import os
import tempfile

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ENTRY = "fix(prod): reviewed my own diff at 3 AM and can confirm it is beautiful. the outage is unrelated (it is not unrelated)"

# Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-200
# characters, not only whitespace.
assert 1 <= len(ENTRY) <= 200, "entry must be 1-200 characters"
assert ENTRY.strip(), "entry must not be only whitespace"
ENTRY.encode("utf-8")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dest = os.path.join(OUTPUT_DIR, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=OUTPUT_DIR, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        os.chmod(tmp, 0o644)
        os.replace(tmp, dest)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
