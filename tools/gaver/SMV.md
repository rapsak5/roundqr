# SMV'er: arbejdsgang

Ark: "Round QR gaver: SMV'er", Google Sheet id 1knsUtV74gEGoQrjiOrMPOf1Az1eZldD1RJWVEIJHeuw (Drive-mappen Round QR).
Arket blev oprettet 13. nov. 2026 med sin egen struktur (ikke en kopi af modtagerarket). Fanerne Proces og Overblik forklarer faserne.
Faner med data: "Sjælland og Lolland" (København, Nordsjælland, resten af Sjælland, Lolland-Falster og Møn) og "Fyn" (Fyn og øerne).
Bornholm har ingen fane endnu. Opret fanen "Bornholm" som kopi af "Fyn" (duplicateSheet, ryd datarækker), når de første bornholmske virksomheder findes.

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
Som kommunerne, tilpasset en virksomhed: kort, venligt, ikke sælgende, gaven i centrum. Emne "En lille gave til <Navn>: QR-koder i jeres farver".

## Status
13. nov. 2026, hold 1: Herslev Bryghus, Dragsholm Slot, EBK Huse, Tvedemose, Knuthenborg, Faaborg Værft, Egeskov og Ordbogen
har side og mailudkast. Fravalgt: Ingeniørfirmaet J&P (logo kun 85 px) og Krenkerup Gods (intet logo på siden).
Kandidater til næste hold: Søby Værft (Ærø, fondsejet), Lyngkilde (Næstved, siden blokerede automatisk læsning), Hotel Nørrevang (Falster).
