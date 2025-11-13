# Demo Website Creation Workflow

## 🎯 ZIEL: Überzeugende Demo, die zum Kauf führt

**KRITISCH:** Die Demo muss sich anfühlen, als wäre sie NUR für dieses spezifische Unternehmen erstellt worden. Keine generischen Platzhalter-Websites!

## Automatischer Workflow für neue Demo-Websites

Wenn der User nur eine URL angibt, folge diesem Workflow:

### 1. Website-Informationen sammeln & analysieren
```
- Nutze WebFetch auf die angegebene URL
- Extrahiere ALLES: Firmenname, Services, Kontaktdaten, Öffnungszeiten, USPs, Besonderheiten
- Notiere die Branche (z.B. Bäckerei, Anwalt, Autoersatzteile, etc.)
- WICHTIG: Finde die EINZIGARTIGEN Merkmale dieses Unternehmens:
  * Was macht sie anders?
  * Welche spezifischen Services bieten sie?
  * Gibt es besondere Zertifikate, Partner, Auszeichnungen?
  * Welche Sprache/Tonalität nutzt die aktuelle Website?
```

### 2. Neue Demo-Website erstellen
```
- Erstelle einen neuen Ordner in demos/ mit dem Firmen-/Projektnamen (z.B. demos/autoteile-zurich/)
- Kopiere die Struktur eines bestehenden Demos oder erstelle neue Astro-Projekt-Struktur:
  demos/demo-name/
  ├── src/
  │   ├── components/
  │   ├── layouts/
  │   ├── pages/
  │   └── styles/
  ├── public/
  ├── package.json
  ├── astro.config.mjs
  ├── tsconfig.json
  └── vercel.json
```

### 3. 4-seitige Website generieren

**REGEL: JEDE SEITE BRAUCHT EINEN HERO MIT BILD!**

#### Seite 1: Home (index.astro)
- ✅ **Hero mit Background-Bild** (PFLICHT!)
  * Titel: Firmenname oder Slogan (spezifisch, nicht "Willkommen")
  * Untertitel: USP des Unternehmens (aus WebFetch)
  * CTA-Button zu /kontakt
- Services-Sektion mit 6 Dienstleistungen (spezifisch für das Unternehmen!)
- 3 ImageCards mit KONKRETEN Benefits (nicht generisch "Qualität", sondern z.B. "20 Jahre Erfahrung in Zürich")
- Footer mit AI-Chat

#### Seite 2: Leistungen/Services
- ✅ **Hero mit Background-Bild** (PFLICHT!)
  * Titel: "Unsere Leistungen" oder besser: branchenspezifisch
  * Untertitel: Kurze Zusammenfassung
- Alle Services DETAILLIERT (keine Standardtexte!)
- 4-6 Produktkategorien mit Bildern (spezifisch für diese Firma)
- CTA zur Kontaktseite mit überzeugendem Text
- Footer mit AI-Chat

#### Seite 3: Über uns
- ✅ **Hero mit Background-Bild** (PFLICHT!)
  * Titel: "Über [Firmenname]"
  * Untertitel: Mission/Vision Statement
- Firmengeschichte/Beschreibung mit großem Bild
- 3 Team/Service/Lager ImageCards (spezifisch!)
- Werte-Sektion (individuell, nicht Standard-Werte)
- Öffnungszeiten
- Footer mit AI-Chat

#### Seite 4: Kontakt
- ✅ **Hero mit Background-Bild** (PFLICHT!)
  * Titel: "Kontaktieren Sie uns" oder persönlicher
  * Untertitel: Einladend, spezifisch
- Kontaktformular mit branchenspezifischen Feldern
- Kontaktdaten mit Icons
- Öffnungszeiten prominent
- Karten-Platzhalter mit echter Adresse
- Footer mit AI-Chat

### 4. Navigation anpassen
```
- currentPage prop für aktive Seite setzen
- Firmenname, Telefon übergeben
```

### 5. Bilder strategisch auswählen
**Wichtig: Keine Copyright-geschützten Bilder!**

**ALLE 4 HERO SECTIONS BRAUCHEN BILDER!**

