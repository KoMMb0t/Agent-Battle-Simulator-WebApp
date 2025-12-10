# 🚀 Render Deployment Guide

## Quick Deploy (5 Minutes)

### Step 1: Gehe zu Render.com
**https://render.com**

### Step 2: Sign Up / Login
- Erstelle Account (kostenlos)
- Verbinde GitHub Account

### Step 3: New Web Service
1. Klicke **"New +"** → **"Web Service"**
2. Wähle Repository: `Agent-Battle-Simulator-WebApp`
3. Klicke **"Connect"**

### Step 4: Konfiguration

**Name**: `agent-battle-simulator`

**Environment**: `Python 3`

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

**Plan**: `Free` (ausreichend für Hackathon)

### Step 5: Environment Variables

Keine nötig! (SECRET_KEY wird automatisch generiert)

### Step 6: Deploy

Klicke **"Create Web Service"**

⏳ Warte ~3-5 Minuten

✅ Du bekommst URL: `https://agent-battle-simulator.onrender.com`

---

## ✅ Deployment Checklist

- [ ] Render Account erstellt
- [ ] GitHub Repository verbunden
- [ ] Web Service konfiguriert
- [ ] Deployment gestartet
- [ ] URL funktioniert
- [ ] Alle 21 Bots laden
- [ ] Battle funktioniert
- [ ] Screenshots gemacht
- [ ] URL in Devpost eingetragen

---

## 🐛 Troubleshooting

### Problem: "Application failed to start"
**Lösung**: Prüfe Build Log, stelle sicher dass `gunicorn` in requirements.txt ist

### Problem: "Port already in use"
**Lösung**: Render setzt $PORT automatisch, keine Änderung nötig

### Problem: "Module not found"
**Lösung**: Alle Dependencies in requirements.txt? `pip freeze > requirements.txt`

---

## 📊 Nach Deployment

### 1. Teste die Live-App
- Öffne URL
- Wähle 2 Bots
- Starte Battle
- Spiele bis zum Ende

### 2. Screenshots machen
- Bot Selection Screen
- Battle Screen (Mid-Fight)
- Victory Screen
- XP Bar / Level Up

### 3. Devpost Update
- Füge Live-URL hinzu
- Upload Screenshots
- Optional: Screen Recording

---

## 🎥 Demo Video (Optional)

### Quick Recording (2 Minuten):
1. Öffne https://www.loom.com
2. "Start Recording"
3. Zeige:
   - Bot Selection (10 Sek)
   - Battle Start (10 Sek)
   - Combat Actions (30 Sek)
   - Victory Screen (10 Sek)
   - Erkläre Features (60 Sek)
4. Upload zu YouTube
5. Link in Devpost

---

## ✅ FERTIG!

Deine App ist jetzt live und bereit für die Hackathon-Submission! 🎉
