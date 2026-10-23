// Z oficiálneho cvičného testu MV SR (data5.js, 100 testov) vytiahne pre A2 otázky všetky tri odpovede.
// Použitie: node data/extrahuj_minv.js <cesta k data5.js>
const fs=require('fs');
const data=new Function(fs.readFileSync(process.argv[2],'utf8')+';return data')();
global.window={}; require('../public/questions.js'); const A=window.QDATA.qs;
const N=s=>s.normalize('NFC').toLowerCase().replace(/[^a-z0-9áäčďéíĺľňóôŕšťúýž]/g,'');
const byKey=new Map();
for(const t of data[0]) for(const k of Object.keys(t.otazky)){
  const q=t.otazky[k][0], o=t.odpovede[k].map(a=>a.odpoved.trim()), c=q.platna-1;
  byKey.set(N(q.text)+'|'+N(o[c]), {minv:q.id,o,c});
  byKey.set('*'+N(q.text+o[c]), {minv:q.id,o,c}); // rovnaký text, len inak rozdelený medzi otázku a odpoveď
}
const out={}, chyba=[];
for(const a of A){
  const m=byKey.get(N(a.q)+'|'+N(a.a))||byKey.get('*'+N(a.q+a.a));
  if(m){ const o=[...m.o]; o[m.c]=a.a; out[a.id]={o,c:m.c,minv:m.minv}; } else chyba.push(a.id);
}
fs.writeFileSync(__dirname+'/odpovede_minv.json',JSON.stringify(out,null,0));
console.log('spárované',Object.keys(out).length,'chýba',chyba.length);
