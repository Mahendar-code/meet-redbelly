# Brand compliance

The entry follows the [Redbelly DAO Task Board brand kit](https://taskboard.redbellydao.network/brand). The kit covers "task graphics, social assets, and contributor deliverables", and the winning thread is posted from the DAO account, so this is the right kit. The tokens file in `site/assets/css/tokens.css` is the kit's own download, unedited.

Redbelly Network's corporate brand (Readex Pro, #FF5050) is a separate identity. The DAO kit says it "is built to sit consistently alongside" that brand and does not replace it. Nothing here is published under the Redbelly Network name.

## Visual rules

| Kit rule | How it is applied | Where |
| --- | --- | --- |
| One accent, #EF5350, never a second | Red is used only for the headline phrase, the label marker and primary buttons. `verify.py` fails if any colour outside the kit's tokens appears | `design/templates/`, `site/assets/css/site.css` |
| Base surface #0c1317, never pure black | Images use the kit's background-deep and surface tokens | all images |
| Accent text on dark is #ffb3ae, on light #B3272A | Small accent text uses the `--primary` token, which switches by theme | site, images |
| White on red only at 14px bold or larger | Primary buttons are 14px, weight 700 | `site.css` `.btn.primary` |
| Be Vietnam Pro for all headings and copy | Self-hosted woff2 files, no Google request at runtime | `site/assets/fonts/` |
| JetBrains Mono only for machine values | Used for post numbers, character counts, quote IDs, URLs, dates. Never for sentences | images, site |
| Body line height 1.5, line length 65 to 75 characters, 16px minimum on mobile | `body` is 16px with 1.5 line height, intros capped at 68ch | `site.css` |
| Logo: light ink on dark, dark ink on light, never on a plate, scale by height | Light-ink `dao-logo-on-dark.png` on the dark and steel backgrounds. The site switches to the dark-ink file in the light theme. Only height is set | images 1 and 9, site header |
| Clear space around the logo | Nothing within the mark's height of the logo | images 1 and 9 |
| Radius 4px base, 8px large, full only for dots | Buttons and chips 4px, cards 8px, status dots round | all |
| Depth is tonal, no heavy shadows | Cards are a lighter slate with a 1px panel-edge border. No drop shadows anywhere. The sticky header uses a 14px backdrop blur, within the 12 to 20px the kit allows | `site.css` |
| Margins 16px mobile, 64px desktop, max width 1280px | `.wrap` uses the kit's spacing tokens | `site.css` |
| Status is a small dot plus a monospace label, not a pill | Used in the fact check, the checks list and the notice bar | site |
| Light theme is the same brand; hero bands stay dark steel | Theme toggle uses the kit's light tokens. The hero band stays #1d3140 in both themes | site |
| X single image post: 1600 x 900, text in a 5% safe margin | All 5 images are 1600 x 900 with at least 80px side and top margins. `verify.py` checks the size | `submission/images/` |
| Open Graph image: 1200 x 630 | `site/assets/img/og-image.png` | site |
| PNG for anything with text, never JPEG | All images are PNG | |
| Deliver exports plus editable source files | Each image has an HTML template in `design/templates/`, rendered by `scripts/render_images.mjs` | |
| Graphics with facts that can expire carry a dated "last verified" line | Every fact image says "Facts last verified 30 October 2026". Image 7 also names its source | images 1, 2, 7, 9 |

## Voice rules

| Kit rule | How it is applied | Checked |
| --- | --- | --- |
| No em dashes or en dashes, anywhere, including commit messages | None in the posts, images, site, documents, code or the commit message in `push-main.sh` | `verify.py` scans every text file |
| No emoji | None anywhere | `verify.py` |
| No filler verbs (the kit names four) | None in anything we wrote | `verify.py` |
| Say the number | Dates are exact ("November 2024", "May 2026", "30 October 2026"), posts are numbered 1/9 to 9/9 | |
| Lead with the answer | Post 1 says what Redbelly is in its second sentence | |
| First person, direct, plain | Short sentences. One idea per post | |
