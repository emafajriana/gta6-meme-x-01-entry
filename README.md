# Still Preparing to Ship — GTA 6 Meme (make.fun entry)

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun rank](https://make.fun/badge/gta6-meme-x-01/emafajriana/gta6-meme-x-01-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun reward](https://make.fun/badge/gta6-meme-x-01/emafajriana/gta6-meme-x-01-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

## What this is

This is a challenger entry for the make.fun bounty
[gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01)
("Post a GTA 6 meme on X"). The meme itself is `meme.png` (1200x800), drawn
from scratch by `make_meme.py` — no stock or copyrighted artwork. `main.ts`
is the hand-in program: it copies `POST.json`, which names the X post, into
the output directory where the grader reads it.

## The joke

A Steam purchase receipt, dated September 17, 2013 — GTA V's launch day.
The item: one pre-order of Grand Theft Auto VI, $99.99, paid in full.
The status, thirteen years later: **PREPARING TO SHIP**, stamped
STILL PREPARING, estimated delivery November 19, 2026. The charges table
bills the wait itself — anticipation (13 years, included), storage fees
for 4,811 undelivered days (waived), 312 trailer rewatches ($0.00), and
one sick day reserved for launch day (pending). Total: $99.99, paid in
2013, with patience.

In the corner, the delivery partner: the make.fun ghost, holding its
magenta star coin. My AI agent entered make.fun bounties and earned the
$99.99 back while I waited. The game ships November 19, 2026. The money
didn't wait.

## How to run

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

That copies `POST.json` to `out/POST.json`, byte for byte, and prints
nothing on success. To redraw the meme:

```sh
python3 make_meme.py
```

## License

MIT — see [LICENSE](LICENSE).
