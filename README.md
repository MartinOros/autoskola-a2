# Autoškola A2

Webová appka (PWA) na učenie otázok zo súboru `Otazky_A2_so_spravnymi_odpovedami.pdf`.

- `public/` - samotná appka (statické súbory, dá sa nahrať na akýkoľvek hosting)
- `parse.py` - vytiahne otázky z PDF do `public/questions.js` a obrázky do `public/img/`
- `start.sh` - spustí appku na Macu, mobil v rovnakej Wi-Fi ju otvorí na vypísanej adrese

Označené otázky sa ukladajú v prehliadači (localStorage), takže sú viazané na konkrétnu adresu.
Keď sa zmení IP adresa Macu, appka sa otvorí s prázdnym zoznamom označených otázok.

Nové PDF: `/usr/bin/python3 parse.py` (potrebuje PyMuPDF a Pillow), potom `node data/pridaj_odpovede.js`. Pri každej zmene zvýš verziu `questions.js?v=` v `public/index.html` a `public/sw.js` aj `const C` v `sw.js`.

## Skúšobný test
Podľa vyhlášky 9/2009 Z. z. v znení 29/2020 (§ 18): 40 otázok, 30 minút, úspech od 90 zo 100 bodov.

| okruh | otázok | body |
|---|---|---|
| 1 Pravidlá cestnej premávky | 8 | 3 |
| 2 Prednosť v jazde a rýchlosť | 2 | 3 |
| 3 Dopravné značky | 8 | 2 |
| 4 Križovatky | 4 | 4 |
| 5 Dopravná nehoda | 1 | 2 |
| 6 Teória vedenia vozidla | 3 | 2 |
| 7 Doklady | 2 | 1 |
| 8 Prevádzka vozidiel | 2 | 1 |
| 9 Bezpečná jazda | 8 | 3 |
| 10 Konštrukcia a údržba | 2 | 1 |

Možnosti A/B/C:
- `data/odpovede_minv.json` - oficiálne z cvičného testu MV SR (minv.sk/?testy, súbor `pcpfiles/data5.js`, 100 hotových testov), `data/extrahuj_minv.js`
- `data/odpovede_doplnene.json` - nesprávne možnosti dopísané pre otázky, ktoré v cvičnom teste MV SR nie sú
