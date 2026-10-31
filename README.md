# Round QR

Kildekoden til [roundqr.dk](https://roundqr.dk): et gratis værktøj til runde og firkantede QR-koder. Ren HTML, CSS og JavaScript uden server, login, cookies eller sporing. Lavet af Kasper Bergstrøm sammen med AI.

## Sådan retter du siden

1. Ret i `src/round-qr.html`. Det er selve værktøjet med alle tekster på dansk og engelsk (objektet `T`).
2. Sponsorer, download-boksen og hjemmesidens ekstra tekster ligger i `tools/build.py`.
3. Byg: `python3 tools/build.py`. Det laver `index.html` (hjemmesiden) og `roundqr.html` (offline-filen).
4. Commit og push til `main`. GitHub Pages udgiver automatisk på roundqr.dk.

## Filer

- `index.html` er hjemmesiden med værktøj, sponsorer og download.
- `roundqr.html` er hele programmet i én fil, der virker uden internet.
- `logos/` er sponsorlogoerne.
- `assets/` indeholder skrifttyper (IBM Plex, Bricolage Grotesque) og bibliotekerne [qrcode-generator](https://github.com/kazuhikoarase/qrcode-generator) (MIT) og [jsQR](https://github.com/cozmo/jsQR) (Apache 2.0).
- `CNAME` peger GitHub Pages på roundqr.dk.

## Hosting

GitHub Pages fra `main`, mappen `/`. Domænet ligger hos Simply.com (DNS Service) med fire A-records til GitHub (185.199.108.153 til 185.199.111.153) og `www` som CNAME til `rapsak5.github.io`. HTTPS er slået til.
