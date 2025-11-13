# Website Development Workflow

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
- Icons verwenden für visuelle Auflockerung
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

## Deployment

### Vercel
- **IMMER manuelles Deployment mit `npx vercel --prod` nach Push**
- Automatisches Deployment ist zu langsam
- URL: https://autoteile-zurich.vercel.app

### Git Workflow
```bash
git add -A
git commit -m "Beschreibung der Änderungen"
git push origin main
npx vercel --prod
```

## Technologie-Stack
- **Framework**: Astro
- **Styling**: Tailwind CSS
- **Hosting**: Vercel
- **Sprache**: Deutsch (Schweiz)
