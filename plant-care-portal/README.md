# GreenRoot — Online Plant Disease Detection Portal

A greenery-themed React portal for plant disease detection, plant identification, botanist help,
blogs, community feed, weed community and an offline-first database — with **3D visual effects**,
**haptic feedback**, and **multi-language** support (English, Hindi, Spanish, French).

## Tech Stack

- **React 18 + Vite** — fast SPA
- **React Router** — navigation
- **Framer Motion** — animations
- **Dexie (IndexedDB)** — offline database
- **react-i18next** — translations

## Getting Started

```bash
npm install
npm run dev
```

Build for production:

```bash
npm run build
npm run preview
```

> On Windows, if PowerShell blocks `npm`, run `npm.cmd install` instead.

## Features

- 🔍 **Disease Detection** — upload a leaf image, match symptoms, get treatment plans
- 🌿 **Plant Identifier** — recognize plants and get care guides
- 🐛 **All Problems** — browse common plant problems (pests, diseases, deficiencies)
- 📝 **Blogs** — gardening & plant-health articles with detail views
- 👩‍🌾 **Botanist Help** — book consultations with experts
- 💬 **Feed** — share posts with the community
- 🌾 **Weed Community** — a forum-style space for growers
- 🗄️ **Database** — browse diseases & plants stored in the IndexedDB, with add/remove/search
- 🌍 **Language Switcher** — EN / हिंदी / ES / FR
- 📳 **Haptics** — `navigator.vibrate` feedback on supported devices
- 🎲 **3D tilt cards** & floating leaf particles

## Folder Structure

```
plant-care-portal/
├── public/                 # static assets (favicon)
├── src/
│   ├── components/         # layout + UI components
│   ├── context/            # global app context
│   ├── data/               # static seed content
│   ├── db/                 # Dexie database layer
│   ├── i18n/               # translations + language config
│   ├── pages/              # route pages
│   ├── utils/              # haptics, formatting helpers
│   ├── App.jsx             # router + layout shell
│   ├── main.jsx            # entry point
│   └── index.css           # greenery theme + 3D styles
```