Nutze Unsplash mit sehr spezifischen Suchbegriffen:
- Format: `https://images.unsplash.com/photo-{id}?w={width}&h={height}&fit=crop`
- Typische Größen:
  - **Hero: w=1200&h=600** (IMMER mit Bild!)
  - ImageCard: w=800&h=600
  - Kleine Cards: w=600&h=400

**Beispiel-Suchanfragen nach Branche (SPEZIFISCH!):**
- Bäckerei:
  * Hero Home: "artisan bakery", "fresh bread oven"
  * Hero Produkte: "pastry display", "bakery showcase"
  * Hero Über uns: "baker working", "bakery team"
  * Hero Kontakt: "cozy bakery interior", "welcoming bakery"

- Anwalt:
  * Hero Home: "modern law office", "legal consultation"
  * Hero Leistungen: "lawyer meeting client", "courtroom"
  * Hero Über uns: "professional law team", "law library"
  * Hero Kontakt: "office building exterior", "modern office"

- Autoersatzteile:
  * Hero Home: "car parts workshop", "automotive parts"
  * Hero Leistungen: "car mechanic parts", "auto parts shelf"
  * Hero Über uns: "auto parts warehouse", "car workshop team"
  * Hero Kontakt: "auto service center", "car parts store"

- Restaurant:
  * Hero Home: "restaurant interior ambiance", "fine dining"
  * Hero Menü: "chef preparing food", "gourmet dishes"
  * Hero Über uns: "restaurant kitchen", "chef team"
  * Hero Kontakt: "restaurant entrance", "cozy restaurant"

**WICHTIG: Bilder müssen zur Stimmung und Qualität des Unternehmens passen!**
- Luxus-Restaurant → hochwertige Food-Fotografie
- Handwerksbetrieb → authentische Werkstatt-Bilder
- Anwaltskanzlei → professionelle Office-Bilder

### 6. Komponenten verwenden

**Verfügbare Komponenten:**
- `<Navigation>` - Sticky Navigation mit Logo und Links
- `<Hero>` - Hero-Section mit Background-Bild
- `<Services>` - Grid mit Service-Cards
- `<ImageCard>` - Bild-Karte mit Titel und Beschreibung
- `<OpeningHours>` - Öffnungszeiten-Tabelle
- `<Contact>` - Kontaktformular und -informationen
- `<Footer>` - Footer mit Copyright
- `<AIChat>` - Interaktiver AI-Chat Widget (immer einbinden!)

**AI Chat Konfiguration:**
```astro
<AIChat
  businessType="auto-parts"  // 'auto-parts' | 'bakery' | 'lawyer' | 'restaurant' | 'default'
  companyName="Auto Teile Zürich AG"
  phone="044 455 33 11"
  mapsUrl="https://maps.google.com/..."  // Optional: Google Maps Link (User fragen!)
/>
```

**WICHTIG:** Für Google Maps Links oder andere externe URLs → **IMMER den User fragen!**
Niemals selbst URLs generieren oder raten.

**Features des AI Chats:**
- ✅ Vordefinierte Quick-Reply Buttons (kein freies Textfeld!)
- ✅ Business-spezifische Optionen je nach Branche
- ✅ Führt zu Kontaktformular mit branchenspezifischen Feldern
- ✅ Zeigt Öffnungszeiten, Anfahrt etc.
- ✅ Direct Call-to-Action (Telefon anrufen)

**Business Types:**
- `auto-parts`: Ersatzteil suchen, Angebot anfragen, Öffnungszeiten, Anfahrt
- `bakery`: Torte bestellen, Produktsortiment, Öffnungszeiten, Kontakt
- `lawyer`: Beratung anfragen, Fachgebiete, Termin vereinbaren
- `restaurant`: Tisch reservieren, Menü ansehen, Öffnungszeiten
- `default`: Angebot anfragen, Öffnungszeiten, Kontakt

### 7. Farbschema anpassen
Standard: Blau (blue-600)

