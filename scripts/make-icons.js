// Renders the Android launcher icons and splash screens from HTML, using the bundled fonts.
// Usage: node scripts/make-icons.js   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const res = path.join(root, 'android/app/src/main/res');
const font = fs.readFileSync(path.join(root, 'assets/fonts/ArchivoBlack-400.woff2')).toString('base64');
const BG = '#110e2b', GOLD = '#ffc94a', HIT = '#17b890', NEAR = '#ff8a4c', LINE = '#3d377f', EMPTY = '#1d1948';

const base = `<style>@font-face{font-family:A;src:url(data:font/woff2;base64,${font})}
html,body{margin:0;width:100%;height:100%}body{display:grid;place-items:center;font-family:A}</style>`;

// The mark: a gold "L" tile with green and orange tiles tucked behind it. `s` is the art box in px.
const mark = s => `<div style="position:relative;width:${s}px;height:${s}px">
  <div style="position:absolute;right:0;top:0;width:${s * .42}px;height:${s * .42}px;border-radius:${s * .09}px;background:${HIT}"></div>
  <div style="position:absolute;right:0;bottom:0;width:${s * .42}px;height:${s * .42}px;border-radius:${s * .09}px;background:${NEAR}"></div>
  <div style="position:absolute;left:0;top:${s * .08}px;width:${s * .74}px;height:${s * .84}px;border-radius:${s * .14}px;background:${GOLD};box-shadow:0 0 0 ${s * .045}px ${BG};display:grid;place-items:center;color:#2a1d00;font-size:${s * .62}px;line-height:1">L</div>
</div>`;

const dens = { mdpi: 1, hdpi: 1.5, xhdpi: 2, xxhdpi: 3, xxxhdpi: 4 };

(async () => {
  const b = await chromium.launch();
  const shot = async (html, w, h, file, transparent) => {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(base + html);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: file, omitBackground: !!transparent });
    await p.close();
  };
  for (const [d, k] of Object.entries(dens)) {
    const dir = path.join(res, 'mipmap-' + d);
    const fg = 108 * k, ic = 48 * k;
    // adaptive foreground: art kept inside the 66dp safe zone
    await shot(`<body style="background:transparent">${mark(fg * 0.5)}`, fg, fg, path.join(dir, 'ic_launcher_foreground.png'), true);
    await shot(`<body style="background:transparent"><div style="width:${ic}px;height:${ic}px;border-radius:${ic * .2}px;background:${BG};display:grid;place-items:center">${mark(ic * .62)}</div>`, ic, ic, path.join(dir, 'ic_launcher.png'), true);
    await shot(`<body style="background:transparent"><div style="width:${ic}px;height:${ic}px;border-radius:50%;background:${BG};display:grid;place-items:center">${mark(ic * .56)}</div>`, ic, ic, path.join(dir, 'ic_launcher_round.png'), true);
  }
  // splash screens (Android 11 and below; Android 12+ shows the launcher icon on the background color)
  const word = (t) => [...'LETTERLOCK'].map((c, i) => {
    const bg = i === 0 ? GOLD : [1, 4, 6, 9].includes(i) ? HIT : [3, 8].includes(i) ? NEAR : EMPTY;
    return `<b style="width:${t}px;height:${t}px;display:grid;place-items:center;border-radius:${t * .16}px;background:${bg};${bg === EMPTY ? `border:${t * .05}px solid ${LINE};box-sizing:border-box;` : ''}color:${i === 0 ? '#2a1d00' : '#fff'};font-size:${t * .55}px;font-weight:400">${c}</b>`;
  }).join('');
  const splashes = fs.readdirSync(res).filter(f => fs.existsSync(path.join(res, f, 'splash.png')));
  for (const dir of splashes) {
    const f = path.join(res, dir, 'splash.png');
    const buf = fs.readFileSync(f);
    const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
    const t = Math.min(w, h) * 0.075;
    await shot(`<body style="background:${BG}"><div style="display:flex;flex-direction:column;align-items:center;gap:${t * .9}px">${mark(t * 3.2)}<div style="display:flex;gap:${t * .12}px">${word(t)}</div></div>`, w, h, f);
  }
  fs.writeFileSync(path.join(res, 'values/ic_launcher_background.xml'),
    `<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">${BG}</color>\n</resources>\n`);
  await b.close();
  console.log('icons + splash written');
})();
