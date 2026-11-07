import base64, json, os, re
# Bygger index.html (hjemmesiden) og roundqr.html (offline-filen) ud fra src/round-qr.html.
# Kør fra repo-roden: python3 tools/build.py
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(OUT, 'src', 'round-qr.html')
src = open(SRC, encoding='utf-8').read()

FONTS = [
  ('Bricolage Grotesque', 600, 'bricolage-600.woff2'),
  ('Bricolage Grotesque', 700, 'bricolage-700.woff2'),
  ('IBM Plex Sans', 400, 'plex-sans-400.woff2'),
  ('IBM Plex Sans', 500, 'plex-sans-500.woff2'),
  ('IBM Plex Sans', 600, 'plex-sans-600.woff2'),
  ('IBM Plex Mono', 400, 'plex-mono-400.woff2'),
  ('IBM Plex Mono', 500, 'plex-mono-500.woff2'),
]
LIBS = ['qrcode.js', 'jsQR.js']

def fontface(inline):
    out = []
    for fam, w, name in FONTS:
        if inline:
            url = 'data:font/woff2;base64,' + base64.b64encode(open(os.path.join(OUT, 'assets', 'fonts', name), 'rb').read()).decode()
        else:
            url = 'assets/fonts/' + name
        out.append('@font-face{font-family:"%s";font-style:normal;font-weight:%d;font-display:swap;src:url(%s) format("woff2")}' % (fam, w, url))
    return '\n'.join(out)

# ---------- strip artifact-only head bits ----------
body = src
body = re.sub(r'<title>.*?</title>\n', '', body, count=1)
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
body = re.sub(r'<link rel="preconnect"[^>]*>\n', '', body)
body = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n', '', body)
assert 'fonts.googleapis' not in body

RESET = ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}'