Für verschiedene Branchen:
- Bäckerei: orange-600 / amber-600
- Anwalt: slate-700 / gray-800
- Autoersatzteile: blue-600
- Restaurant: red-600 / rose-600
- Handwerker: yellow-600 / amber-700
- Zahnarzt: teal-600 / cyan-600

Ersetze in Navigation, Hero, Buttons: `bg-blue-600` → `bg-{color}-600`

### 7.5. Emojis & Icons - Branchen-gerecht verwenden!

**KRITISCH: Nicht jede Zielgruppe mag Emojis!**

**Zielgruppen-Analyse:**

**Ältere Zielgruppe (50+):**
- ❌ **KEINE bunten/poppy Emojis** (🎉 🚀 💯)
- ⚠️ **Minimal oder gar keine** Emojis in Services
- ✅ Nur **funktionale Icons** erlaubt (📞 📍 wenn überhaupt)
- Beispiele: Autoersatzteile, Rechtsanwälte, Ärzte, Steuerberater

**Junge Zielgruppe (18-35):**
- ✅ Emojis ok, aber **nicht übertreiben**
- ✅ Moderne Icons/Emojis passen (🍰 🥖 ☕ 🎨)
- Beispiele: Cafés, Bäckerei, Fitness, Mode

**Branchen-spezifisch:**

**KEINE Emojis (professionell/älter):**
- Anwälte, Steuerberater, Notare
- Finanzdienstleister, Versicherungen
- Ärzte, Zahnärzte, Apotheken
- Autoersatzteile (ältere Autobesitzer)
- Immobilienmakler (Luxussegment)

**Moderate/funktionale Emojis nur:**
- Handwerker (🔧 nur wenn nötig)
- Autoersatzteile (besser ohne)
- Restaurants (gehobene Küche)

**Emojis ok:**
- Bäckerei, Café (🥖 🍰 ☕)
- Kindertagesstätten (🎨 🎈)
- Fitnessstudios (jung)
- Casual Restaurants

**Regel:**
- **Ältere Zielgruppe → KEINE poppy Emojis!**
- B2B / seriöse Branchen → **KEINE Emojis**
- B2C / lockere Branchen → Emojis sparsam nutzen
- AI Chat: Für ältere Zielgruppen → **nur funktionale Icons** (📞 📍) oder ganz ohne

**Beispiel - Services ohne Emojis (Anwalt):**
```js
const services = [
  {
    title: "Vertragsrecht",
    description: "Professionelle Beratung...",
    // KEIN icon!
  }
];
```

**Beispiel - Services mit Emojis (Bäckerei):**
```js
const services = [
  {
    title: "Frische Brötchen",
    description: "Täglich...",
    icon: "🥖"  // OK für Bäckerei
  }
];
```

### 8. Inhalte generieren (NICHT GENERISCH!)

**KRITISCH: Website muss sich individuell anfühlen!**

#### Texte schreiben:
- ✅ Verwende IMMER echte Infos von der Website (WebFetch)
- ✅ Firmenname überall verwenden, nicht "wir" oder "das Unternehmen"
- ✅ Konkrete Details einbauen:
  * Standort erwähnen ("in Zürich", "am Bahnhof", etc.)
  * Spezifische Services benennen (nicht "Beratung", sondern "Steuerberatung für KMU")
  * Echte Marken/Partner nennen (wenn auf Website erwähnt)
  * Konkrete Zahlen ("über 20 Jahre", "500+ zufriedene Kunden")

#### Service-Beschreibungen:
- ❌ NICHT: "Wir bieten professionelle Beratung"
- ✅ SONDERN: "Auto Teile Zürich berät Sie bei der Auswahl von Ersatzteilen für Ihren BMW, VW oder Mercedes"

#### Headlines/Titles:
- ❌ NICHT: "Willkommen auf unserer Website"
- ✅ SONDERN: "Hochwertige Autoersatzteile in Zürich seit 2003"

#### CTAs (Call to Actions):
- ❌ NICHT: "Kontaktieren Sie uns"
- ✅ SONDERN: "Jetzt Angebot für Ihr Fahrzeug anfragen"

