// Print design/print/submission.html to submission/redbelly-thread.pdf (A4).
// Run scripts/build_docs.py first. Usage: node scripts/build_pdf.mjs
//
// No header or footer: Chromium renders those on their own, without the page's
// web fonts, and falls back to a system font the brand kit does not allow.
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(join(ROOT, "design/print/submission.html")).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.pdf({
  path: join(ROOT, "submission/redbelly-thread.pdf"),
  format: "A4",
  printBackground: true,
  preferCSSPageSize: true,
});
await browser.close();
console.log("wrote submission/redbelly-thread.pdf");
