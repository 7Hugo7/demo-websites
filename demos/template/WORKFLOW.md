# Website Development Workflow
**Zentrale Workflow-Datei für ALLE Demo-Websites**
Pfad: `demos/template/WORKFLOW.md`

## 0. Template Verwendung & Originalseite analysieren
- **IMMER Komponenten aus dem Template-Ordner kopieren**
- **IMMER die Original-Website analysieren und Inhalte übernehmen**
- **Dieser Workflow gilt für ALLE Demo-Projekte - NICHT in einzelne Projekte kopieren**
- Template-Pfad: `demos/template/src/components/`

### Workflow beim Erstellen einer neuen Demo-Website:
1. **Original-Website analysieren** (z.B. mit WebFetch oder manuell)
   - Navigation und Seitenstruktur erfassen
   - Logo-URLs und Branding-Elemente extrahieren
   - Farbschema (Hex-Codes) notieren
   - Echte Firmeninfos sammeln (Adresse, Telefon, Email, Öffnungszeiten)
   - Service-Beschreibungen und Texte kopieren
   - **Bildmaterial-URLs sammeln und downloaden/verwenden**
   - Design-Patterns und Layout verstehen
   - **Business-Type bestimmen (für Chatbot-Personalisierung) - WICHTIG!**

2. **Neues Astro-Projekt erstellen**
3. **Tailwind CSS hinzufügen**
4. **ALLE Komponenten aus `demos/template/src/` kopieren**
5. **Komponenten mit echten Daten anpassen:**
   - Firmenlogo einbinden
   - Farbschema aus Original übernehmen
   - Navigation entsprechend Original aufbauen
   - Echte Texte und Beschreibungen verwenden
   - Kontaktdaten korrekt eintragen
   - **Bilder vom Original verwenden (gleiche oder ähnliche Motive)**

6. **⚠️ AI-CHATBOT VOLLSTÄNDIG PERSONALISIEREN (MANDATORY!):**
   - ✅ `businessType` in allen Pages setzen (auto-parts, bakery, lawyer, restaurant, industrial, default)
   - ✅ **CHATBOT-FARBE muss mit Site-Farbe übereinstimmen!** (`primaryColor` Prop setzen)
   - ✅ **NEUE businessConfig in AIChat.astro hinzufügen falls nötig**
   - ✅ **CUSTOM FORMULAR erstellen mit branchenspezifischen Feldern**
   - ✅ **ÖFFNUNGSZEITEN im Chatbot aktualisieren (case 'opening-hours')**
   - ✅ Custom Quick-Reply-Optionen für die Branche erstellen
   - ✅ Neue Actions im handleOptionClick Switch hinzufügen
   - ✅ Firmenname, Telefon, Maps-URL korrekt setzen

7. **Footer auf allen Pages anpassen:**
   - ✅ `openingHours` Array definieren
   - ✅ `phone` und `email` Props setzen

```bash
# Beispiel: Neue Demo-Website erstellen
cd demos
npm create astro@latest neue-website -- --template minimal --no-install --no-git --typescript strict
cd neue-website
npm install
npx astro add tailwind --yes

# Komponenten aus Template kopieren
cp -r ../template/src/components/* ./src/components/
cp -r ../template/src/layouts/* ./src/layouts/
cp -r ../template/src/pages/* ./src/pages/

# Original-Website analysieren (z.B. https://www.firma.ch)
# WebFetch verwenden oder manuell erfassen

# Dann Anpassungen vornehmen mit echten Daten:
# - Logo, Farben, Navigation, Texte, Kontaktdaten
```

### AI-Chatbot Personalisierung (WICHTIG!)
Der Chatbot muss **IMMER** an die Branche angepasst werden:

**Verfügbare Business-Types:**
- `auto-parts` - Ersatzteile, Autowerkstatt (mit Fahrzeug-Formular)
- `bakery` - Bäckerei, Konditorei
- `lawyer` - Anwaltskanzlei, Rechtsberatung
- `restaurant` - Restaurant, Gastronomie
- `industrial` - Industrie, Oberflächentechnik (mit Bauteil/Beschichtung-Formular)
- `default` - Allgemeine Dienstleistungen

**Was anpassen in den Pages:**
```astro
<AIChat
  businessType="industrial"  // <- An Branche anpassen!
  companyName="Firma Name"
  phone="+41 XX XXX XX XX"
  mapsUrl="https://www.google.com/maps/..."
  primaryColor="#4D7ABF"     // <- Muss mit Site-Farbe übereinstimmen!
/>
```

