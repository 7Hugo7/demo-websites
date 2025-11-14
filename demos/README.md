# Demo Websites

This folder contains demo websites built with the template system.

## 📋 Workflow

**All demo websites follow the same workflow documented in:**
**`template/WORKFLOW.md`**

Please refer to that file for:
- How to create a new demo website
- Template usage guidelines
- Original website analysis
- AI Chatbot personalization
- Image usage guidelines
- Deployment instructions

## 📁 Structure

```
demos/
├── template/           # Master template with all reusable components
│   ├── WORKFLOW.md    # ⭐ CENTRAL WORKFLOW (read this!)
│   └── src/
│       ├── components/
│       ├── layouts/
│       └── pages/
├── autoteile-zurich/  # Demo: Auto parts shop
├── buehrer-ag/        # Demo: Thermal spraying company
└── [future-demos]/    # Add more demo projects here
```

## 🚀 Demo Sites

- **Autoteile Zürich**: https://autoteile-zurich.vercel.app
- **Bührer AG**: https://buehrer-ag.vercel.app

## 🛠️ Quick Start

```bash
cd demos
# Read the workflow first!
cat template/WORKFLOW.md

# Then create your new demo following the workflow
npm create astro@latest neue-demo -- --template minimal --no-install --no-git --typescript strict
```
