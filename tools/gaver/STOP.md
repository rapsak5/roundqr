# STOP: gavesiderne er taget ned

Kasper bad 13. november 2026 om, at alle gavesider fjernes fra roundqr.dk, mens tilgangen bliver tjekket juridisk (markedsføringsloven, varemærker og ophavsret).

Gælder alle samtaler og planlagte opgaver:
- Udgiv ingen gavesider i roden af repo'et, og læg ingen af de nedtagne tilbage, før Kasper selv siger til i en samtale.
- Byg ingen nye gavesider til udgivelse. Ark og mailadresser må gerne holdes ved lige.
- Kaspers egne brands (aiworkshop, arbejdsliv, bergstreaming, ciderkompagniet, pharmaconsulting, stemplerind, uldahl) og selve roundqr.dk er ikke berørt.

De 342 nedtagne sider står i tools/gaver/nedtagne-sider.txt. HTML'en ligger uændret i commit 1d08ba5 på main (det sidste, før de blev taget ned).
Genudgiv, når Kasper har sagt ja: sh tools/gaver/genudgiv.sh (alle) eller sh tools/gaver/genudgiv.sh dm glasgow (udvalgte), og push.

## Undtagelse: de seks, der har fået mail

HK, DSR, FOA, 3F, Finansforbundet og BUPL fik mail 12. november med link til deres side. De sider ligger online igen, men uden logo: farver og navn er beholdt, og der står en neutral pladsholder med teksten "Jeres logo" i brandbjælken, under koden og i midten af koden.
De er lavet med tools/gaver/uden_logo.py ud fra den gamle side. Læg ikke logoerne tilbage på dem. genudgiv.sh henter de gamle udgaver med logo, så brug den ikke til de seks.