**✨ Features des AI-Chatbots:**
- ✅ **Full-Screen Formular**: Wenn ein Formular angezeigt wird, versteckt sich der Nachrichten-Bereich automatisch und das Formular nimmt den gesamten Chat-Bereich ein
- ✅ **Dynamische Farben**: Alle Button- und Akzentfarben passen sich automatisch der `primaryColor` an
- ✅ **Responsive Design**: Optimiert für Mobile (voller Bildschirm) und Desktop (abgerundetes Fenster)
- ✅ **Abgerundete Ecken**: Chat-Fenster ohne Borders, mit `rounded-t-2xl` (mobile) / `rounded-2xl` (desktop)

**WICHTIG: Für neue Branchen MÜSSEN folgende Anpassungen in `AIChat.astro` gemacht werden:**

1. **businessConfig erweitern** - Neue Branche hinzufügen:
```javascript
'neue-branche': {
  welcome: `Begrüßungstext für ${companyName}`,
  options: [
    { text: '📋 Aktion 1', value: 'action-1' },
    { text: '🕒 Öffnungszeiten', value: 'opening-hours' },
    { text: '📞 Kontakt', value: 'contact' }
  ]
}
```

2. **Formular anpassen** - In der `showForm(type)` Funktion:
```javascript
} else if (type === 'neue-branche') {
  form.innerHTML = `
    <div>
      <label class="block text-sm font-medium mb-1">Branchenspezifisches Feld *</label>
      <input type="text" name="field" required class="..." />
    </div>
    // Weitere branchenspezifische Felder
  `;
```

3. **Öffnungszeiten aktualisieren** - Im `handleOptionClick` bei `case 'opening-hours'`:
```javascript
addMessage('Unsere Öffnungszeiten:<br><br>📅 Montag - Freitag<br>🕒 XX:XX - XX:XX Uhr...');
```

4. **Neue Actions hinzufügen** - Im `handleOptionClick` Switch für custom Options:
```javascript
case 'neue-action':
  addMessage('Response Text');
  setTimeout(() => showForm('neue-branche'), 500);
  break;
```

**Beispiele erfolgreicher Customizations:**
- **Auto-Parts**: Formular mit Fahrzeug, Ersatzteil, Kontakt
- **Industrial (Bührer AG)**: Formular mit Firma, Bauteil/Material, Beschichtung, Kontakt

**Footer auch anpassen:**
```astro
<Footer
  companyName="Firma Name"
  phone="+41 XX XXX XX XX"
  email="info@firma.ch"
  openingHours={openingHours}  // Array definieren!
/>
```

### Bildmaterial-Verwendung (WICHTIG!)
**IMMER ähnliche Bilder wie auf der Original-Website verwenden:**

1. **Logo**: Direkt von Original-Website URL verwenden wenn möglich
2. **Hero-Images**: Ähnliche Motive wie Original (Industrie, Produkte, etc.)
3. **Service-Bilder**: Passend zur Branche und Services
4. **ImageCards**: Thematisch konsistente Bilder

**Quellen für Bilder:**
- Original-Website (beste Option)
- Unsplash mit passenden Suchbegriffen zur Branche
- Firmenspezifische Stock-Fotos

**Beispiel für Bührer AG (Thermisches Spritzen):**
```astro
// Industrie-bezogene Bilder verwenden
backgroundImage="https://images.unsplash.com/photo-1581092918056-0c4c3acd3789"
// Suchbegriffe: industrial, manufacturing, metal work, coating
```

## Wichtige Richtlinien für diese Website

### 1. Mobile-First Approach
- **Alle Komponenten müssen auf allen Geräten gut aussehen**
- Verwende Tailwind CSS responsive Breakpoints (sm, md, lg, xl)
- Teste auf verschiedenen Bildschirmgrößen (Mobile, Tablet, Desktop)

### 2. Chat-Verhalten
- **Der AI-Chatbot darf sich auf Mobile NIE automatisch öffnen**
- Auto-open nur auf Desktop (>= 768px Breite)
- Mobile: Chat-Button sichtbar, aber geschlossen
- Mobile: Chat nimmt volle Breite ein wenn geöffnet (92vh Höhe)
- **Formulare im Chat müssen vollständig ohne Scrollen sichtbar sein**
- Kompakte Formularfelder auf Mobile: kleinere Padding (py-1.5), kleinere Schrift (text-xs)
- Weniger Abstand zwischen Formularfeldern (space-y-2 statt space-y-3)
- Textarea rows auf Mobile reduziert (2 Zeilen statt 3)
- Input-Area: max-h-[45vh] auf Mobile für bessere Sichtbarkeit

