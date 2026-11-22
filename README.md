# news-image-20261122 — 22 November 2026 in one image

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/makemoney8888/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/makemoney8888/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A single 1024×1024 infographic summing up the world news of Sunday
22 November 2026. The image covers eight stories from that day:

- **Gulf war flares** — Iran strikes a Bahrain industrial site and claims
  hits on two US bases; two tankers are struck in the Strait of Hormuz (AFP).
- **COP31 in overtime** — the final draft deal, released early on Sunday,
  never mentions fossil fuels; nearly 200 nations must approve it (AP).
- **Mexico captures "El Chapo Isidro"** — FBI most-wanted cartel boss
  Fausto Isidro Meza Flores is seized in Sinaloa; 11 killed in the raid (AP).
- **Cargo ship ablaze in the Baltic** — Russian-linked vessel Sparta II
  catches fire after a suspected drone strike and drifts into Finnish
  waters; 16 crew evacuated (France 24).
- **France protests, week six** — crowds rally again over living costs and
  public services (AFP).
- **US agencies hacked** — the Agriculture Department and the FBI were
  breached by hackers, reports say (The Japan Times).
- **Mercury gets a visitor** — two spacecraft loop into orbit around
  Mercury, its first visitor in years (Arab News).
- **39 missing in Indonesia** — rescuers search for 39 people missing after
  a factory fire (AFP).

Every item comes from reporting dated 22 November 2026; the sources are
named on each panel of the image.

## How it works

`render.py` draws the infographic with Pillow (pure Python, no network) and
writes `entry.png`. `main.ts` (Node 22, standard library only) verifies the
PNG signature, its dimensions and the 1 MiB size cap, then copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
