# CLV LAB — Public Record

Public sports-signal research record, published here automatically every hour. Not for sale.
Every signal is listed — wins and losses. The run: 100 public signals, each counted once.

- **[Public record](./)** — side, entry price, edge bucket, and CLV once the game starts.
- **CLV** (closing line value) = sharp closing no-vig price ÷ published entry price − 1. Positive CLV over
  many picks is what separates real edge from luck.

## Seasons

The record runs in seasons. Season 0 was the testing period; Season 1 starts with the NBA regular season
(2026-10-20 00:00 UTC) and its counts start again at 1 / 100. Season 0's rows are not deleted: they are archived in
[`archive/season-0/public_chain.jsonl`](archive/season-0/), and Season 1's run starts with the hash of Season 0's last
row, so the two runs verify as one: `python chain.py public_chain.jsonl --after <Season 0 head>`.

## Verify nothing was deleted or edited

Every record carries the hash of the record before it. Download
[`public_chain.jsonl`](public_chain.jsonl) and [`chain.py`](chain.py) (Python standard library only) and run:

    python chain.py public_chain.jsonl

It prints `OK` and the chain head, or the first record where the chain breaks. The head also appears on the
public page, and each channel message carries the first 12 characters of its record's hash. This repository's
commit history is a second timestamped log.

## Anchored to Bitcoin

Once a day the chain head is written to [`anchors/<date>.txt`](anchors/) and timestamped with
[OpenTimestamps](https://opentimestamps.org): `anchors/<date>.txt.ots` proves the file existed by a Bitcoin block.
Run `ots verify anchors/<date>.txt.ots` (or drop both files on opentimestamps.org). Then take the chain as it was
that day — its first `rows` rows (the number is in the `.txt`) — and check that `chain.py` prints the head in the
`.txt`:

    cat public_chain.jsonl | head -n <rows> > upto.jsonl && python chain.py upto.jsonl

The chain keeps growing, so the head of the whole file moves on; the first `rows` rows never change. Every record up
to that head is covered by the anchor.

Not financial advice.
