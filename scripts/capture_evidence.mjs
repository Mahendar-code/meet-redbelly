// Screenshot every quote in content/sources.json on its live page.
//
// For each quote the script opens the source, finds each fragment in the page
// text, draws a highlight box over it, covers any banned term with a solid
// redaction box, and saves a crop around it. A header with the source ID, URL,
// quote ID and capture time is added on top. PDF quotes are first rendered by
// scripts/pdf_evidence.py (run it before this script); this script only adds
// the header to those.
//
// Output: evidence/captures/<quote id>.png and evidence/captures/index.json
// Usage:  python3 scripts/pdf_evidence.py && node scripts/capture_evidence.mjs
import { createRequire } from "node:module";
import { readFileSync, writeFileSync, mkdirSync, existsSync, rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(ROOT, "evidence", "captures");
const RAW = join(ROOT, "evidence", ".raw");
mkdirSync(OUT, { recursive: true });
mkdirSync(RAW, { recursive: true });

const { sources } = JSON.parse(readFileSync(join(ROOT, "content", "sources.json"), "utf8"));
const captured = new Date().toISOString().replace("T", " ").slice(0, 16) + " UTC";
const rev = (s) => s.split("").reverse().join("");
// Same banned patterns as scripts/terms.py, assembled so this file stays clean.
const BANNED = [
  "block[\\s\\-_]*" + rev("niahc"),
  rev("regdel"),
  "\\b" + rev("tld") + "s?\\b",
  "\\b" + rev("niahc") + "s?\\b",
  "\\b(on|off)[\\s\\-]?" + rev("niahc"),
].join("|");

// Runs inside the page: find a fragment, return its client rects in page coordinates.
function locate([fragment, banned]) {
  const norm = (s) =>
    s.normalize("NFKC").replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"')
      .replace(/[\u2012-\u2015]/g, "-").replace(/\u00a0/g, " ");
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const map = [];
  let text = "";
  let lastSpace = true;
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const p = n.parentElement;
    if (!p || ["SCRIPT", "STYLE", "NOSCRIPT"].includes(p.tagName)) continue;
    const v = n.nodeValue;
    // Separate text from different elements, as a reader would see it.
    if (!lastSpace && map.length) { text += " "; map.push(map[map.length - 1]); lastSpace = true; }
    for (let i = 0; i < v.length; i++) {
      // Normalise per character so offsets still point into the raw text node.
      for (const c of norm(v[i])) {
        const ch = /\s/.test(c) ? " " : c;
        if (ch === " " && lastSpace) continue;
        text += ch;
        map.push([n, i]);
        lastSpace = ch === " ";
      }
    }
  }
  const lower = text.toLowerCase();
  const want = norm(fragment).replace(/\s+/g, " ").trim().toLowerCase();
  const rectsFor = (start, end) => {
    const r = document.createRange();
    r.setStart(map[start][0], map[start][1]);
    r.setEnd(map[end - 1][0], map[end - 1][1] + 1);
    return [...r.getClientRects()]
      .filter((q) => q.width > 1 && q.height > 1)
      .map((q) => ({ x: q.left, y: q.top, w: q.width, h: q.height }));
  };
  let from = 0;
  while (true) {
    const at = lower.indexOf(want, from);
    if (at < 0) return null;
    // Bring it into view, including inside sideways-scrolling carousels.
    map[at][0].parentElement.scrollIntoView({ block: "center", inline: "center" });
    const rects = rectsFor(at, at + want.length);
    const vw = document.documentElement.clientWidth;
    const visible = rects.length && rects.every((q) => q.x >= 0 && q.x + q.w <= vw + 1) &&
      getComputedStyle(map[at][0].parentElement).visibility !== "hidden";
    if (visible) {
      const block = map[at][0].parentElement.closest("p,li,div,section,td,article") || map[at][0].parentElement;
      const b = block.getBoundingClientRect();
      const redact = [];
      const rx = new RegExp(banned, "gi");
      for (let m; (m = rx.exec(lower)); ) redact.push(...rectsFor(m.index, m.index + m[0].length));
      return { rects, block: { x: b.left, w: b.width }, redact };
    }
    from = at + 1;
  }
}

function overlay(page, boxes, style) {
  return page.evaluate(([boxes, style]) => {
    for (const b of boxes) {
      const d = document.createElement("div");
      d.setAttribute("data-evidence", "1");
      Object.assign(d.style, {
        position: "fixed", left: b.x - 3 + "px", top: b.y - 2 + "px",
        width: b.w + 6 + "px", height: b.h + 4 + "px", zIndex: 2147483647,
        pointerEvents: "none", boxSizing: "border-box", ...style,
      });
      document.body.appendChild(d);
    }
  }, [boxes, style]);
}

