"""Hash chain over the public record — makes "every published signal, unedited" checkable.

Each public_record row carries
  prev_hash  hash of the previous row (for the first chained row: sha256 of all bytes
             written before it, so pre-chain legacy rows are anchored too)
  hash       sha256 of the row's canonical JSON (sorted keys, no spaces, without `hash`)

Deleting, editing or reordering any earlier row breaks every hash after it. The head hash
goes out on the public page, the daily report and (shortened) in each channel message,
whose Telegram timestamps are a third-party record of when each row existed.

Standard library only, so subscribers can verify the published file themselves:

  python chain.py public_chain.jsonl
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def canonical(row: dict) -> bytes:
    body = {k: v for k, v in row.items() if k != "hash"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def row_hash(row: dict) -> str:
    return hashlib.sha256(canonical(row)).hexdigest()


def next_prev_hash(path: Path) -> str:
    """prev_hash for the row about to be appended to `path`."""
    data = path.read_bytes() if path.exists() else b""
    lines = [l for l in data.splitlines() if l.strip()]
    if lines:
        try:
            last = json.loads(lines[-1])
            if last.get("hash"):
                return last["hash"]
        except json.JSONDecodeError:
            pass
    return hashlib.sha256(data).hexdigest()


def chained(path: Path, row: dict) -> dict:
    row = {**row, "prev_hash": next_prev_hash(path)}
    row["hash"] = row_hash(row)
    return row


def verify(data: bytes) -> tuple[bool, int, str, str]:
    """-> (ok, chained rows checked, head hash, error). `data` = file bytes, rows in write order."""
    prefix = b""
    prev: str | None = None
    n = 0
    for line in data.splitlines(keepends=True):
        if not line.strip():
            prefix += line
            continue
        row = json.loads(line)
        if "hash" in row:
            expected_prev = prev if prev is not None else hashlib.sha256(prefix).hexdigest()
            if row.get("prev_hash") != expected_prev:
                return False, n, prev or "", f"row {row.get('signal_id')}: prev_hash mismatch (deleted / reordered row before it)"
            if row_hash(row) != row["hash"]:
                return False, n, prev or "", f"row {row.get('signal_id')}: content changed after it was written"
            prev = row["hash"]
            n += 1
        elif prev is not None:
            return False, n, prev, f"row {row.get('signal_id')}: unchained row after the chain started"
        prefix += line
    return True, n, prev or "", ""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python chain.py public_chain.jsonl")
    ok, n, head, err = verify(Path(sys.argv[1]).read_bytes())
    print(f"{'OK' if ok else 'BROKEN'}: {n} chained rows, head {head}" + (f"\n{err}" if err else ""))
    sys.exit(0 if ok else 1)