# ---------- strings for the new sections ----------
DA = {
 'spTitle': 'Sponsorer',
 'spIntro': 'Round QR er gratis og uden reklamer. Tak til dem, der støtter siden.',
 'sp1': 'Praktiske workshops og kurser i AI for medarbejdere, ledere og undervisere. Fra første prompt til faste arbejdsgange i hverdagen.',
 'sp2': 'Video, podcast og livestreaming af events. Klippekort, faste pakker eller en workshop, hvor I lærer at producere selv.',
 'sp3': 'Tidsregistrering med NFC. Et klistermærke ved døren stempler dig ind og ud, og den gratis app holder styr på timer og flex.',
 'sp4': 'Et nyt dansk forlag med bøger om naturen og de gode oplevelser i den, for både børn og voksne.',
 'sp5': 'Cider fra England, Irland, Frankrig, Danmark og USA. Med og uden alkohol, og flere af dem er økologiske.',
 'sp6': 'En konference om AI i arbejdslivet for den enkelte, teamet og organisationen. 11. februar 2027 i Dansk Arkitektur Center.',
 'sp7': 'Hjælper medicinalvirksomheder med at tage AI i brug på en ansvarlig måde med mennesket i centrum. Rådgivning, coaching og workshops.',
 'dlTitle': 'Hent Round QR',
 'dlText': 'Hele programmet i én HTML-fil. Åbn den i din browser og lav QR-koder, også uden internet. Der er intet at installere.',
 'dlBtn': 'Hent roundqr.html',
 'footNote': 'Ingen cookies og ingen sporing. Dine indstillinger gemmes kun i din egen browser.',
}
EN = {
 'spTitle': 'Sponsors',
 'spIntro': 'Round QR is free and has no ads. Thanks to the companies that support it.',
 'sp1': 'Hands-on AI workshops and courses for staff, managers and teachers. From the first prompt to routines that stick.',
 'sp2': 'Video, podcasts and livestreaming of events. Clip cards, fixed packages or a workshop where you learn to produce it yourself.',
 'sp3': 'Time tracking with NFC. A sticker by the door clocks you in and out, and the free app keeps track of your hours and balance.',
 'sp4': 'A new Danish publisher of books about nature and the good experiences it offers, for children and adults.',
 'sp5': 'Cider from England, Ireland, France, Denmark and the USA. With and without alcohol, and several are organic.',
 'sp6': 'A conference on AI at work for individuals, teams and organisations. 11 February 2027 at the Danish Architecture Centre.',
 'sp7': 'Helps pharmaceutical companies adopt AI responsibly, with people at the centre. Consulting, coaching and workshops.',
 'dlTitle': 'Download Round QR',
 'dlText': 'The whole program in one HTML file. Open it in your browser and make QR codes, even offline. Nothing to install.',
 'dlBtn': 'Download roundqr.html',
 'footNote': 'No cookies and no tracking. Your settings are only stored in your own browser.',
}
# Tysk, norsk og svensk til sponsorer, download-boksen og bunden.
SITE_LANGS = {
 "de": {
  "spTitle": "Sponsoren",
  "spIntro": "Round QR ist kostenlos und werbefrei. Danke an alle, die die Seite unterstützen.",
  "sp1": "Praxisnahe Workshops und Kurse zu KI für Mitarbeitende, Führungskräfte und Lehrende. Vom ersten Prompt bis zu festen Abläufen im Alltag.",
  "sp2": "Video, Podcast und Livestreaming von Events. Zehnerkarten, feste Pakete oder ein Workshop, in dem ihr lernt, selbst zu produzieren.",
  "sp3": "Zeiterfassung mit NFC. Ein Aufkleber an der Tür stempelt dich ein und aus, und die kostenlose App behält Stunden und Gleitzeit im Blick.",
  "sp4": "Ein neuer dänischer Verlag mit Büchern über die Natur und die schönen Erlebnisse darin, für Kinder und Erwachsene.",
  "sp5": "Cider aus England, Irland, Frankreich, Dänemark und den USA. Mit und ohne Alkohol, und mehrere davon sind Bio.",
  "sp6": "Eine Konferenz über KI im Arbeitsleben für den Einzelnen, das Team und die Organisation. 11. Februar 2027 im Dansk Arkitektur Center.",
  "sp7": "Hilft Pharmaunternehmen, KI verantwortungsvoll und mit dem Menschen im Mittelpunkt einzuführen. Beratung, Coaching und Workshops.",
  "dlTitle": "Round QR herunterladen",
  "dlText": "Das ganze Programm in einer HTML-Datei. Öffne sie im Browser und erstelle QR-Codes, auch ohne Internet. Es muss nichts installiert werden.",
  "dlBtn": "roundqr.html herunterladen",
  "footNote": "Keine Cookies und kein Tracking. Deine Einstellungen werden nur in deinem eigenen Browser gespeichert."
 },
 "no": {
  "spTitle": "Sponsorer",
  "spIntro": "Round QR er gratis og uten reklame. Takk til dem som støtter siden.",
  "sp1": "Praktiske workshops og kurs i KI for ansatte, ledere og undervisere. Fra første prompt til faste arbeidsrutiner i hverdagen.",
  "sp2": "Video, podkast og livestreaming av arrangementer. Klippekort, faste pakker eller en workshop der dere lærer å produsere selv.",
  "sp3": "Timeregistrering med NFC. Et klistremerke ved døra stempler deg inn og ut, og den gratis appen holder styr på timer og fleks.",
  "sp4": "Et nytt dansk forlag med bøker om naturen og de gode opplevelsene i den, for både barn og voksne.",
  "sp5": "Cider fra England, Irland, Frankrike, Danmark og USA. Med og uten alkohol, og flere av dem er økologiske.",
  "sp6": "En konferanse om KI i arbeidslivet for den enkelte, teamet og organisasjonen. 11. februar 2027 i Dansk Arkitektur Center.",
  "sp7": "Hjelper legemiddelselskaper med å ta i bruk KI på en ansvarlig måte med mennesket i sentrum. Rådgivning, coaching og workshops.",
  "dlTitle": "Last ned Round QR",
  "dlText": "Hele programmet i én HTML-fil. Åpne den i nettleseren og lag QR-koder, også uten internett. Det er ingenting å installere.",
  "dlBtn": "Last ned roundqr.html",
  "footNote": "Ingen informasjonskapsler og ingen sporing. Innstillingene dine lagres bare i din egen nettleser."
 },
 "es": {
  "spTitle": "Patrocinadores",
  "spIntro": "Round QR es gratis y sin anuncios. Gracias a quienes apoyan la página.",
  "sp1": "Talleres y cursos prácticos de IA para empleados, directivos y docentes. Del primer prompt a rutinas fijas en el día a día.",
  "sp2": "Vídeo, pódcast y retransmisión en directo de eventos. Bonos de horas, paquetes fijos o un taller para aprender a producir por vuestra cuenta.",
  "sp3": "Control horario con NFC. Una pegatina junto a la puerta registra tu entrada y salida, y la app gratuita lleva la cuenta de horas y saldo.",
  "sp4": "Una nueva editorial danesa con libros sobre la naturaleza y las buenas experiencias que ofrece, para niños y adultos.",
  "sp5": "Sidra de Inglaterra, Irlanda, Francia, Dinamarca y Estados Unidos. Con y sin alcohol, y varias son ecológicas.",
  "sp6": "Una conferencia sobre IA en el trabajo para la persona, el equipo y la organización. 11 de febrero de 2027 en el Dansk Arkitektur Center.",
  "sp7": "Ayuda a empresas farmacéuticas a adoptar la IA de forma responsable y con las personas en el centro. Consultoría, coaching y talleres.",
  "dlTitle": "Descarga Round QR",
  "dlText": "Todo el programa en un solo archivo HTML. Ábrelo en tu navegador y crea códigos QR, también sin internet. No hay nada que instalar.",
  "dlBtn": "Descargar roundqr.html",
  "footNote": "Sin cookies y sin rastreo. Tus ajustes solo se guardan en tu propio navegador."
 },
 "fr": {
  "spTitle": "Sponsors",
  "spIntro": "Round QR est gratuit et sans publicité. Merci à ceux qui soutiennent le site.",
  "sp1": "Ateliers et formations pratiques sur l'IA pour les salariés, les managers et les enseignants. Du premier prompt aux habitudes de travail au quotidien.",
  "sp2": "Vidéo, podcast et diffusion en direct d'événements. Forfaits d'heures, offres fixes ou un atelier pour apprendre à produire vous-mêmes.",
  "sp3": "Pointage avec NFC. Un autocollant près de la porte enregistre vos arrivées et départs, et l'application gratuite suit vos heures et votre solde.",
  "sp4": "Une nouvelle maison d'édition danoise avec des livres sur la nature et les beaux moments qu'elle offre, pour les enfants et les adultes.",
  "sp5": "Du cidre d'Angleterre, d'Irlande, de France, du Danemark et des États-Unis. Avec et sans alcool, et plusieurs sont bio.",
  "sp6": "Une conférence sur l'IA au travail pour l'individu, l'équipe et l'organisation. Le 11 février 2027 au Dansk Arkitektur Center.",
  "sp7": "Aide les entreprises pharmaceutiques à adopter l'IA de façon responsable, en plaçant l'humain au centre. Conseil, coaching et ateliers.",
  "dlTitle": "Télécharger Round QR",
  "dlText": "Tout le programme dans un seul fichier HTML. Ouvrez-le dans votre navigateur et créez des codes QR, même sans internet. Rien à installer.",
  "dlBtn": "Télécharger roundqr.html",
  "footNote": "Pas de cookies et pas de suivi. Vos réglages sont enregistrés uniquement dans votre propre navigateur."
 },
 "sv": {
  "spTitle": "Sponsorer",
  "spIntro": "Round QR är gratis och utan reklam. Tack till dem som stöttar sidan.",
  "sp1": "Praktiska workshoppar och kurser i AI för medarbetare, chefer och lärare. Från första prompten till fasta arbetssätt i vardagen.",
  "sp2": "Video, podd och livestreaming av evenemang. Klippkort, fasta paket eller en workshop där ni lär er att producera själva.",
  "sp3": "Tidrapportering med NFC. Ett klistermärke vid dörren stämplar in och ut dig, och den kostnadsfria appen håller koll på timmar och flex.",
  "sp4": "Ett nytt danskt förlag med böcker om naturen och de fina upplevelserna i den, för både barn och vuxna.",
  "sp5": "Cider från England, Irland, Frankrike, Danmark och USA. Med och utan alkohol, och flera av dem är ekologiska.",
  "sp6": "En konferens om AI i arbetslivet för individen, teamet och organisationen. 11 februari 2027 på Dansk Arkitektur Center.",
  "sp7": "Hjälper läkemedelsföretag att börja använda AI på ett ansvarsfullt sätt med människan i centrum. Rådgivning, coachning och workshoppar.",
  "dlTitle": "Ladda ner Round QR",
  "dlText": "Hela programmet i en HTML-fil. Öppna den i webbläsaren och skapa QR-koder, även utan internet. Inget att installera.",
  "dlBtn": "Ladda ner roundqr.html",
  "footNote": "Inga kakor och ingen spårning. Dina inställningar sparas bara i din egen webbläsare."
 }
}


