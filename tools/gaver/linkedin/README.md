# LinkedIn-brandsider (ja tak)

Folk, der selv har bedt om en QR-generator i eget brand: kommentaren "ja tak" på Kaspers LinkedIn-opslag (14. nov. 2026) eller kontaktformularen nederst på roundqr.dk.
Det er ikke kolde gaver. De har sagt ja, så STOP.md gælder ikke her: siderne må bygges og udgives, når Kasper har givet navn og hjemmeside (besluttet 16. nov. 2026).

Ingen mailadresser eller telefonnumre i dette repo. Det er offentligt.

## Input fra Kasper
Kontaktperson (fornavn), hjemmeside. Gerne også mail og sprog. Uden sprog: kun dansk. Engelsktalende: "languages": ["en", "da"].

## Pr. side
1. Slug: virksomhedens korte navn, små bogstaver uden mellemrum (fx treasurehunts). Tjek at mappen ikke findes. Undtagelse: leeann (den første).
2. Design i Chrome (curl fra sessionen er blokeret): åbn hjemmesiden og kør
   `await eval(await (await fetch('https://roundqr.dk/tools/gaver/p5.js')).text())` med javascript_tool.
   Den giver farver (c), logokandidater (l) og viser logoet i et overlay. Tag zoom med save_to_disk UDEN scale og beskær:
   `python3 tools/gaver/logos.py SKAERM.png tools/gaver/linkedin/logos/<slug>.png` (hvide logoer: `--invert HEX`, logo på plade: `--bg HEX`).
   window.__bg vælger baggrund, window.__pick et andet kandidatlogo.
3. Mærke i midten (MAERKER.md): kun symbol eller forkortelse, skåret ud med `python3 tools/gaver/hjaelp/umark.py SKAERM.png <slug> --crop x0 y0 x1 y1`, som gemmer i `tools/gaver/marks/<slug>.png`. Kun tekstlogo: `"mark_file": "none"`.
4. Farver: kun virksomhedens egne fra siden (primary, secondary, accent, text). Skrift: aflæs font-family; findes den på @fontsource, så `npm i @fontsource/<navn>` i /tmp/fs og sæt fonts_embed.
5. Læg brandet i `brands.json` (se leeann). Tekster i "text" pr. sprog: about (hilsen med fornavn), giftPitch, giftNote ("Lavet til X af Kasper Bergstrøm. Ikke et officielt produkt fra X. Farverne er aflæst på domæne.").
6. Byg og test: `sh tools/gaver/linkedin/ny.sh <slug>`. Kig på skærmbillederne i /home/claude/gaver/test. Krav: scrollW 390, scan True, noindex ok.
7. `git fetch` og rebase, commit "LinkedIn-brandside: <Navn> på roundqr.dk/<slug>", push. Tjek at roundqr.dk/<slug> svarer efter et minut.
8. Mailudkast i Gmail fra kasper@ai-workshop.dk, uden afslutningshilsen (signaturen klarer det). Kort direkte link roundqr.dk/<slug>.

## Mailudkast (dansk)
Emne: Din QR-kodegenerator til <Navn>

Hej <Fornavn>

Tak for dit ja tak på LinkedIn. Her er Round QR i farverne fra <Navn>:
roundqr.dk/<slug>

Vælg en skabelon, ret teksten, og gem koden som PNG, JPG eller SVG. Nederst på siden kan du hente hele generatoren som én fil, der virker uden internet. Intet bliver sendt nogen steder hen.

Er en farve forkert, eller mangler der noget, så skriv bare. Så retter jeg det.

## Mailudkast (engelsk)
Subject: Your QR code generator for <Name>

Hi <First name>

Thanks for your "ja tak" on LinkedIn. Here is Round QR in the colours of <Name>:
roundqr.dk/<slug>

Pick a template, edit the text and save the code as PNG, JPG or SVG. At the bottom of the page you can download the whole generator as one file that works offline. Nothing is sent anywhere.

If a colour is off or something is missing, just let me know and I will fix it.

## Sider
- leeann: Treasure Hunts (treasurehunts.dk), engelsk og dansk, 15. nov. 2026
- connectsport: ConnectSport (connectsport.dk), dansk, 23. nov. 2026
