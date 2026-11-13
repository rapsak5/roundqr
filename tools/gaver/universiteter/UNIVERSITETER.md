# Udenlandske universiteter

Ark: Google Sheet "Round QR gaver: udenlandske universiteter", id 1vGXIi_LoNVBTCo-De0wEid6ZTrYULI2uXjy5YMeEnNg (ligger i Drive-mappen Round QR).
Rækker 2 til 45, slug i kolonne I. Alle 44 har mailadresse. Q er status, V er næste skridt, X er noter om logo.

Rækkefølge for hvert universitet: 1) mailadresse, 2) design (logo og farver), 3) byg siden. Byg først, når både mail og design findes.

## Design
Logo og farver aflæses i Chrome (se KOMMUNER.md). Logoerne ligger i universiteter/logos/<slug>.png, farver og sprog i universiteter/brands.json.
Hvide logoer: sæt overlay-baggrunden til sidens mørke farve og brug logos.py --bg HEX, så pladen beholdes.
Færdige designs (26): Skotland 5, Irland 7, Wales 4, England 6, Lund, Uppsala, Stockholm, KTH. Alle 26 er bygget og udgivet 13. nov. 2026.
Mangler design: Chalmers, Göteborg, Linköping, Umeå, UiO, UiB, NTNU, UiT, NMBU, OsloMet, Hamburg, TUHH, Kiel, Lübeck, Flensburg, Bremen, Hannover, Rostock.

## Sprog
Siderne er på engelsk plus det lokale sprog: Skotland gd, Irland ga, Wales cy, England kun en, Sverige sv, Norge nb og nn, Tyskland de.
Kun de målrettede universitetssider får de lokale sprog. src/round-qr.html og den almindelige roundqr.dk må ikke ændres for det.
build_brand.py har feltet "languages" i brands.json (fx ["en", "gd"]). Det første sprog i listen er standard, men browserens sprog vinder, hvis det er på listen. Sprogvælgeren ligger i brandbjælken.
Sprogfiler: tools/gaver/sprog/<kode>.json med t (nøglen i værktøjets T), name, html (lang-attribut), base (grundsprog for nye sprog, ellers null), ui (værktøjstekster, funktioner skrives som "js:function ...") og gift (sidens egne tekster med {short} og {dom}). Alle gift-nøgler skal findes i hver fil.
Findes: en, sv, gd, ga, cy. Mangler: nb (t "no", base null), nn (t "nn", base "no", fuld ui-oversættelse) og de (t "de", base null). Lav dem, når det første universitet med det sprog skal bygges.
Brands uden "languages" (kommuner, NGO, fagforeninger) bygges byte for byte som før. Det er testet ved at bygge alle kommuner og sammenligne.
gd, ga og cy er skrevet af Claude og bør tjekkes af en modersmålstaler.
Test at de danske sider (kommuner, NGO, fagforeninger) bygger uændret efter udvidelsen.

## Byg
Mærke i midten: kun symbol, våben, segl eller forkortelse (se MAERKER.md). Læg mærket i tools/gaver/marks/<slug>.png og sæt "mark_file" i brands.json, før siden bygges. Tekstlogo uden symbol giver "mark_file": "none". De 26 første har mærker (13. nov.).
SITE=1 python3 tools/build_brand.py tools/gaver/universiteter/brands.json /tmp/ud <slug ...>, kopier til <slug>/index.html, noindex, test med check.py (390 px uden vandret scroll og QR-koden kan scannes; check.py læser pillens klasse ok og tjekker hvert sprog på siden og melder danske ord på ikke-danske sider).
Opdater arket: J "ja", Q "Klar til afsendelse", V "Godkend mailen", X logo-noter (fx lav opløsning).
Mails er på engelsk og nævner University of Glasgow og 5 af 8 danske universiteter.