# ---------- FAQ (spørgsmål og svar nederst på hjemmesiden) ----------
FAQ_N = 6
FAQ = {
 'da': {
  'faqTitle': 'Spørgsmål og svar',
  'faqIntro': 'Det, folk oftest spørger om.',
  'faq1q': 'Må jeg bruge QR-koderne kommercielt?',
  'faq1a': 'Ja. Brug dem på emballage, skilte, menukort, visitkort, plakater og alt det andet. Du skal ikke betale, spørge om lov eller nævne Round QR.',
  'faq2q': 'Udløber QR-koderne?',
  'faq2a': 'Nej. Det er statiske koder, hvor linket står direkte i selve mønsteret. Der er ingen mellemled, viderestilling eller konto, der kan lukke ned. Koden virker, så længe siden, den peger på, findes.',
  'faq3q': 'Kan en rund QR-kode scannes?',
  'faq3a': 'Ja. Den runde form er pynt rundt om en helt almindelig QR-kode, som alle telefoner kan læse. Round QR scanner selv koden og viser "Kan scannes", når den er i orden. Prøv den alligevel med din egen telefon, før du sender noget til tryk.',
  'faq4q': 'Hvad koster det?',
  'faq4a': 'Ingenting. Der kommer aldrig abonnement, login eller reklamer. Siden betales af sponsorerne ovenfor.',
  'faq5q': 'Gemmer I mine links eller billeder?',
  'faq5a': 'Nej. Alt sker i din egen browser, og intet sendes til en server. Der er ingen cookies og ingen sporing.',
  'faq6q': 'Er Round QR åben?',
  'faq6a': 'Ja. Hele kildekoden ligger offentligt på GitHub, og du kan hente programmet som én HTML-fil og bruge det uden internet.',
 },
 'en': {
  'faqTitle': 'Questions and answers',
  'faqIntro': 'The things people ask most.',
  'faq1q': 'Can I use the QR codes commercially?',
  'faq1a': "Yes. Use them on packaging, signs, menus, business cards, posters and anything else. You don't need to pay, ask permission or mention Round QR.",
  'faq2q': 'Do the QR codes expire?',
  'faq2a': "No. They are static codes, so the link is stored directly in the pattern itself. There's no redirect service or account in between that can shut down. The code works as long as the page it points to exists.",
  'faq3q': 'Can a round QR code be scanned?',
  'faq3a': 'Yes. The round shape is decoration around a completely normal QR code that every phone can read. Round QR scans the code itself and shows "Scans correctly" when it is fine. Still, test it with your own phone before you send anything to print.',
  'faq4q': 'What does it cost?',
  'faq4a': 'Nothing. There will never be subscriptions, logins or ads. The site is paid for by the sponsors above.',
  'faq5q': 'Do you store my links or images?',
  'faq5a': 'No. Everything happens in your own browser and nothing is sent to a server. No cookies and no tracking.',
  'faq6q': 'Is Round QR open?',
  'faq6a': 'Yes. All the source code is public on GitHub, and you can download the whole program as one HTML file and use it offline.',
 },
 'de': {
  'faqTitle': 'Fragen und Antworten',
  'faqIntro': 'Was am häufigsten gefragt wird.',
  'faq1q': 'Darf ich die QR-Codes kommerziell nutzen?',
  'faq1a': 'Ja. Auf Verpackungen, Schildern, Speisekarten, Visitenkarten, Plakaten und überall sonst. Du musst nichts bezahlen, nicht um Erlaubnis fragen und Round QR nicht nennen.',
  'faq2q': 'Laufen die QR-Codes ab?',
  'faq2a': 'Nein. Es sind statische Codes, der Link steht direkt im Muster selbst. Es gibt keinen Weiterleitungsdienst und kein Konto dazwischen, das abgeschaltet werden kann. Der Code funktioniert, solange die Seite existiert, auf die er zeigt.',
  'faq3q': 'Lässt sich ein runder QR-Code scannen?',
  'faq3a': 'Ja. Die runde Form ist Schmuck um einen ganz normalen QR-Code, den jedes Handy lesen kann. Round QR scannt den Code selbst und zeigt "Lässt sich scannen", wenn alles passt. Teste ihn trotzdem mit deinem eigenen Handy, bevor du etwas drucken lässt.',
  'faq4q': 'Was kostet es?',
  'faq4a': 'Nichts. Es wird nie ein Abo, einen Login oder Werbung geben. Die Seite wird von den Sponsoren oben bezahlt.',
  'faq5q': 'Speichert ihr meine Links oder Bilder?',
  'faq5a': 'Nein. Alles passiert in deinem eigenen Browser, und nichts wird an einen Server geschickt. Keine Cookies und kein Tracking.',
  'faq6q': 'Ist Round QR offen?',
  'faq6a': 'Ja. Der gesamte Quellcode liegt öffentlich auf GitHub, und du kannst das ganze Programm als eine HTML-Datei herunterladen und ohne Internet nutzen.',
 },
 'no': {
  'faqTitle': 'Spørsmål og svar',
  'faqIntro': 'Det folk spør oftest om.',
  'faq1q': 'Kan jeg bruke QR-kodene kommersielt?',
  'faq1a': 'Ja. Bruk dem på emballasje, skilt, menyer, visittkort, plakater og alt annet. Du trenger ikke betale, spørre om lov eller nevne Round QR.',
  'faq2q': 'Utløper QR-kodene?',
  'faq2a': 'Nei. Det er statiske koder der lenken står direkte i selve mønsteret. Det finnes ingen mellomledd, videresending eller konto som kan legges ned. Koden virker så lenge siden den peker til, finnes.',
  'faq3q': 'Kan en rund QR-kode skannes?',
  'faq3a': 'Ja. Den runde formen er pynt rundt en helt vanlig QR-kode som alle telefoner kan lese. Round QR skanner koden selv og viser "Kan skannes" når den er i orden. Test den likevel med din egen telefon før du sender noe til trykk.',
  'faq4q': 'Hva koster det?',
  'faq4a': 'Ingenting. Det kommer aldri abonnement, innlogging eller reklame. Siden betales av sponsorene over.',
  'faq5q': 'Lagrer dere lenkene eller bildene mine?',
  'faq5a': 'Nei. Alt skjer i din egen nettleser, og ingenting sendes til en server. Ingen informasjonskapsler og ingen sporing.',
  'faq6q': 'Er Round QR åpen?',
  'faq6a': 'Ja. All kildekoden ligger offentlig på GitHub, og du kan laste ned hele programmet som én HTML-fil og bruke det uten internett.',
 },
 'es': {
  'faqTitle': 'Preguntas y respuestas',
  'faqIntro': 'Lo que más se pregunta.',
  'faq1q': '¿Puedo usar los códigos QR con fines comerciales?',
  'faq1a': 'Sí. Úsalos en envases, carteles, cartas de restaurante, tarjetas de visita, pósteres y todo lo demás. No tienes que pagar, pedir permiso ni mencionar Round QR.',
  'faq2q': '¿Caducan los códigos QR?',
  'faq2a': 'No. Son códigos estáticos, en los que el enlace va directamente en el propio patrón. No hay intermediarios, redirecciones ni cuentas que puedan cerrarse. El código funciona mientras exista la página a la que apunta.',
  'faq3q': '¿Se puede escanear un código QR redondo?',
  'faq3a': 'Sí. La forma redonda es decoración alrededor de un código QR normal que cualquier móvil puede leer. Round QR escanea el código por sí mismo y muestra "Se puede escanear" cuando está bien. Aun así, pruébalo con tu móvil antes de mandar algo a imprimir.',
  'faq4q': '¿Cuánto cuesta?',
  'faq4a': 'Nada. Nunca habrá suscripciones, registros ni anuncios. La página la pagan los patrocinadores de arriba.',
  'faq5q': '¿Guardáis mis enlaces o imágenes?',
  'faq5a': 'No. Todo ocurre en tu propio navegador y no se envía nada a ningún servidor. Sin cookies y sin rastreo.',
  'faq6q': '¿Round QR es abierto?',
  'faq6a': 'Sí. Todo el código fuente es público en GitHub, y puedes descargar el programa completo como un único archivo HTML y usarlo sin internet.',
 },
 'fr': {
  'faqTitle': 'Questions et réponses',
  'faqIntro': 'Ce que l\'on nous demande le plus souvent.',
  'faq1q': 'Puis-je utiliser les codes QR à des fins commerciales ?',
  'faq1a': 'Oui. Utilisez-les sur des emballages, des panneaux, des menus, des cartes de visite, des affiches et tout le reste. Vous n\'avez rien à payer, aucune autorisation à demander et pas besoin de citer Round QR.',
  'faq2q': 'Les codes QR expirent-ils ?',
  'faq2a': 'Non. Ce sont des codes statiques : le lien est inscrit directement dans le motif. Il n\'y a ni intermédiaire, ni redirection, ni compte qui puisse fermer. Le code fonctionne tant que la page vers laquelle il pointe existe.',
  'faq3q': 'Un code QR rond peut-il être scanné ?',
  'faq3a': 'Oui. La forme ronde est une décoration autour d\'un code QR tout à fait normal que tous les téléphones savent lire. Round QR scanne lui-même le code et affiche "Se scanne bien" quand tout est en ordre. Testez-le quand même avec votre téléphone avant d\'imprimer.',
  'faq4q': 'Combien ça coûte ?',
  'faq4a': 'Rien. Il n\'y aura jamais d\'abonnement, de compte ni de publicité. Le site est financé par les sponsors ci-dessus.',
  'faq5q': 'Conservez-vous mes liens ou mes images ?',
  'faq5a': 'Non. Tout se passe dans votre propre navigateur et rien n\'est envoyé à un serveur. Pas de cookies et pas de suivi.',
  'faq6q': 'Round QR est-il ouvert ?',
  'faq6a': 'Oui. Tout le code source est public sur GitHub, et vous pouvez télécharger tout le programme sous forme d\'un seul fichier HTML et l\'utiliser sans internet.',
 },
 'sv': {
  'faqTitle': 'Frågor och svar',
  'faqIntro': 'Det folk oftast frågar om.',
  'faq1q': 'Får jag använda QR-koderna kommersiellt?',
  'faq1a': 'Ja. Använd dem på förpackningar, skyltar, menyer, visitkort, affischer och allt annat. Du behöver inte betala, be om lov eller nämna Round QR.',
  'faq2q': 'Slutar QR-koderna att fungera?',
  'faq2a': 'Nej. Det är statiska koder där länken står direkt i själva mönstret. Det finns ingen mellanhand, vidarebefordran eller konto som kan stängas ner. Koden fungerar så länge sidan den pekar på finns.',
  'faq3q': 'Går en rund QR-kod att skanna?',
  'faq3a': 'Ja. Den runda formen är dekoration runt en helt vanlig QR-kod som alla telefoner kan läsa. Round QR skannar koden själv och visar "Kan skannas" när den är i ordning. Testa den ändå med din egen telefon innan du skickar något till tryck.',
  'faq4q': 'Vad kostar det?',
  'faq4a': 'Ingenting. Det kommer aldrig någon prenumeration, inloggning eller reklam. Sidan betalas av sponsorerna ovan.',
  'faq5q': 'Sparar ni mina länkar eller bilder?',
  'faq5a': 'Nej. Allt sker i din egen webbläsare och ingenting skickas till en server. Inga kakor och ingen spårning.',
  'faq6q': 'Är Round QR öppen?',
  'faq6a': 'Ja. All källkod ligger öppet på GitHub, och du kan ladda ner hela programmet som en HTML-fil och använda det utan internet.',
 },
}
DA.update(FAQ['da']); EN.update(FAQ['en'])
for _lg in ('de', 'no', 'sv', 'es', 'fr'): SITE_LANGS[_lg].update(FAQ[_lg])
GITHUB = 'https://github.com/rapsak5/roundqr'

