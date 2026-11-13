> STOP 13. november 2026: alle gavesider er taget ned på Kaspers ordre. Udgiv og byg ingen sider. Læs tools/gaver/STOP.md først.

# Mærker i midten af QR-koden

Regel: i midten af Kvadrat og Rund står kun et mærke: et symbol, et våbenskjold, et segl eller en forkortelse (fx ITU, KP, SDU).
Aldrig et fuldt logo med navn i tekst. Det fulde logo bruges i brandbjælken og i skabelonerne Bred og Banner, og under koden i Rund, når midten er tom.
Har organisationen kun et tekstlogo uden symbol (fx Horsens, Herning, Klimarådet, og kommuner hvor byvåbnet kræver tilladelse), er midten tom ("none"). Kasper har besluttet det 13. nov. 2026.

Filer:
- tools/gaver/marks/<id>.png: mærket. Gennemsigtig baggrund, beskåret tæt. Plader (fx ITU, Amnesty, Mariagerfjord) har runde hjørner.
- tools/gaver/mark.py: sætter mærket i en færdig side eller gavefil (mark.py SIDE.html MAERKE.png | none). Kan køres igen.
- build_brand.py kalder mark.py, når brands.json har "mark_file": "tools/gaver/marks/<id>.png" eller "none".
- tools/gaver/marks/kilde: scripts brugt til at skære mærkerne ud af logoerne (spec.py siger hvordan for hver side).

Størrelse: logoSize 34 (skyderen går til 36). Runde mærker (tomme hjørner) fylder hele den hvide cirkel, andre lægges så diagonalen rammer cirklen.
Test: alle sider gav "Kan scannes" og blev læst af ZXing i alle fire skabeloner (13. nov. 2026).

Nye sider: lav mærket, før siden bygges, og sæt mark_file i brands.json. Kig på mærket i 100 px: kan man se, hvad det er?
