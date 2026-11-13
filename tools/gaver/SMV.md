# SMV'er: arbejdsgang

Ark: "Round QR gaver: SMV'er", Google Sheet id 1knsUtV74gEGoQrjiOrMPOf1Az1eZldD1RJWVEIJHeuw (Drive-mappen Round QR).
Arket blev oprettet 13. nov. 2026 med sin egen struktur (ikke en kopi af modtagerarket). Fanerne Proces og Overblik forklarer faserne.
Faner med data: "Sjælland og Lolland" (København, Nordsjælland, resten af Sjælland, Lolland-Falster og Møn) og "Fyn" (Fyn og øerne).
Fanen "Bornholm" (sheetId 4) blev oprettet 13. nov. 2026 som kopi af "Fyn". Overblik tæller ikke Bornholm med (formler, rør dem ikke).

Kolonner (A til AE): Fase, Virksomhed, CVR, By, Område, Branche, Ansatte (ca.), Kilde ansatte, Hjemmeside, Til (mail), Mailtype,
Kilde mail, Telefon, Kontaktperson, Hilsen, Vinkel, Hvorfor relevant, Vurdering, Begrundelse, Logo, Farver, Designnoter,
Godkendt af Kasper (flueben), Side, Side klar, Emne, Mailtekst, Kontaktet dato, Svar, Næste skridt, Noter.
Ingen formler i datarækkerne. Overblik tæller faserne med formler: skriv aldrig i Overblik.

Mål: 50 virksomheder, cirka 20 Sjælland, 15 Fyn, 8 Lolland-Falster og 7 Bornholm. Højst 10 nye rækker pr. kørsel.

## Udvælgelse
Private, selvstændige virksomheder med cirka 20 til 249 ansatte og hovedsæde i regionen. Vidensarbejdere eller udadvendte
(rådgivning, produktion med salg og eksport, fødevarer, bryggerier, turisme, hoteller, attraktioner). Spred over brancher og byer.
Spring over: kæder, datterselskaber af store koncerner, offentlige, fonde og foreninger, organisationer i de andre gaveark,
og virksomheder uden brugbart logo på egen side. Fravalgte skrives i arket med fasen Fravalgt og en begrundelse, så de ikke findes igen.

## Pr. virksomhed
1. Mail: kun adresser på virksomhedens egen side (Kilde mail = siden). Foretræk navngiven direktør, marketing eller kommunikation.
   Læs adresser i Chrome med javascript_tool (mailto-links og body.innerText). Telefon = hovednummeret.