def faq_html():
    rows = []
    for i in range(1, FAQ_N + 1):
        link = f' <a href="{GITHUB}">github.com/rapsak5/roundqr</a>' if i == FAQ_N else ''
        q, a = DA[f'faq{i}q'], DA[f'faq{i}a']
        rows.append(f'''      <li><details class="fq">
        <summary data-t="faq{i}q">{q}</summary>
        <p><span data-t="faq{i}a">{a}</span>{link}</p>
      </details></li>''')
    return '\n'.join(rows)

def js_obj(d):
    import json
    return ''.join('      %s: %s,\n' % (k, json.dumps(v, ensure_ascii=False)) for k, v in d.items())

SPONSORS = [
  ('AI Workshop', 'ai-workshop.dk', 'https://ai-workshop.dk', 'ai-workshop.png', 'sp1'),
  ('Berg-Streaming', 'berg-streaming.dk', 'https://berg-streaming.dk', 'berg-streaming.png', 'sp2'),
  ('StemplerInd', 'stemplerind.dk', 'https://stemplerind.dk', 'stemplerind.svg', 'sp3'),
  ('Forlaget Uldahl', 'forlagetuldahl.dk', 'https://forlagetuldahl.dk', 'forlaget-uldahl.png', 'sp4'),
  ('Cider Kompagniet', 'ciderkompagniet.dk', 'https://ciderkompagniet.dk', 'ciderkompagniet.png', 'sp5'),
  ('Arbejdsliv.ai', 'arbejdsliv.ai', 'https://arbejdsliv.ai', 'arbejdsliv.svg', 'sp6'),
  ('PharmaConsulting.ai', 'pharmaconsulting.ai', 'https://pharmaconsulting.ai', 'pharmaconsulting.png', 'sp7'),
]

