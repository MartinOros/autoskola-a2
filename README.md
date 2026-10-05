# Autoškola A2

Webová appka (PWA) na učenie otázok zo súboru `Otazky_A2_so_spravnymi_odpovedami.pdf`.

- `public/` - samotná appka (statické súbory, dá sa nahrať na akýkoľvek hosting)
- `parse.py` - vytiahne otázky z PDF do `public/questions.js` a obrázky do `public/img/`
- `start.sh` - spustí appku na Macu, mobil v rovnakej Wi-Fi ju otvorí na vypísanej adrese

Označené otázky sa ukladajú v prehliadači (localStorage), takže sú viazané na konkrétnu adresu.
Keď sa zmení IP adresa Macu, appka sa otvorí s prázdnym zoznamom označených otázok.

Nové PDF: `python3 parse.py` (potrebuje PyMuPDF a Pillow).
