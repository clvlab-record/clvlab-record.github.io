# CLV LAB — Public Record

Delayed sports signals for Polymarket (NBA · NFL · CFB), published here automatically every hour.
Every signal is listed — wins and losses — once its channel delay has passed.

- **[Public record](./)** — pick, entry price, edge bucket, and CLV once the game starts.
- **CLV** (closing line value) = sharp closing no-vig price ÷ published entry price − 1. Positive CLV over
  many picks is what separates real edge from luck.

## Verify nothing was deleted or edited

Every record carries the hash of the record before it. Download
[`public_chain.jsonl`](public_chain.jsonl) and [`chain.py`](chain.py) (Python standard library only) and run:

    python chain.py public_chain.jsonl

It prints `OK` and the chain head, or the first record where the chain breaks. The head also appears on the
public page, and each channel message carries the first 12 characters of its record's hash. This repository's
commit history is a second timestamped log.

Not financial advice.