SECTION_CSS = '''
/* Sponsors, download, footer (website only) */
:root { --plate: #ffffff; }
.sponsors { display: grid; grid-template-columns: minmax(0, 280px) minmax(0, 1fr); gap: 20px 48px; align-items: start;
  margin-top: 18px; padding-top: 36px; border-top: 1px solid var(--line); }
@media (max-width: 760px) { .sponsors { grid-template-columns: minmax(0, 1fr); } }
.site-h2 { font-family: var(--font-display); font-weight: 700; font-size: 27px; line-height: 1.1; letter-spacing: -0.015em; margin: 0 0 8px; text-wrap: balance; }
.sp-intro p, .dl-text p { margin: 0; color: var(--muted); max-width: 48ch; }
.sp-list { list-style: none; margin: 0; padding: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; min-width: 0; }
.sp-list li + li { border-top: 1px solid var(--line); }
.sp { display: grid; grid-template-columns: 58px minmax(0, 1fr) auto; gap: 16px; align-items: start; padding: 16px 18px; color: inherit; text-decoration: none; }
.sp:hover { background: var(--bg); }
.sp:focus-visible { outline: 2px solid var(--accent-strong); outline-offset: -3px; border-radius: 12px; }
.sp-logo { width: 58px; height: 58px; border-radius: 13px; background: var(--plate); display: grid; place-items: center; padding: 6px; box-shadow: 0 0 0 1px var(--line); }
.sp-logo img { width: 46px; height: 46px; object-fit: contain; display: block; }
.sp-body { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.sp-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 10px; }
.sp-name { font-weight: 600; font-size: 15.5px; }
.sp-url { font-family: var(--font-mono); font-size: 12.5px; color: var(--accent-strong); }
.sp-text { font-size: 14px; line-height: 1.5; color: var(--muted); max-width: 64ch; }
.sp-arrow { color: var(--muted); font-size: 18px; line-height: 1; align-self: center; }
.sp:hover .sp-arrow { color: var(--accent-strong); }
@media (max-width: 480px) {
  .sp { grid-template-columns: 48px minmax(0, 1fr); gap: 14px; padding: 14px; }
  .sp-logo { width: 48px; height: 48px; border-radius: 11px; padding: 5px; }
  .sp-logo img { width: 38px; height: 38px; }
  .sp-arrow { display: none; }
}
.download { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px 32px;
  padding: 26px 28px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; }
.dl-text { flex: 1 1 320px; min-width: 0; }
.dl-action { display: flex; flex-direction: column; align-items: flex-start; gap: 7px; }
.btn.big { font-size: 15.5px; padding: 12px 20px 12px 16px; border-radius: 10px; text-decoration: none; gap: 9px; }
.btn.big svg { width: 19px; height: 19px; flex: none; }
.faq { display: grid; grid-template-columns: minmax(0, 280px) minmax(0, 1fr); gap: 20px 48px; align-items: start; }
@media (max-width: 760px) { .faq { grid-template-columns: minmax(0, 1fr); } }
.faq-intro p { margin: 0; color: var(--muted); max-width: 48ch; }
.fq-list { list-style: none; margin: 0; padding: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; min-width: 0; }
.fq-list li + li { border-top: 1px solid var(--line); }
.fq summary { list-style: none; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 16px;
  padding: 15px 18px; font-weight: 600; font-size: 15.5px; }
.fq summary::-webkit-details-marker { display: none; }
.fq summary::after { content: "+"; flex: none; font-family: var(--font-mono); font-weight: 500; font-size: 18px; line-height: 1; color: var(--muted); }
.fq[open] summary::after { content: "\\2212"; }
.fq summary:hover { background: var(--bg); }
.fq summary:focus-visible { outline: 2px solid var(--accent-strong); outline-offset: -3px; border-radius: 12px; }
.fq p { margin: 0; padding: 0 18px 16px; font-size: 14.5px; line-height: 1.55; color: var(--muted); max-width: 68ch; }
.fq p a { color: var(--accent-strong); overflow-wrap: anywhere; }
@media (max-width: 480px) { .fq summary { padding: 14px; } .fq p { padding: 0 14px 14px; } }
.foot { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 6px 24px; font-size: 13px; color: var(--muted);
  padding-top: 18px; border-top: 1px solid var(--line); }
.foot a { color: inherit; }
@media (max-width: 480px) { .download { padding: 20px 18px; } }
'''

DL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10.5l5 5 5-5M5 19.5h14"/></svg>'

def sponsor_html():
    rows = []
    for name, host, url, logo, key in SPONSORS:
        rows.append(f'''      <li><a class="sp" href="{url}" target="_blank" rel="noopener">
        <span class="sp-logo"><img src="logos/{logo}" alt="{name} logo" width="46" height="46" loading="lazy" decoding="async"></span>
        <span class="sp-body"><span class="sp-head"><span class="sp-name">{name}</span><span class="sp-url">{host}</span></span>
          <span class="sp-text" data-t="{key}">{DA[key]}</span></span>
        <span class="sp-arrow" aria-hidden="true">&#8599;</span></a></li>''')
    return '\n'.join(rows)

