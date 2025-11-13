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
- Mobile: Chat nimmt volle Breite ein wenn geöffnet

### 3. Disclaimer
- **Disclaimer-Popup beim ersten Besuch (alle Geräte)**
- Wird im localStorage gespeichert
- Zusätzlicher Disclaimer im Footer sichtbar
- Hinweis: "Dies ist keine offizielle Website des Unternehmens"

### 4. Navigation
- Desktop: Horizontales Menü mit allen Links
- Mobile: Hamburger-Menü mit Toggle-Funktion
- Sticky Navigation auf allen Geräten

### 5. Responsive Design Checklist
Vor jedem Deployment prüfen:
- [ ] Navigation funktioniert auf Mobile
- [ ] Chat öffnet sich nicht automatisch auf Mobile
- [ ] Alle Texte sind lesbar auf kleinen Bildschirmen
- [ ] Bilder skalieren korrekt
- [ ] Formulare sind auf Mobile bedienbar
- [ ] Footer ist auf Mobile lesbar
- [ ] Disclaimer-Popup ist auf Mobile vollständig sichtbar

## Deployment

### Vercel
- Automatisches Deployment bei Push zu `main`
- URL: https://autoteile-zurich.vercel.app
- Vor Push: Lokalen Build testen mit `npm run build`

### Git Workflow
```bash
git add .
git commit -m "Beschreibung der Änderungen"
git push origin main
```

## Technologie-Stack
- **Framework**: Astro
- **Styling**: Tailwind CSS
- **Hosting**: Vercel
- **Sprache**: Deutsch (Schweiz)
