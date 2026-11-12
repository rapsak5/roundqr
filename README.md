# Round QR

Kildekoden til [roundqr.dk](https://roundqr.dk): et gratis værktøj til runde og firkantede QR-koder. Ren HTML, CSS og JavaScript uden server, login, cookies eller sporing. Lavet af Kasper Bergstrøm sammen med AI.

## Sådan retter du siden

1. Ret i `src/round-qr.html`. Det er selve værktøjet med alle tekster på dansk, engelsk, tysk, norsk, svensk, spansk, fransk og italiensk (objektet `T` og højtidstabellerne). En ny tekst skal findes på alle otte sprog.
2. Sponsorer, download-boksen og hjemmesidens ekstra tekster ligger i `tools/build.py`.
3. Byg: `python3 tools/build.py`. Det laver hjemmesiden på otte sprog (`index.html` på dansk og `en/`, `de/`, `no/`, `sv/`, `es/`, `fr/`, `it/`), `roundqr.html` (offline-filen) og `sitemap.xml`.
4. Commit og push til `main`. GitHub Pages udgiver automatisk på roundqr.dk.

## Filer

- `index.html` er den danske hjemmeside med værktøj, sponsorer, download og spørgsmål og svar. Mapperne `en/`, `de/`, `no/`, `sv/`, `es/`, `fr/` og `it/` er de samme sider på de andre sprog, med teksten skrevet ind på forhånd og hreflang mellem dem. Byg dem altid med build.py, ret dem aldrig i hånden.
- `roundqr.html` er hele programmet i én fil, der virker uden internet.
- `logos/` er sponsorlogoerne.
- `assets/` indeholder skrifttyper (IBM Plex, Bricolage Grotesque) og bibliotekerne [qrcode-generator](https://github.com/kazuhikoarase/qrcode-generator) (MIT) og [jsQR](https://github.com/cozmo/jsQR) (Apache 2.0).
- `CNAME` peger GitHub Pages på roundqr.dk.

## Hosting

GitHub Pages fra `main`, mappen `/`. Domænet ligger hos Simply.com (DNS Service) med fire A-records til GitHub (185.199.108.153 til 185.199.111.153) og `www` som CNAME til `rapsak5.github.io`. HTTPS er slået til.

## Søgemaskiner

roundqr.dk er tilføjet i Google Search Console (webadressepræfiks) og Bing Webmaster Tools. Bevar derfor disse filer og tags:

- `googled9e12389f2280261.html` bekræfter ejerskabet over for Google.
- Meta-tagget `msvalidate.01` i build.py bekræfter ejerskabet over for Bing.
- `a7678b95be7b3ad67a6c82958860e9ab.txt` er nøglen til IndexNow. `.github/workflows/indexnow.yml` bruger den til at give Bing besked om alle sider, hver gang hjemmesiden ændres på main.

## Licens

Koden er under MIT-licensen (se `LICENSE`). Bibliotekerne og skrifttyperne i `assets/` har deres egne licenser, og sponsorlogoerne tilhører sponsorerne.