def site_sections(dl_size):
    return f'''
  <section class="sponsors" id="sponsorer" aria-labelledby="sp-h">
    <div class="sp-intro">
      <h2 class="site-h2" id="sp-h" data-t="spTitle">{DA['spTitle']}</h2>
      <p data-t="spIntro">{DA['spIntro']}</p>
    </div>
    <ul class="sp-list">
{sponsor_html()}
    </ul>
  </section>

  <section class="download" id="hent" aria-labelledby="dl-h">
    <div class="dl-text">
      <h2 class="site-h2" id="dl-h" data-t="dlTitle">{DA['dlTitle']}</h2>
      <p data-t="dlText">{DA['dlText']}</p>
    </div>
    <div class="dl-action">
      <a class="btn primary big" href="roundqr.html" download="roundqr.html">{DL_ICON}<span data-t="dlBtn">{DA['dlBtn']}</span></a>
      <span class="spec">HTML · {dl_size}</span>
    </div>
  </section>

  <section class="faq" id="faq" aria-labelledby="faq-h">
    <div class="faq-intro">
      <h2 class="site-h2" id="faq-h" data-t="faqTitle">{DA['faqTitle']}</h2>
      <p data-t="faqIntro">{DA['faqIntro']}</p>
    </div>
    <ul class="fq-list">
{faq_html()}
    </ul>
  </section>

  <footer class="foot">
    <span>Round QR · roundqr.dk</span>
    <span data-t="footNote">{DA['footNote']}</span>
  </footer>
'''

OFFLINE_FOOT = '''
  <footer class="foot" style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 24px;font-size:13px;color:var(--muted);padding-top:18px;border-top:1px solid var(--line)">
    <span>Round QR · <a href="https://roundqr.dk" style="color:inherit">roundqr.dk</a></span>
    <span data-t="footNote"></span>
  </footer>
'''

ANCHORS = {'da': '      subtitle: "Indsæt et link', 'en': '      subtitle: "Paste a link', 'de': '      subtitle: "Link einfügen',
           'no': '      subtitle: "Lim inn en lenke', 'sv': '      subtitle: "Klistra in en länk',
           'es': '      subtitle: "Pega un enlace', 'fr': '      subtitle: "Collez un lien'}
def add_strings(html, per_lang):
    for lg, d in per_lang.items():
        assert html.count(ANCHORS[lg]) == 1, lg
        html = html.replace(ANCHORS[lg], js_obj(d) + ANCHORS[lg], 1)
    return html

def head(title, desc, extra='', html_attrs='lang="da"'):
    return f'''<!doctype html>
<html {html_attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{extra}<style>{RESET}</style>
</head>
<body>
'''

def libs(inline):
    if not inline:
        return '\n'.join('<script src="assets/%s"></script>' % n for n in LIBS)
    out = []
    for n in LIBS:
        code = open(os.path.join(OUT, 'assets', n), encoding='utf-8').read().replace('</script', '<\\/script')
        out.append('<script>\n' + code + '\n</script>')
    return '\n'.join(out)

CDN = '<script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>'
assert CDN in body
END_WRAP = '</div>\n\n' + CDN
assert END_WRAP in body, 'wrap end'
DESC = 'Lav runde eller almindelige QR-koder fra et link. Vælg form, farver og logo, og gem som PNG, JPG eller SVG. Gratis, uden login og uden reklamer.'

# ---------- offline single file ----------
# Højtiderne og temaerne (jul, Halloween, påske, nytår, pirat, Oktoberfest, fødselsdag, skovtur) er kun til hjemmesiden. Download-filen får ingen af tilstandene.
FEST = re.compile(r'(?:<!-- (julelys|halloween|paaske|nytaar|pirat|oktober|foedselsdag|skovtur):start -->|/\* (julelys|halloween|paaske|nytaar|pirat|oktober|foedselsdag|skovtur):start \*/).*?(?:<!-- (?:\1|\2):end -->|/\* (?:\1|\2):end \*/)\n?', re.S)
off = FEST.sub('', body)
assert 'julelys:' not in off and 'id="xbar"' not in off and 'setXmas' not in off
assert 'halloween:' not in off and 'id="hbar"' not in off and 'setHall' not in off and 'HFX' not in off
assert 'paaske:' not in off and 'id="ebar"' not in off and 'setEaster' not in off and 'EFX' not in off
assert 'nytaar:' not in off and 'id="nbar"' not in off and 'setNyt' not in off and 'NFX' not in off
assert 'pirat:' not in off and 'id="pbar"' not in off and 'setPirat' not in off and 'PFX' not in off
assert 'oktober:' not in off and 'id="obar"' not in off and 'setOkt' not in off and 'OFX' not in off
assert 'foedselsdag:' not in off and 'id="bbar"' not in off and 'setBday' not in off and 'BFX' not in off
assert 'skovtur:' not in off and 'id="sbar"' not in off and 'setSkov' not in off and 'SFX' not in off
off = off.replace('<style>\n', '<style>\n' + fontface(True) + '\n', 1)
off = off.replace(END_WRAP, OFFLINE_FOOT + END_WRAP, 1).replace(CDN, libs(True), 1)
off = add_strings(off, {'da': {'footNote': 'Virker uden internet. Ingen cookies og ingen sporing.'}, 'en': {'footNote': 'Works offline. No cookies and no tracking.'},
  'de': {'footNote': 'Funktioniert ohne Internet. Keine Cookies und kein Tracking.'}, 'no': {'footNote': 'Virker uten internett. Ingen informasjonskapsler og ingen sporing.'},
  'sv': {'footNote': 'Fungerar utan internet. Inga kakor och ingen spårning.'},
  'es': {'footNote': 'Funciona sin internet. Sin cookies y sin rastreo.'}, 'fr': {'footNote': 'Fonctionne sans internet. Pas de cookies et pas de suivi.'}})
OFF_DA = 'Jeg har udviklet Round QR sammen med AI, fordi jeg selv manglede et godt værktøj til QR-koder. Den er gratis, uden abonnement, login og reklamer, og virker også uden internet.'
OFF_EN = "I built Round QR together with AI because I needed a good QR code tool myself. It's free, with no subscriptions, logins or ads, and it works offline too."
off = re.sub(r'(      about: )"Jeg har udviklet[^"]*"', lambda m: m.group(1) + '"' + OFF_DA + '"', off)
off = re.sub(r'(      about: )"I built Round QR[^"]*"', lambda m: m.group(1) + '"' + OFF_EN.replace('"', '\\"') + '"', off)
OFF_ABOUT = {
  'Ich habe Round QR': 'Ich habe Round QR zusammen mit KI entwickelt, weil mir selbst ein gutes Werkzeug für QR-Codes fehlte. Es ist kostenlos, ohne Abo, Login und Werbung, und funktioniert auch ohne Internet.',
  'Jeg har utviklet': 'Jeg har utviklet Round QR sammen med KI fordi jeg selv manglet et godt verktøy for QR-koder. Det er gratis, uten abonnement, innlogging og reklame, og virker også uten internett.',
  'Jag har utvecklat': 'Jag har utvecklat Round QR tillsammans med AI eftersom jag själv saknade ett bra verktyg för QR-koder. Det är gratis, utan prenumeration, inloggning och reklam, och fungerar även utan internet.',
  'He creado Round QR': 'He creado Round QR junto con la IA porque yo mismo echaba en falta una buena herramienta para códigos QR. Es gratis, sin suscripciones, registros ni anuncios, y también funciona sin internet.',
  "J'ai créé Round QR": "J'ai créé Round QR avec l'aide de l'IA parce qu'il me manquait un bon outil pour les codes QR. C'est gratuit, sans abonnement, compte ni publicité, et ça fonctionne aussi sans internet.",
}
for start, text in OFF_ABOUT.items():
    off, n = re.subn(r'(      about: )"' + start + r'[^"]*"', lambda m, text=text: m.group(1) + json.dumps(text, ensure_ascii=False), off)
    assert n == 1, start