#### Regeln:
- **Nie erfundene Kontaktdaten!** Nur echte verwenden
- Texte: 100-150 Wörter pro Sektion, überzeugend, konkret
- Tonalität an Branche anpassen (Anwalt = seriös, Bäckerei = warm/einladend)
- SEO-Keywords natürlich einbauen (Standort + Branche)

### 9. Testing
```bash
cd demos/demo-name
npm install     # Dependencies installieren (beim ersten Mal)
npm run build   # Prüfen ob alles kompiliert
npm run dev     # Dev-Server starten
```

### 10. Deployment zu Vercel
```bash
cd demos/demo-name
npx vercel --prod --yes                          # Erstmalig deployen
npx vercel alias <deployment-url> demo-name.vercel.app  # Custom URL setzen
```

Jede Demo wird als separates Vercel-Projekt deployed mit eigener URL:
- autoteile-zurich.vercel.app
- bakery-demo.vercel.app
- restaurant-demo.vercel.app
etc.

### 11. Fertigstellung
- Bestätige dem User die fertige Website
- URL zum Dev-Server: http://localhost:4321
- URL zur Live-Demo: https://demo-name.vercel.app
- Hinweis auf Deployment-Bereitschaft (Vercel)

## ⚠️ KRITISCHE Regeln - IMMER befolgen!

### Überzeugungskraft (Demo muss zum Kauf führen!)
1. ✅ **JEDE Hero Section braucht ein Bild** - Keine Ausnahmen!
2. ✅ **Nie generisch** - Immer spezifisch für DIESES Unternehmen
3. ✅ **Konkrete Details** - Namen, Orte, Zahlen, Marken verwenden
4. ✅ **Überzeugende CTAs** - Spezifische Handlungsaufforderungen
5. ✅ **Professionelle Qualität** - Muss besser sein als aktuelle Website

### Technische Anforderungen
6. ✅ **Nie Copyright-Bilder** - Nur Unsplash
7. ✅ **Immer AI-Chat** - Auf jeder Seite `<AIChat />`
8. ✅ **Responsive Design** - Mobile-first
9. ✅ **SEO-optimiert** - Title, Description, H1-H6 Struktur
10. ✅ **4 Seiten minimum** - Home, Leistungen, Über uns, Kontakt

### Qualitätschecks vor Abschluss:
- [ ] Alle 4 Hero Sections haben Bilder?
- [ ] Firmenname wird überall verwendet?
- [ ] Services sind spezifisch (nicht generisch)?
- [ ] Standort wird erwähnt?
- [ ] CTAs sind überzeugend und spezifisch?
- [ ] Farbschema passt zur Branche?
- [ ] Alle Kontaktdaten sind korrekt?
- [ ] Website fühlt sich individuell an?

## Beispiel-Befehl vom User

User sagt nur: `https://www.example-bakery.ch`

Du machst:
1. ✅ WebFetch auf URL
2. ✅ Infos extrahieren
3. ✅ Neuen Demo-Ordner erstellen: `demos/example-bakery/`
4. ✅ 4 Seiten erstellen (Home, Produkte, Über uns, Kontakt)
5. ✅ Bilder von Unsplash (bakery, bread, pastry)
6. ✅ Orange/Amber Farbschema
7. ✅ Alle Komponenten nutzen
8. ✅ Build & Dev-Server starten
9. ✅ "Fertig! Die Website läuft auf http://localhost:4321"
10. ✅ Optional: Deploy zu Vercel mit `npx vercel --prod` und alias setzen

## Monorepo-Struktur

Dieses Projekt ist als Monorepo organisiert. Jede Demo-Website ist ein eigenständiges Astro-Projekt in `demos/`:

```
demo-websites/
├── demos/
│   ├── autoteile-zurich/     # Demo 1: https://autoteile-zurich.vercel.app
│   ├── bakery-demo/          # Demo 2: https://bakery-demo.vercel.app
│   └── restaurant-demo/      # Demo 3: https://restaurant-demo.vercel.app
└── README.md
```

Jede Demo hat ihre eigene:
- package.json (Dependencies)
- vercel.json (Deployment-Config)
- Eigene Vercel-Deployment-URL
