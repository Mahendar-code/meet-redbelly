# Manual screenshots

Two quotes are verified in the page source and in `evidence/snapshots/S02.txt`, but the page could not be captured automatically. The About Us timeline is a scroll-animated carousel that renders these entries blank in a headless browser.

Add one screenshot per quote, named exactly as below, then run `python3 scripts/build_docs.py && python3 scripts/build_site.py && python3 scripts/verify.py`. The PENDING check turns to PASS and the fact check links to the new files.

| File to add | Page | What must be visible |
| --- | --- | --- |
| `S02-Q1.png` | https://redbelly.network/about-us | Timeline entry: 2021, June, "Block8, CSIRO and University of Sydney create Redbelly Network as a joint venture with seed funding" |
| `S02-Q2.png` | https://redbelly.network/about-us | Timeline entry: 2024, November, "Mainnet Launched" |

How to take them: open the page, scroll to "Redbelly Journey", drag or scroll the timeline until the entry is on screen, and screenshot just that entry with its year and month. Include the browser address bar if you can. If any other part of the page shows the banned word, crop it out or cover it.

Both facts are also backed by other sources, so the thread does not depend on these two screenshots: S03-Q5, S07-Q2 and S11-Q3 for the University of Sydney and CSIRO origin, and S11-Q1 and S11-Q2 for the November 2024 launch.
