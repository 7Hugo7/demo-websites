# Demo Websites Monorepo

This repository contains multiple demo websites, each deployed separately to Vercel.

## 🚀 Project Structure

```text
/
├── demos/
│   └── autoteile-zurich/    # Auto parts shop demo
│       ├── src/
│       ├── public/
│       ├── package.json
│       └── vercel.json
└── README.md
```

## 📦 Available Demos

- **autoteile-zurich** - Auto parts shop website
  - URL: https://autoteile-zurich.vercel.app
  - Location: `demos/autoteile-zurich/`

## 🧞 Working with Demos

Each demo is a standalone Astro project. To work on a demo:

```sh
cd demos/autoteile-zurich
npm install
npm run dev
```

## 🚀 Deploying

Each demo is deployed as a separate Vercel project:

```sh
cd demos/autoteile-zurich
npx vercel --prod
```
