# CLV LAB — Public Record

Public sports-signal research record, published here automatically every hour. Not for sale.
Every signal is listed — wins and losses. The run: 100 public signals, each counted once.

- **[Public record](./)** — side, entry price, edge bucket, and CLV once the game starts.
- **CLV** (closing line value) = sharp closing no-vig price ÷ published entry price − 1. Positive CLV over
  many picks is what separates real edge from luck.

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
Run `ots verify anchors/<date>.txt.ots` (or drop both files on opentimestamps.org) and check that the head in the
`.txt` equals the head `chain.py` prints. Every record before that head is covered by it.

Not financial advice.
