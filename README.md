# 🤖 Agent Battle Simulator - WebApp Edition

**Absurde Kämpfe. Maximaler Spaß. Null Sinn.**

Eine vollständig spielbare Browser-Version des Agent Battle Simulators, erstellt für den **Cline Hackathon**!

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)

## 🎮 Features

- **8 absurde Kampfaktionen** mit einzigartigen Effekten
- **HP & Stamina System** mit visuellen Balken
- **Buffs & Debuffs** (Brennend, Verlangsamt, Demoralisiert, etc.)
- **AI-Gegner** mit strategischer Aktionswahl
- **Live Kampf-Kommentar** mit witzigen Sprüchen
- **Retro Gaming Ästhetik** (Courier New, Neon-Grün)

## 🚀 Quick Start

```bash
# Repository klonen
git clone https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp.git
cd Agent-Battle-Simulator-WebApp

# Dependencies installieren
pip install -r requirements.txt

# Server starten
python app.py
```

Öffne deinen Browser: `http://localhost:5001`

## 🎲 Spielanleitung

1. **Start Screen:** Gib Namen für beide Agents ein
2. **Kampf:** Wähle jede Runde eine Aktion (1-8)
3. **Strategie:** Achte auf Stamina-Kosten und Effekte
4. **Sieg:** Reduziere die HP des Gegners auf 0!

## 🌐 Deployment

### Replit
1. Importiere Repository
2. Setze `PORT=5000`
3. Run!

### Render
1. Neuer Web Service
2. Build: `pip install -r requirements.txt`
3. Start: `gunicorn app:app`

## 📝 Lizenz

Apache License 2.0

## 👨‍💻 Autor

**KoMMb0t** - kommuniverse@gmail.com

**Original Projekt:** [github.com/KoMMb0t/Hackaton](https://github.com/KoMMb0t/Hackaton)
