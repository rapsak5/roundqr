> STOP 13. november 2026: alle gavesider er taget ned på Kaspers ordre. Udgiv og byg ingen sider. Læs tools/gaver/STOP.md først.

# Kommunesider: arbejdsgang

Ark: "Round QR gaver: kommuner" (Google Sheet id 1dp5YI8l3cj6fnA18chCDMeDt3hYmv6j5hz6kPGVQuPU), fanen Modtagere.
Kolonner: A Kanal (Kommunikation, Politik, Arrangement, Generel, Tidligere kunde), B Organisation, C Modtagere, D Hilsen,
E Rolle, F Til, G Cc, H Varm kontakt, I Side, J Side klar, K Vinkel, L Egen tekst, M Emne (formel), N Mailtekst (formel),
O Godkendt, P Kladde oprettet, Q Status, R Sendt dato, S og T formler, U Svar, V Næste skridt, W Opkald aftalt, X Noter,
Y Kilde, Z Region, AA Hjemmeside, AB Logo og farver. Skriv aldrig i M, N, S eller T. Arkets locale er da_DK.
Rækkenummer pr. kommune står i kommuner/kommuner.json.

1. Mailadresser: WebSearch med allowed_domains = kommunens domæne og ordene "pressekontakt kommunikation", derefter WebFetch
   af pressesiden. Kun adresser, der står på siden. Vælg kanal efter adressen: kommunikation/presse = Kommunikation,
   borgmester/byråd/politik = Politik, kultur/fritid/borgerinddragelse = Arrangement, kun hovedpostkasse = Generel.
   Hilsen med op til tre fornavne, ellers "Hej". Byg forespørgsler med rowsupd.py og send dem med update_spreadsheet.
2. Logo og farver i Claude i Chrome: åbn forsiden, kør probe.js (javascript_tool), og tag zoom med save_to_disk på
   regionen [16,16,16+bredde,16+højde] fra "shown" (aldrig scale). Hvidt logo: sæt window.__bg='#000' og kør probe igen,
   og brug logos.py --invert HEX. Vælg window.__pick=n, hvis den gættede kandidat er forkert (banner, våbenskjold uden navn).
   Står der, at byvåbnet kræver tilladelse, så brug wordmark.py i stedet for logoet og skriv det i AB.
3. Byg: læg kommunen i kommuner/brands.json (id = slug, colors primary/secondary/accent + text #222222,
   source "aflæst på hjemmesiden", logo_file tools/gaver/kommuner/logos/<slug>.png), og kør
   SITE=1 python3 tools/build_brand.py tools/gaver/kommuner/brands.json /tmp/ud <slug ...> og kopier til <slug>/index.html.
   Hovedfarven skal kunne bære hvid tekst (kontrast mindst 4,5). Ellers brug den mørke farve som primary.
4. Test: python3 tools/gaver/check.py /fuld/sti/*.html (390 px uden vandret scroll, "Kan scannes").
4b. Mærke i midten: se MAERKER.md. Sæt "mark_file" i brands.json.
5. Hent først fra main (git fetch og rebase), commit og push til main. Kasper har godkendt, at kommunesiderne udgives på roundqr.dk. Siderne har noindex og kommer ikke i Google.

Hjælpescripts i tools/gaver/hjaelp (kør fra repo-roden):
- add.py slug "Navn Kommune" hjemmeside primary secondary [accent]: lægger kommunen i brands.json.
- build.sh slug: bygger, kopierer til slug/index.html og tester (scrollW 390, Kan scannes, noindex).
- dom.py billede.png: de mest brugte farver i et logo.
- whitefix.py ind.png ud.png HEX: hvidt logo vist på sort bund; hvid tekst farves HEX, farvede dele beholdes.
Tip: læs mailadresser med javascript_tool (mailto-links og main.textContent) og fjern ?, & og = fra output,
ellers blokerer Chrome-værktøjet svaret. Logo: vis billedet i et hvidt overlay og tag zoom med save_to_disk uden scale.
Status 12. nov. 2026: Alle 98 kommuner har en side og mindst én mailadresse. Opgaven er færdig.