async function htmlShots(page, source, quote) {
  const shots = [];
  for (const [i, frag] of quote.fragments.entries()) {
    let hit = await page.evaluate(locate, [frag, BANNED]);
    if (!hit) {
      // Some pages only render text once it has been scrolled past.
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); }
        scrollTo(0, 0);
      });
      hit = await page.evaluate(locate, [frag, BANNED]);
    }
    if (!hit) throw new Error(`fragment not found on page: "${frag.slice(0, 60)}"`);
    await overlay(page, hit.rects, { border: "3px solid #EF5350", background: "rgba(239,83,80,0.12)" });
    await overlay(page, hit.redact, { background: "#0c1317", border: "0" });
    const ys = hit.rects.map((r) => r.y), ye = hit.rects.map((r) => r.y + r.h);
    const xs = hit.rects.map((r) => r.x), xe = hit.rects.map((r) => r.x + r.w);
    // Clip in viewport coordinates. A full-page screenshot resizes the
    // viewport, which re-lays out scroll-driven pages, so it is avoided.
    const [vw, vh] = await page.evaluate(() => [document.documentElement.clientWidth, innerHeight]);
    const x0 = Math.max(0, Math.min(Math.min(...xs), hit.block.x) - 40);
    const x1 = Math.min(vw, Math.max(Math.max(...xe), hit.block.x + hit.block.w) + 40);
    const y0 = Math.max(0, Math.min(...ys) - 80);
    const y1 = Math.min(vh, Math.max(...ye) + 80);
    const clip = { x: x0, y: y0, width: Math.min(x1 - x0, 1240), height: y1 - y0 };
    const file = join(RAW, `${quote.id}-${i}.png`);
    await page.screenshot({ path: file, clip });
    await page.evaluate(() => document.querySelectorAll("[data-evidence]").forEach((d) => d.remove()));
    shots.push(file);
  }
  return shots;
}

async function compose(page, source, quote, shots) {
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const quoteText = quote.fragments.join(" [...] ");
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face{font-family:"JetBrains Mono";src:url("${pathToFileURL(join(ROOT, "site/assets/fonts/JetBrainsMono-var.woff2")).href}")}
    @font-face{font-family:"Be Vietnam Pro";font-weight:600;src:url("${pathToFileURL(join(ROOT, "site/assets/fonts/BeVietnamPro-600.woff2")).href}")}
    body{margin:0;background:#0c1317;color:#f1f5f8;font-family:"Be Vietnam Pro",sans-serif;width:1300px}
    .h{padding:20px 28px;border-bottom:1px solid #263641;background:#141f26}
    .m{font-family:"JetBrains Mono",monospace;font-size:15px;letter-spacing:.04em;color:#8fa1ad;line-height:1.6}
    .m b{color:#ffb3ae;font-weight:500}
    .q{font-size:17px;line-height:1.5;margin-top:10px;color:#c2ced6}
    .s{padding:24px 28px;display:flex;flex-direction:column;gap:16px}
    .s img{max-width:1244px;border:1px solid #263641;border-radius:4px;background:#fff;display:block}
  </style></head><body><div class="h">
    <div class="m"><b>${source.id} / ${quote.id}</b>${quote.page ? `  PDF page ${quote.page} (printed page ${quote.printed_page})` : ""}</div>
    <div class="m">${esc(source.url)}</div>
    <div class="m">captured ${captured}. Highlight = quoted text. Dark boxes = banned terms redacted.</div>
    <div class="q">"${esc(quoteText)}"</div>
  </div><div class="s">${shots.map((f) => `<img src="${pathToFileURL(f).href}">`).join("")}</div></body></html>`;
  const tmp = join(RAW, `${quote.id}.html`);
  writeFileSync(tmp, html);
  await page.setViewportSize({ width: 1300, height: 800 });
  await page.goto(pathToFileURL(tmp).href);
  await page.evaluate(() => document.fonts.ready);
  const out = join(OUT, `${quote.id}.png`);
  await page.screenshot({ path: out, fullPage: true });
  return out;
}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();
const index = [];
const failures = [];
const manual = [];
for (const s of sources) {
  for (const q of s.quotes) {
    if (q.manual_capture) {
      manual.push({ quote: q.id, source: s.id, url: s.url, reason: q.manual_capture, file: `manual/${q.id}.png` });
      console.log("skip", q.id, "(manual screenshot needed)");
      continue;
    }
    try {
      let shots;
      if (s.type === "pdf") {
        const f = join(RAW, `${q.id}-pdf.png`);
        if (!existsSync(f)) throw new Error("run scripts/pdf_evidence.py first");
        shots = [f];
      } else {
        await page.setViewportSize({ width: 1280, height: 900 });
        await page.goto(s.url, { waitUntil: "networkidle", timeout: 90000 }).catch(() => {});
        await page.addStyleTag({ content: `*{animation:none!important;transition:none!important;scroll-behavior:auto!important}
          [class*="cookie" i],[id*="cookie" i],[class*="consent" i],[id*="consent" i]{display:none!important}
          [style*="opacity: 0"],[style*="opacity:0"],[class*="timeline" i]{opacity:1!important}` });
        shots = await htmlShots(page, s, q);
      }
      const out = await compose(page, s, q, shots);
      index.push({ quote: q.id, source: s.id, url: s.url, file: `captures/${q.id}.png`, captured });
      console.log("ok  ", q.id);
    } catch (e) {
      failures.push({ quote: q.id, source: s.id, url: s.url, error: String(e.message || e) });
      console.log("FAIL", q.id, e.message);
    }
  }
}
await browser.close();
writeFileSync(join(OUT, "index.json"), JSON.stringify({ captured, captures: index, manual, failures }, null, 2) + "\n");
rmSync(RAW, { recursive: true, force: true });
console.log(`${index.length} captured, ${failures.length} failed`);
