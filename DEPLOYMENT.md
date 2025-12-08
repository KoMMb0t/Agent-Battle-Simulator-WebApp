# 🚀 Deployment Guide

Dieser Guide zeigt dir, wie du die Agent Battle Simulator WebApp auf verschiedenen Plattformen deployen kannst.

## 📋 Voraussetzungen

- Python 3.11+
- Git
- Account auf der gewünschten Plattform

## 🌐 Deployment Optionen

### 1. Replit (Einfachste Option)

**Vorteile:** Kostenlos, kein Setup nötig, instant deployment

**Schritte:**

1. Gehe zu [replit.com](https://replit.com)
2. Klicke auf "Create Repl"
3. Wähle "Import from GitHub"
4. Gib die URL ein: `https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp`
5. Replit erkennt automatisch Python
6. Klicke auf "Run"
7. Fertig! 🎉

**Wichtig:** Replit nutzt automatisch Port 5000. Keine Änderungen nötig!

### 2. Render (Empfohlen für Production)

**Vorteile:** Kostenlos, automatische HTTPS, gute Performance

**Schritte:**

1. Gehe zu [render.com](https://render.com)
2. Klicke auf "New +" → "Web Service"
3. Verbinde dein GitHub Repository
4. Konfiguration:
   - **Name:** `agent-battle-webapp`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Klicke auf "Create Web Service"
6. Warte ~2 Minuten auf Deployment
7. Deine App ist live! 🚀

**URL:** `https://agent-battle-webapp.onrender.com`

### 3. Heroku

**Vorteile:** Etablierte Plattform, viele Add-ons

**Schritte:**

1. Installiere [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login: `heroku login`
3. Erstelle App:
```bash
cd Agent-Battle-Simulator-WebApp
heroku create agent-battle-webapp
```

4. Erstelle `Procfile`:
```bash
echo "web: gunicorn app:app" > Procfile
```

5. Deploy:
```bash
git add .
git commit -m "Add Procfile for Heroku"
git push heroku main
```

6. Öffne App:
```bash
heroku open
```

### 4. Railway

**Vorteile:** Moderne UI, einfaches Deployment

**Schritte:**

1. Gehe zu [railway.app](https://railway.app)
2. Klicke auf "New Project"
3. Wähle "Deploy from GitHub repo"
4. Wähle dein Repository
5. Railway erkennt automatisch Python
6. Klicke auf "Deploy"
7. Fertig! 🎉

### 5. PythonAnywhere

**Vorteile:** Python-spezialisiert, kostenloser Tier

**Schritte:**

1. Erstelle Account auf [pythonanywhere.com](https://www.pythonanywhere.com)
2. Gehe zu "Web" Tab
3. Klicke "Add a new web app"
4. Wähle "Flask"
5. Clone Repository:
```bash
cd ~
git clone https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp.git
```

6. Konfiguriere WSGI File:
```python
import sys
path = '/home/yourusername/Agent-Battle-Simulator-WebApp'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

7. Reload Web App
8. Fertig! 🎉

### 6. DigitalOcean App Platform

**Vorteile:** Professionell, skalierbar

**Schritte:**

1. Gehe zu [digitalocean.com](https://www.digitalocean.com/products/app-platform)
2. Klicke "Create App"
3. Verbinde GitHub Repository
4. Konfiguration:
   - **Type:** Web Service
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn app:app --bind 0.0.0.0:8080`
5. Klicke "Launch App"
6. Fertig! 🚀

## 🔧 Environment Variables

Für alle Plattformen kannst du optional folgende Environment Variables setzen:

- `PORT` - Port für den Server (default: 5001)
- `SECRET_KEY` - Flask Secret Key (wird automatisch generiert)

## 🐳 Docker Deployment

Erstelle `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

Build & Run:

```bash
docker build -t agent-battle-webapp .
docker run -p 5000:5000 agent-battle-webapp
```

## 🌍 Custom Domain

### Render
1. Gehe zu Settings → Custom Domains
2. Füge deine Domain hinzu
3. Konfiguriere DNS bei deinem Provider

### Heroku
```bash
heroku domains:add www.yourdomain.com
```

## 📊 Monitoring

### Render
- Automatische Logs im Dashboard
- Metriken für CPU/Memory

### Heroku
```bash
heroku logs --tail
```

## 🔒 HTTPS

Alle modernen Plattformen (Render, Heroku, Railway) bieten automatisch HTTPS!

## ⚡ Performance Tipps

1. **Gunicorn Workers:**
```bash
gunicorn app:app --workers 4 --bind 0.0.0.0:$PORT
```

2. **Caching:** Nutze Redis für Session-Storage (für Production)

3. **CDN:** Nutze Cloudflare für static assets

## 🆘 Troubleshooting

### "Application Error" auf Heroku
- Prüfe Logs: `heroku logs --tail`
- Stelle sicher, dass `Procfile` existiert
- Prüfe `requirements.txt`

### Port-Probleme
- Nutze `PORT` Environment Variable
- Default: 5001 (lokal), $PORT (production)

### Import-Fehler
- Stelle sicher, dass `game/` Ordner existiert
- Prüfe `__init__.py` in `game/`

## 📞 Support

Bei Problemen:
1. Prüfe Logs der Plattform
2. Erstelle [GitHub Issue](https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp/issues)
3. Email: kommuniverse@gmail.com

## ✅ Deployment Checklist

- [ ] Repository auf GitHub gepusht
- [ ] `requirements.txt` aktuell
- [ ] `Procfile` erstellt (für Heroku)
- [ ] Environment Variables gesetzt
- [ ] Deployment getestet
- [ ] Custom Domain konfiguriert (optional)
- [ ] Monitoring eingerichtet

---

**Happy Deploying! 🚀**
