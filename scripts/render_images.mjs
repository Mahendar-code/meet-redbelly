// Render the thread images from design/templates/*.html to PNG at 1600 x 900.
// Also renders the Open Graph image for the site (1200 x 630).
// Usage: node scripts/render_images.mjs
import { createRequire } from "node:module";
import { readFileSync, copyFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const TPL = join(ROOT, "design", "templates");
const OUT = join(ROOT, "submission", "images");
const SITE = join(ROOT, "site", "assets", "img", "thread");
mkdirSync(OUT, { recursive: true });
mkdirSync(SITE, { recursive: true });

const thread = JSON.parse(readFileSync(join(ROOT, "content", "thread.json"), "utf8"));
const jobs = thread.posts
  .filter((p) => p.image)
  .map((p) => ({ tpl: p.image.template, out: p.image.file, w: 1600, h: 900 }));
jobs.push({ tpl: "og.html", out: "og-image.png", w: 1200, h: 630, siteOnly: true });

const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
for (const j of jobs) {
  await page.setViewportSize({ width: j.w, height: j.h });
  await page.goto(pathToFileURL(join(TPL, j.tpl)).href);
  await page.evaluate(() => document.fonts.ready);
  // Fail loudly if any text overflows the canvas.
  const overflow = await page.evaluate(() => {
    const f = document.querySelector(".frame");
    return f.scrollHeight > f.clientHeight + 1 || f.scrollWidth > f.clientWidth + 1;
  });
  if (overflow) throw new Error(`${j.tpl}: content overflows the ${j.w}x${j.h} frame`);
  const dest = j.siteOnly ? join(ROOT, "site", "assets", "img", j.out) : join(OUT, j.out);
  await page.screenshot({ path: dest, clip: { x: 0, y: 0, width: j.w, height: j.h } });
  if (!j.siteOnly) copyFileSync(dest, join(SITE, j.out));
  console.log("rendered", j.out);
}
await browser.close();
