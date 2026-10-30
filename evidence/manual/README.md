# Manual screenshots

Two quotes come from the "Redbelly Journey" timeline on https://redbelly.network/about-us. The text is in the page source and in `evidence/snapshots/S02.txt`, so `verify.py` checks it like every other quote. The timeline itself is a scroll-animated carousel that renders these entries blank in a headless browser, so the screenshots were taken by hand.

| File | Timeline entry |
| --- | --- |
| `S02-Q1.png` | 2021, June: "Block8, CSIRO and University of Sydney create Redbelly Network as a joint venture with seed funding" |
| `S02-Q2.png` | 2024, November: "Mainnet Launched" |

How they were made: screenshots taken in a desktop browser on 30 October 2026, cropped to the timeline heading and the quoted entry, quoted lines boxed in red, and the same header as the automated captures added on top. Nothing else on the page was changed. Neighbouring entries that contain the banned word are outside the crop, not covered over.

Both facts are also backed by other sources: S03-Q5, S07-Q2 and S11-Q3 for the University of Sydney and CSIRO origin, and S11-Q1 and S11-Q2 for the November 2024 launch.

To replace them: save new screenshots here with the same names, then run `python3 scripts/build_docs.py && python3 scripts/build_site.py && python3 scripts/verify.py`.