off = re.sub(r'<span data-t="about">[^<]*</span>', '<span data-t="about">' + OFF_DA + '</span>', off)
off = head('Round QR', DESC, '<link rel="canonical" href="https://roundqr.dk/">\n<link rel="icon" href="data:image/svg+xml;base64,' + base64.b64encode(open(OUT + '/favicon.svg','rb').read()).decode() + '">\n') + off + '\n</body>\n</html>\n'
assert 'cdn.jsdelivr' not in off and 'googleapis' not in off
open(OUT + '/roundqr.html', 'w', encoding='utf-8').write(off)
size = os.path.getsize(OUT + '/roundqr.html')
dl_size = f'{round(size/1024)} KB'

# ---------- website: én side pr. sprog ----------
# / er dansk, de andre sprog ligger i /en/, /de/ osv. Teksten skrives ind i HTML'en på forhånd,
# så Google og AI-søgemaskiner læser siden på det rigtige sprog uden at køre JavaScript.
LANGS = ['da', 'en', 'de', 'no', 'sv', 'es', 'fr']
HTML_LANG = {'da': 'da', 'en': 'en', 'de': 'de', 'no': 'nb', 'sv': 'sv', 'es': 'es', 'fr': 'fr'}
OG_LOCALE = {'da': 'da_DK', 'en': 'en_GB', 'de': 'de_DE', 'no': 'nb_NO', 'sv': 'sv_SE', 'es': 'es_ES', 'fr': 'fr_FR'}
BASE = 'https://roundqr.dk'
def url_of(lg): return BASE + ('/' if lg == 'da' else f'/{lg}/')

PAGE = {
 'da': ('Round QR · Gratis QR-kode generator til runde og firkantede koder', DESC),
 'en': ('Round QR · Free QR code generator for round and square codes',
        'Make round or regular QR codes from a link. Pick shape, colours and logo, and save as PNG, JPG or SVG. Free, no sign-up and no ads.'),
 'de': ('Round QR · Kostenloser QR-Code-Generator für runde und eckige Codes',
        'Erstelle runde oder normale QR-Codes aus einem Link. Wähle Form, Farben und Logo und speichere als PNG, JPG oder SVG. Kostenlos, ohne Anmeldung und ohne Werbung.'),
 'no': ('Round QR · Gratis QR-kodegenerator for runde og firkantede koder',
        'Lag runde eller vanlige QR-koder fra en lenke. Velg form, farger og logo, og lagre som PNG, JPG eller SVG. Gratis, uten innlogging og uten reklame.'),
 'sv': ('Round QR · Gratis QR-kodgenerator för runda och fyrkantiga koder',
        'Skapa runda eller vanliga QR-koder från en länk. Välj form, färger och logga och spara som PNG, JPG eller SVG. Gratis, utan inloggning och utan reklam.'),
 'es': ('Round QR · Generador de códigos QR gratis, redondos y cuadrados',
        'Crea códigos QR redondos o normales a partir de un enlace. Elige forma, colores y logo, y guárdalo como PNG, JPG o SVG. Gratis, sin registro y sin anuncios.'),
 'fr': ('Round QR · Générateur de codes QR gratuit, ronds et carrés',
        "Créez des codes QR ronds ou classiques à partir d'un lien. Choisissez la forme, les couleurs et le logo, puis enregistrez en PNG, JPG ou SVG. Gratuit, sans compte et sans publicité."),
}
FEATURES = {
 'da': ['Runde og firkantede QR-koder', 'Statiske koder der aldrig udløber', 'Egne farver, farveforløb og logo', 'Gem som PNG, JPG eller SVG', 'Virker uden internet', 'Ingen login, cookies eller sporing'],
 'en': ['Round and square QR codes', 'Static codes that never expire', 'Your own colours, gradients and logo', 'Save as PNG, JPG or SVG', 'Works offline', 'No login, cookies or tracking'],
 'de': ['Runde und eckige QR-Codes', 'Statische Codes, die nie ablaufen', 'Eigene Farben, Farbverläufe und Logo', 'Als PNG, JPG oder SVG speichern', 'Funktioniert ohne Internet', 'Kein Login, keine Cookies, kein Tracking'],
 'no': ['Runde og firkantede QR-koder', 'Statiske koder som aldri utløper', 'Egne farger, fargeforløp og logo', 'Lagre som PNG, JPG eller SVG', 'Virker uten internett', 'Ingen innlogging, informasjonskapsler eller sporing'],
 'sv': ['Runda och fyrkantiga QR-koder', 'Statiska koder som aldrig slutar fungera', 'Egna färger, färgövergångar och logga', 'Spara som PNG, JPG eller SVG', 'Fungerar utan internet', 'Ingen inloggning, kakor eller spårning'],
 'es': ['Códigos QR redondos y cuadrados', 'Códigos estáticos que nunca caducan', 'Colores, degradados y logo propios', 'Guardar como PNG, JPG o SVG', 'Funciona sin internet', 'Sin registro, cookies ni rastreo'],
 'fr': ['Codes QR ronds et carrés', 'Codes statiques qui n\'expirent jamais', 'Vos couleurs, dégradés et logo', 'Enregistrer en PNG, JPG ou SVG', 'Fonctionne sans internet', 'Sans compte, cookies ni suivi'],
}
PER_LANG = {'da': DA, 'en': EN}
PER_LANG.update(SITE_LANGS)
for lg in LANGS:
    PER_LANG[lg] = dict(PER_LANG[lg], pageTitle=PAGE[lg][0], pageDesc=PAGE[lg][1])

