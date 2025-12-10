# 🪟 Windows Setup Guide

## 🎯 Schritt-für-Schritt Anleitung für Windows

### 1️⃣ Python installieren

1. Gehe zu [python.org/downloads](https://www.python.org/downloads/)
2. Lade **Python 3.11+** herunter
3. **WICHTIG:** Hake "Add Python to PATH" an!
4. Installiere Python

**Testen:**
```cmd
python --version
```
Sollte zeigen: `Python 3.11.x` oder höher

---

### 2️⃣ Projekt herunterladen

**Option A: Mit Git (empfohlen)**

1. Installiere [Git für Windows](https://git-scm.com/download/win)
2. Öffne **PowerShell** oder **CMD**
3. Navigiere zu deinem Wunschordner:
```cmd
cd C:\Users\ModBot\
```

4. Clone das Repository:
```cmd
git clone https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp.git
cd Agent-Battle-Simulator-WebApp
```

**Option B: ZIP Download**

1. Gehe zu https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp
2. Klicke auf grünen "Code" Button
3. Wähle "Download ZIP"
4. Entpacke nach `C:\Users\ModBot\Agent-Battle-Simulator-WebApp`
5. Öffne CMD/PowerShell in diesem Ordner

---

### 3️⃣ Dependencies installieren

Im Projekt-Ordner:

```cmd
pip install -r requirements.txt
```

Falls Fehler: Versuche:
```cmd
python -m pip install -r requirements.txt
```

---

### 4️⃣ Server starten

```cmd
python app.py
```

Du solltest sehen:
```
 * Running on http://127.0.0.1:5001
```

---

### 5️⃣ Im Browser öffnen

Öffne deinen Browser und gehe zu:

**http://localhost:5001**

🎮 **Das Spiel läuft jetzt lokal!**

---

## 🐛 Troubleshooting

### Problem: "python" wird nicht erkannt

**Lösung:** Nutze `py` statt `python`:
```cmd
py app.py
```

### Problem: Port 5001 bereits belegt

**Lösung:** Ändere Port in `app.py` (Zeile 137):
```python
port = int(os.environ.get('PORT', 5002))  # Ändere auf 5002
```

### Problem: Module nicht gefunden

**Lösung:** Installiere einzeln:
```cmd
pip install Flask flask-cors
```

### Problem: "Permission denied"

**Lösung:** Führe CMD/PowerShell als Administrator aus

---

## 🚀 Dauerhaft Deployen (Online verfügbar machen)

### Option 1: Replit (EINFACHSTE!)

1. Gehe zu [replit.com](https://replit.com)
2. Erstelle Account (kostenlos)
3. Klicke "Create Repl"
4. Wähle "Import from GitHub"
5. Gib ein: `https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp`
6. Klicke "Import from GitHub"
7. Klicke "Run" ▶️
8. **FERTIG!** Du bekommst eine öffentliche URL!

**Vorteile:**
- ✅ Kostenlos
- ✅ Keine Konfiguration nötig
- ✅ Instant Deployment
- ✅ Öffentliche URL

---

### Option 2: Render (Empfohlen für Production)

1. Gehe zu [render.com](https://render.com)
2. Erstelle Account (kostenlos)
3. Klicke "New +" → "Web Service"
4. Verbinde GitHub Account
5. Wähle Repository: `Agent-Battle-Simulator-WebApp`
6. Konfiguration:
   - **Name:** `agent-battle-webapp`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
7. Klicke "Create Web Service"
8. Warte ~2 Minuten
9. **FERTIG!** Du bekommst URL wie: `https://agent-battle-webapp.onrender.com`

**Vorteile:**
- ✅ Kostenlos
- ✅ Automatisches HTTPS
- ✅ Gute Performance
- ✅ Custom Domain möglich

---

### Option 3: Railway

1. Gehe zu [railway.app](https://railway.app)
2. Erstelle Account
3. Klicke "New Project"
4. Wähle "Deploy from GitHub repo"
5. Wähle dein Repository
6. Railway erkennt automatisch Python
7. Klicke "Deploy"
8. **FERTIG!**

---

## 📱 Von anderen Geräten testen

### Im lokalen Netzwerk (z.B. Handy)

1. Finde deine lokale IP:
```cmd
ipconfig
```
Suche nach "IPv4-Adresse" (z.B. `192.168.1.100`)

2. Ändere in `app.py` (Zeile 138):
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

3. Starte Server neu

4. Auf anderem Gerät im gleichen WLAN:
```
http://192.168.1.100:5001
```

---

## 🔄 Updates vom GitHub pullen

Wenn du Änderungen am Code machst:

```cmd
cd Agent-Battle-Simulator-WebApp
git pull origin main
```

---

## 🎨 Code bearbeiten

**Empfohlene Editoren:**
- [VS Code](https://code.visualstudio.com/) (kostenlos, beste Wahl!)
- [PyCharm](https://www.jetbrains.com/pycharm/) (Community Edition kostenlos)
- Notepad++ (einfach)

**Wichtige Dateien:**
- `app.py` - Backend Logic
- `templates/index.html` - HTML Structure
- `static/css/style.css` - Styling
- `static/js/game.js` - Frontend Logic
- `game/actions.py` - Aktionen hinzufügen/ändern

---

## 📞 Hilfe benötigt?

1. Prüfe [GitHub Issues](https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp/issues)
2. Erstelle neues Issue
3. Email: kommuniverse@gmail.com

---

## ✅ Quick Checklist

- [ ] Python 3.11+ installiert
- [ ] Repository gecloned/downloaded
- [ ] Dependencies installiert (`pip install -r requirements.txt`)
- [ ] Server gestartet (`python app.py`)
- [ ] Im Browser getestet (`http://localhost:5001`)
- [ ] Optional: Auf Replit/Render deployed

---

**Viel Erfolg! 🚀**
