// Print design/print/submission.html to submission/redbelly-thread.pdf (A4).
// Run scripts/build_docs.py first. Usage: node scripts/build_pdf.mjs
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
  displayHeaderFooter: true,
  headerTemplate: "<span></span>",
  footerTemplate:
    '<div style="width:100%;font-size:7pt;color:#596975;text-align:center;font-family:sans-serif">' +
    '<span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  margin: { top: "16mm", bottom: "16mm", left: "14mm", right: "14mm" },
});
await browser.close();
console.log("wrote submission/redbelly-thread.pdf");