2. Design i Chrome: find logoet (header img/svg), vis det i et hvidt overlay (position fixed, padding 20) og tag zoom med save_to_disk
   UDEN scale. Hvide logoer: sort overlay og logos.py --invert HEX. SVG uden viewBox: sæt viewBox til width/height. SVG med
   class h-full: fjern class og sæt højde. Skjul cookie-bannere uden at klikke (fjern #CybotCookiebotDialog m.fl.).
   Mærke i midten: kun symbol eller forkortelse (umark.py --crop), ellers "none" (se MAERKER.md).
3. Byg: læg virksomheden i tools/gaver/smv/brands.json (logo i smv/logos/<slug>.png, mærke i marks/<slug>.png) og kør
   SITE=1 python3 tools/build_brand.py tools/gaver/smv/brands.json /tmp/ud <slug ...>, kopier til <slug>/index.html,
   test med check.py og tjek noindex. Navne der ender på s får "genitive" (fx "Herslev Bryghus'").
4. Arket: Fase "4 Til godkendelse", Side, Side klar "ja", Emne og Mailtekst. Kasper sætter flueben i Godkendt af Kasper,
   før der tages kontakt. Proces-fanen nævner markedsføringslovens § 10: ring gerne først og spørg, om I må sende en mail.

## Mailudkast
Som kommunerne, tilpasset en virksomhed: kort, venligt, ikke sælgende, gaven i centrum. Emne "En QR-kodegenerator til <Navn>" (som kommunerne). Afsnittet om kommunikationsfolk er taget ud.

## Status
13. nov. 2026, hold 1: Herslev Bryghus, Dragsholm Slot, EBK Huse, Tvedemose, Knuthenborg, Faaborg Værft, Egeskov og Ordbogen
har side og mailudkast. Fravalgt: Ingeniørfirmaet J&P (logo kun 85 px) og Krenkerup Gods (intet logo på siden).
13. nov. 2026, hold 2: Kjærstrup, Svaneke Chokoladeri, Svaneke Bryghus (Bornholm), Søby Værft (Ærø), DanuCare, K.J. Elektro (Lolland-Falster)
og Lyngkilde (Næstved) har side og mailudkast. Fravalgt: Johannes Dam & Søn (siden under vedligehold), Ortofon (kapitalfondsejet), Hotel Nørrevang (siden åbner ikke).
Optalt: Sjælland 5 af 20, Fyn 4 af 15, Lolland-Falster 3 af 8, Bornholm 3 af 7 (15 af 50).
Bornholm og Lolland-Falster har få virksomheder over 20 ansatte; her er 10 til 20 ansatte taget med og markeret "Måske".
Tip: firmaapi.dk/virksomhed/<cvr> giver ansatte, ejere og ledelse. businesslf.dk har lister over nominerede Lolland-Falster-virksomheder.
13. nov. 2026, hold 3: En anden proces (research-agenter) har lagt mange kandidater i arket med fasen "4 Til godkendelse", mail, vinkel og designnoter,
men uden side. Hold 3 byggede sider og mailudkast for 10 af dem: DreistStorgaard, Skel.dk, Frederiksminde, Addere, Norsyn, Mølbak, Kragerup (Sjælland),
GeoCenter Møns Klint (Møn), Hotel Falster og Friis Andersen (Lolland-Falster). Fasen er ikke ændret; Kasper sætter flueben i Godkendt af Kasper.
Række 25 (Lyngkilde) er en dublet af række 13. Optalt med side: Sjælland 13 af 20, Fyn 4 af 15, Lolland-Falster 5 af 8, Bornholm 3 af 7 (25 af 50).
Næste hold: Fyn-fanen har 10 kandidater uden side (C & W, Kielberg, OBH, Hesselet, Falsled Kro, Fjelsted Skov, Praksis, Hotel Faaborg Fjord,
Hindsgavl, Focus Advokater). Derefter resten af Sjælland (Unibio, J&P række 37, Strunge, Rødvig Kro m.fl.). Bornholm mangler 4 nye.
Logoer: logo-URL'er står ofte i Designnoter. Åbn siden i Chrome og kør
await eval(await (await fetch('https://roundqr.dk/tools/gaver/p2.js')).text()) (window.__bg for hvide logoer, window.__pick for et andet kandidatlogo).
Kan siden ikke åbnes, så åbn logo-URL'en direkte og sæt body-baggrunden med javascript_tool. curl fra sessionen er blokeret.
Kandidater til næste hold: Bornholms Tidende (fondsejet), Hotel Griffen, Sjælland og Fyn mangler flest.
13. nov. 2026, hold 4 (session ..ZqpZEf, Kasper har bedt om 80 til 150 virksomheder og godkendt, at alle ventende får side):
sider bygget for de 33 resterende kandidater i fase 4: Coffee Collective, ADEPT, NORD, JJW, EFFEKT, Lund Elmer Sandager, ABC, Ingholt,
Mikkeller, Unibio, Strunge, Advokatfirmaet Svendsen, Ringsted Festival, Rødvig Kro, J&P (jogp), Vejrø, Copenhagen Economics, Wissenberg,
Lundgaard & Tranberg (lt), Bakken, Mazanti-Andersen, GoBoat, NOKC (Sjælland) og alle 10 på Fyn (cw, kielberg, obh, hesselet, falsled,
fjelstedskov, hindsgavl, focus, faaborgfjord, praksis). Byg dem ikke igen. Samme session finder nu nye virksomheder (også Trekantsområdet)
og skriver dem i arket med side. Andre sessioner: tjek kolonnen Side, før I bygger.