def tool_strings(html):
    # Læser de enkle tekster (key: "tekst") for hvert sprog ud af værktøjets JavaScript.
    a = html.index('  var T = {'); b = html.index('  var lang = "da", xmas')
    out = {lg: {} for lg in LANGS}; cur = None
    for line in html[a:b].split('\n'):
        m = re.match(r'^\s{3,4}"?(da|en|de|no|sv|es|fr)"?: \{\s*$', line)
        if m: cur = m.group(1); continue
        if cur is None or 'function' in line: continue
        for k, v in re.findall(r'(?:^|[\s{,])"?(\w+)"?: ("(?:[^"\\]|\\.)*")', line):
            out[cur][k] = json.loads(v)
    return out

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def prerender(html, d):
    html = re.sub(r'(<(\w+)[^>]*\sdata-t="(\w+)"[^>]*>)[^<]*(</\2>)', lambda m: (m.group(1) + esc(d[m.group(3)]) + m.group(4)) if isinstance(d.get(m.group(3)), str) else m.group(0), html)
    def aria(m):
        tag = m.group(0); k = re.search(r'data-t-aria="(\w+)"', tag).group(1)
        v = d.get(k)
        return re.sub(r'aria-label="[^"]*"', 'aria-label="' + esc(v).replace('"', '&quot;') + '"', tag) if isinstance(v, str) else tag
    html = re.sub(r'<[^>]*\sdata-t-aria="\w+"[^>]*>', aria, html)
    return html

PREFIX = ['src="assets/', 'src="logos/', 'href="roundqr.html"', 'url(assets/']

site = body.replace('<style>\n', '<style>\n' + fontface(False) + '\n', 1)
site = site.replace('</style>', SECTION_CSS + '</style>', 1)
site = site.replace(END_WRAP, site_sections(dl_size) + END_WRAP, 1).replace(CDN, libs(False), 1)
site = add_strings(site, PER_LANG)
TOOL = tool_strings(site)

# Ejerskab i Bing Webmaster Tools. Google bruger filen googled9e12389f2280261.html i roden,
# og IndexNow-nøglen ligger som a7678b95be7b3ad67a6c82958860e9ab.txt i roden. Slet ingen af dem.
VERIFY = '<meta name="msvalidate.01" content="6FF3944E70AC36E640FBBDFD5BC174A5">\n'
INDEXNOW_KEY = 'a7678b95be7b3ad67a6c82958860e9ab'

def meta(lg):
    title, desc = PAGE[lg]
    alt = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG[x]}" href="{url_of(x)}">\n' for x in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{url_of("en")}">\n'
    ogalt = ''.join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[x]}">\n' for x in LANGS if x != lg)
    d = PER_LANG[lg]
    ld = {
      '@context': 'https://schema.org',
      '@graph': [
        {'@type': 'WebSite', '@id': BASE + '/#website', 'url': BASE + '/', 'name': 'Round QR',
         'alternateName': ['roundqr.dk', 'RoundQR'], 'inLanguage': [HTML_LANG[x] for x in LANGS]},
        {'@type': 'Person', '@id': BASE + '/#kasper', 'name': 'Kasper Bergstrøm', 'url': 'https://ai-workshop.dk'},
        {'@type': 'WebApplication', '@id': url_of(lg) + '#app', 'name': 'Round QR', 'url': url_of(lg),
         'description': desc, 'applicationCategory': 'DesignApplication', 'operatingSystem': 'Any',
         'browserRequirements': 'Requires JavaScript', 'isAccessibleForFree': True, 'inLanguage': HTML_LANG[lg],
         'image': BASE + '/og-image.png', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'},
         'featureList': FEATURES[lg], 'author': {'@id': BASE + '/#kasper'}, 'sameAs': [GITHUB],
         'isPartOf': {'@id': BASE + '/#website'}},
        {'@type': 'FAQPage', '@id': url_of(lg) + '#faq', 'inLanguage': HTML_LANG[lg],
         'mainEntity': [{'@type': 'Question', 'name': d[f'faq{i}q'],
                         'acceptedAnswer': {'@type': 'Answer', 'text': d[f'faq{i}a']}} for i in range(1, FAQ_N + 1)]},
      ],
    }
    pre = '' if lg == 'da' else '../'
    a = lambda t: t.replace('"', '&quot;')
    return (f'<link rel="canonical" href="{url_of(lg)}">\n' + alt + VERIFY +
f'''<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<meta name="theme-color" content="#f5f3ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141310" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:url" content="{url_of(lg)}">
<meta property="og:site_name" content="Round QR">
<meta property="og:title" content="Round QR">
<meta property="og:description" content="{a(desc)}">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{OG_LOCALE[lg]}">
''' + ogalt + '<meta name="twitter:card" content="summary_large_image">\n' +
      '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1).replace('</', '<\\/') + '\n</script>\n')

for lg in LANGS:
    cut = site.index('<script')
    page = prerender(site[:cut], dict(TOOL[lg], **PER_LANG[lg])) + site[cut:]
    page = page.replace('id="lang-da" value="da" checked', 'id="lang-da" value="da"', 1)
    page = page.replace(f'id="lang-{lg}" value="{lg}"', f'id="lang-{lg}" value="{lg}" checked', 1)
    if lg != 'da':
        for p in PREFIX:
            assert p in page, p
            page = page.replace(p, p.replace('"', '"../', 1) if '"' in p else 'url(../' + p[4:])
    title, desc = PAGE[lg]
    page = head(esc(title), desc.replace('"', '&quot;'), meta(lg), f'lang="{HTML_LANG[lg]}" data-page-lang="{lg}"') + page + '\n</body>\n</html>\n'
    assert 'cdn.jsdelivr' not in page and 'googleapis' not in page
    path = OUT + '/index.html' if lg == 'da' else OUT + f'/{lg}/index.html'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(page)

# Sitemap med alle sprog og dagens dato
import datetime
today = datetime.date.today().isoformat()
alts = ''.join(f'    <xhtml:link rel="alternate" hreflang="{HTML_LANG[x]}" href="{url_of(x)}"/>\n' for x in LANGS)
alts += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_of("en")}"/>\n'
urls = ''.join(f'  <url>\n    <loc>{url_of(lg)}</loc>\n    <lastmod>{today}</lastmod>\n{alts}  </url>\n' for lg in LANGS)
open(OUT + '/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n'
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')

print('roundqr.html', dl_size, '| index.html', round(os.path.getsize(OUT + '/index.html')/1024), 'KB')