### 3. Disclaimer
- **Disclaimer-Popup beim ersten Besuch (alle Geräte)**
- Wird im localStorage gespeichert
- Zusätzlicher Disclaimer im Footer sichtbar
- Hinweis: "Dies ist keine offizielle Website des Unternehmens"

### 4. Navigation
- Desktop: Horizontales Menü mit allen Links
- Mobile: Hamburger-Menü mit Toggle-Funktion
- Sticky Navigation auf allen Geräten

### 5. Content & UX Richtlinien
- **Texte auf Mobile: kurz und prägnant halten**
- Services: Max. 4-6 Items, kurze Beschreibungen (1 Satz)
- **WICHTIG: B2B/Professional Sites - KEINE Emoji-Icons verwenden!**
  - B2B-Websites (Industrie, Handwerk, Professional Services) müssen professionell wirken
  - KEINE Emojis in Services, Cards, oder Content
  - Nur bei B2C (Bäckerei, Restaurant, etc.) sind Emojis akzeptabel
  - Alternative: Verwende SVG-Icons oder Text ohne Icons
- Keine überwältigenden Textmengen auf kleinen Bildschirmen
- Grid Layouts: 2 Spalten auf Mobile, 4 auf Desktop
- Schriftgrößen: text-xs/text-sm auf Mobile, text-base auf Desktop

### 6. Komponenten Best Practices
- **Services Component**: Grid mit 2 Spalten (Mobile) → 4 Spalten (Desktop)
- **ImageCard**: Responsive Bilderhöhe (h-48 Mobile, h-64 Desktop)
- **Navigation**: Hamburger-Menü auf Mobile mit Toggle
- **Footer**: Responsive Padding und Schriftgrößen
- **Formulare**: Kompakte Darstellung auf Mobile

### 7. Responsive Design Checklist
Vor jedem Deployment prüfen:
- [ ] Navigation funktioniert auf Mobile
- [ ] Chat öffnet sich nicht automatisch auf Mobile
- [ ] Chat-Formulare vollständig sichtbar ohne Scrollen
- [ ] Alle Texte sind lesbar und nicht zu lang auf kleinen Bildschirmen
- [ ] Bilder skalieren korrekt
- [ ] Formulare sind auf Mobile bedienbar
- [ ] Footer ist auf Mobile lesbar
- [ ] Disclaimer-Popup ist auf Mobile vollständig sichtbar

### 8. AI-Chatbot Customization Checklist ⚠️
**VOR DEPLOYMENT ZWINGEND PRÜFEN:**
- [ ] **businessType** in allen Pages korrekt gesetzt (nicht "default" wenn Branche bekannt!)
- [ ] **businessConfig** in AIChat.astro erweitert mit branchenspezifischen Options
- [ ] **Custom Formular** für die Branche erstellt (showForm Funktion)
  - [ ] Branchenspezifische Felder definiert (z.B. Fahrzeug, Bauteil, etc.)
  - [ ] Placeholder-Texte angepasst
  - [ ] Alle required Felder korrekt markiert
- [ ] **Öffnungszeiten** im Chatbot aktualisiert (case 'opening-hours')
- [ ] **handleOptionClick** erweitert mit neuen Actions
- [ ] **Firmenname, Telefon, Email** in allen Pages korrekt
- [ ] **Google Maps URL** korrekt gesetzt
- [ ] **Footer** mit openingHours Array, phone und email auf allen Pages
- [ ] Chatbot getestet: Alle Options funktionieren, Formular wird korrekt angezeigt
- [ ] Chatbot getestet: Formular-Submit zeigt Erfolgsmeldung

**WICHTIG:** Nicht mit "default" businessType deployen wenn eine passendere Branche existiert oder erstellt werden kann!

## Deployment

### Vercel
- **IMMER manuelles Deployment mit `npx vercel --prod --yes` nach Push**
- Automatisches Deployment ist zu langsam
- **Nach erstem Deployment: Alias erstellen für saubere URL**

### Git Workflow
```bash
git add -A
git commit -m "Beschreibung der Änderungen"
git push origin main
npx vercel --prod --yes
```

### Erstes Deployment - Alias erstellen
Nach dem ersten Deployment muss eine saubere URL erstellt werden:
```bash
# Deployment URL von Vercel kopieren (z.B. https://project-xyz.vercel.app)
# Alias erstellen (project-name sollte dem Ordnernamen entsprechen)
npx vercel alias <deployment-url> <project-name>.vercel.app

# Beispiel:
# npx vercel alias https://autoteile-zurich-xyz.vercel.app autoteile-zurich.vercel.app
```

## Technologie-Stack
- **Framework**: Astro
- **Styling**: Tailwind CSS
- **Hosting**: Vercel
- **Sprache**: Deutsch (Schweiz)
