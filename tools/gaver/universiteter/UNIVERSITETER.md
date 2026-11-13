# Udenlandske universiteter

Ark: Google Sheet "Round QR gaver: udenlandske universiteter", id 1vGXIi_LoNVBTCo-De0wEid6ZTrYULI2uXjy5YMeEnNg (ligger i Drive-mappen Round QR).
Rækker 2 til 45, slug i kolonne I. Alle 44 har mailadresse. Q er status, V er næste skridt, X er noter om logo.

Rækkefølge for hvert universitet: 1) mailadresse, 2) design (logo og farver), 3) byg siden. Byg først, når både mail og design findes.

## Design
Logo og farver aflæses i Chrome (se KOMMUNER.md). Logoerne ligger i universiteter/logos/<slug>.png, farver og sprog i universiteter/brands.json.
Hvide logoer: sæt overlay-baggrunden til sidens mørke farve og brug logos.py --bg HEX, så pladen beholdes.
Færdige designs (26): Skotland 5, Irland 7, Wales 4, England 6, Lund, Uppsala, Stockholm, KTH.
Mangler design: Chalmers, Göteborg, Linköping, Umeå, UiO, UiB, NTNU, UiT, NMBU, OsloMet, Hamburg, TUHH, Kiel, Lübeck, Flensburg, Bremen, Hannover, Rostock.

## Sprog
Siderne er på engelsk plus det lokale sprog: Skotland gd, Irland ga, Wales cy, England kun en, Sverige sv, Norge nb og nn, Tyskland de.
Kun de målrettede universitetssider får de lokale sprog. src/round-qr.html og den almindelige roundqr.dk må ikke ændres for det.
build_brand.py er i dag kun dansk og fjerner sprogvælgeren. Den skal udvides med feltet "languages" i brands.json og sprogfiler i tools/gaver/sprog/<kode>.json.
Lav en sprogfil først, når det første universitet med mail, design og det sprog skal bygges. sv, no og de findes allerede i værktøjets T-objekt og kan genbruges; nynorsk, gælisk, irsk og walisisk skal skrives. Skriv i Noter, at gd, ga og cy bør tjekkes af en modersmålstaler.
Test at de danske sider (kommuner, NGO, fagforeninger) bygger uændret efter udvidelsen.

## Byg
SITE=1 python3 tools/build_brand.py tools/gaver/universiteter/brands.json /tmp/ud <slug ...>, kopier til <slug>/index.html, noindex, test med check.py (390 px uden vandret scroll og QR-koden kan scannes; check.py skal kunne læse scan-pillen på andre sprog end dansk).
Opdater arket: J "ja", Q "Klar til afsendelse", V "Godkend mailen", X logo-noter (fx lav opløsning).
Mails er på engelsk og nævner University of Glasgow og 5 af 8 danske universiteter.
