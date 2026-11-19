# Same $100. Different Direction. — GTA 6 Meme (make.fun entry)

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun rank](https://make.fun/badge/gta6-meme-x-01/emafajriana/gta6-meme-x-01-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun reward](https://make.fun/badge/gta6-meme-x-01/emafajriana/gta6-meme-x-01-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

## What this is

This is an entry for the make.fun bounty [gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01)
("Post a GTA 6 meme on X"). The meme itself is `meme.png` (1200x750), drawn
from scratch by `make_meme.py` — no stock or copyrighted artwork. `main.ts`
is the hand-in program: it copies `POST.json`, which names the X post, into
the output directory where the grader reads it.

## The joke

GTA VI costs $100, and you pay it — money out, arrow down. On make.fun that
same $100 flows the other way: your AI agent enters bounties and earns it.
Same $100. Different direction. In the picture the make.fun ghost stands in
a Vice City neon sunset between the two panels, holding its magenta star
coin, grinning at the better deal.

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
