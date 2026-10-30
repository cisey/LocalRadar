# 🌐 Local Radar · Live Guides

This repository hosts the **live output** of the [Local Radar](https://github.com/cisey/local-radar) project. 

Local Radar is a Python-based scraper and guide generator. It scans Google Maps for highly-rated places, filters them by rating and reviews, and builds interactive HTML guides. The generated HTML files are published here and served via **GitHub Pages**.

👉 **Explore the live guides:** **[https://cisey.github.io/LocalRadar/](https://cisey.github.io/LocalRadar/)**

## ✨ Features

- 📱 **Mobile-First Design** — Clean, responsive UI tailored for phone screens
- 🌙 **Modern Dark Mode** — Glassmorphism cards, soft gradients, and readable typography
- 🔍 **Instant Search** — Filter guides by city, district, or filename
- 🗂️ **Smart Grouping** — Automatically categorizes and sorts guides by province
- 🏷️ **Dynamic Badges** — Visual indicators for food guides vs. general guides
- ⚡ **Automated Index** — A GitHub Action (`update-guides.yml`) automatically updates `rehberler.json` whenever a new guide is pushed

## 📁 How It Works

1. **Generation**: The Python program generates a new `.html` guide for a district.
2. **Push**: The guide is pushed to this repository.
3. **Automation**: GitHub Actions detects the new file and automatically updates `rehberler.json`.
4. **Publishing**: GitHub Pages serves the new guide, and `index.html` instantly lists it in the UI.

## 🛠️ Architecture

- **Frontend**: Vanilla HTML, CSS, and JavaScript (no frameworks, fast loading)
- **Data Source**: `rehberler.json` (with GitHub API fallback)
- **Automation**: GitHub Actions for indexing
- **Hosting**: GitHub Pages

## 🤝 Related Projects

- **[cisey/local-radar](https://github.com/cisey/local-radar)** — The core Python scraper, GUI, and guide generator.

## ⚠️ Disclaimer

The data displayed in these guides is scraped from publicly available Google Maps data. This is for personal and educational use only. Not affiliated with Google.

Made with ❤️ for travelers and foodies.
