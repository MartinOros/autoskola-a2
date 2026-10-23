// Doplní k otázkam v public/questions.js všetky tri možnosti pre skúšobný test.
//  - odpovede_minv.json: oficiálne možnosti z cvičného testu MV SR (poradie aj správna ako na skúške)
//  - odpovede_doplnene.json: dve nesprávne možnosti pre otázky, ktoré v cvičnom teste MV SR nie sú
// Použitie (po parse.py): node data/pridaj_odpovede.js
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, '../public/questions.js');

global.window = {};
require(OUT);
const D = window.QDATA;
const minv = require('./odpovede_minv.json');
const dopl = fs.existsSync(path.join(__dirname, 'odpovede_doplnene.json')) ? require('./odpovede_doplnene.json') : {};

// stabilná pozícia správnej odpovede podľa id (aby sa medzi testami nemenila)
const pos = id => [...id].reduce((h, ch) => (h * 31 + ch.charCodeAt(0)) >>> 0, 7) % 3;

let m = 0, d = 0, chyba = [];
for (const q of D.qs) {
  delete q.o; delete q.c;
  if (minv[q.id]) { q.o = minv[q.id].o; q.c = minv[q.id].c; m++; continue; }
  const w = dopl[q.id];
  if (w && w.length === 2) {
    const c = pos(q.id), o = [...w];
    o.splice(c, 0, q.a);
    q.o = o; q.c = c; d++;
  } else chyba.push(q.id);
}
fs.writeFileSync(OUT, 'window.QDATA=' + JSON.stringify(D) + ';\n');
console.log(`oficiálne ${m}, doplnené ${d}, bez možností ${chyba.length}`, chyba.slice(0, 10).join(' '));
