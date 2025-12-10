# 📸 Automatic Screenshot Generator

Automatisches Tool zum Erstellen von Screenshots für Hackathon-Submissions.

---

## 🚀 Quick Start (Windows)

### Option 1: Einfachste Methode
```cmd
auto_screenshot.bat
```

### Option 2: Manuell
```cmd
pip install selenium webdriver-manager
python auto_screenshot.py
```

---

## 🚀 Quick Start (Linux/Mac)

```bash
pip3 install selenium webdriver-manager
python3 auto_screenshot.py
```

---

## 📋 Was das Skript macht

1. ✅ Erstellt `screenshots/` Ordner
2. ✅ Startet Flask Server automatisch
3. ✅ Öffnet Chrome im Headless-Modus
4. ✅ Navigiert durchs Spiel:
   - Bot Selection Screen
   - Bots auswählen
   - Battle starten
   - Aktionen ausführen
   - Bis zum Victory Screen
5. ✅ Macht 8 Screenshots an wichtigen Stellen
6. ✅ Speichert alles in `screenshots/`
7. ✅ Räumt auf (Server stoppen, Browser schließen)

---

## 📸 Generierte Screenshots

| Datei | Beschreibung |
|-------|--------------|
| `01_bot_selection.png` | Bot Selection Screen mit allen 21 Bots |
| `02_bots_selected.png` | Ausgewählte Bots (Mende vs Sentinel) |
| `03_battle_start.png` | Battle Screen - Runde 1 |
| `04_battle_ui.png` | Battle UI Details (HP/Stamina/XP Bars) |
| `05_action_executed.png` | Nach erster Aktion |
| `06_mid_battle.png` | Mid-Battle mit Buffs/Debuffs |
| `07_victory_screen.png` | Victory Screen mit Stats |
| `08_final_state.png` | Final Game State |

---

## 🔧 Voraussetzungen

### Windows:
1. **Python 3.7+** installiert
2. **Google Chrome** installiert
3. **ChromeDriver** (wird automatisch installiert)

### Linux/Mac:
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser chromium-chromedriver

# Mac
brew install chromedriver
```

---

## 🐛 Troubleshooting

### Problem: "ChromeDriver not found"
**Lösung 1 (Einfach):**
```cmd
pip install webdriver-manager
```

Dann update `auto_screenshot.py`:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
```

**Lösung 2 (Manuell):**
1. Download ChromeDriver: https://chromedriver.chromium.org/
2. Entpacke `chromedriver.exe`
3. Füge zu PATH hinzu oder lege in Projekt-Ordner

### Problem: "Port 3000 already in use"
**Lösung:**
Ändere `FLASK_PORT` in `auto_screenshot.py`:
```python
FLASK_PORT = 5001
BASE_URL = "http://localhost:5001"
```

Und in `app.py`:
```python
port = int(os.environ.get('PORT', 5001))
```

### Problem: "Selenium module not found"
**Lösung:**
```cmd
pip install selenium
```

### Problem: Screenshots sind schwarz/leer
**Lösung:**
Entferne `--headless` aus `auto_screenshot.py`:
```python
# chrome_options.add_argument("--headless")  # Auskommentieren
```

---

## 🎨 Manuelle Screenshots (Alternative)

Falls das Skript nicht funktioniert:

### Windows:
1. Starte `python app.py`
2. Öffne http://localhost:3000 im Browser
3. Drücke `Windows + Shift + S` für Screenshots
4. Speichere in `screenshots/` Ordner

### Mac:
1. Starte `python app.py`
2. Öffne http://localhost:3000 im Browser
3. Drücke `Cmd + Shift + 4` für Screenshots
4. Speichere in `screenshots/` Ordner

---

## 📝 Für Devpost Submission

Nach dem Ausführen:
1. Öffne `screenshots/` Ordner
2. Wähle beste 4-5 Screenshots aus
3. Upload zu Devpost:
   - `01_bot_selection.png` (zeigt alle 21 Bots)
   - `04_battle_ui.png` (zeigt UI Details)
   - `06_mid_battle.png` (zeigt Gameplay)
   - `07_victory_screen.png` (zeigt Victory)

---

## 🎥 Video Recording (Optional)

Das Skript macht nur Screenshots. Für Video:

### Windows:
- **OBS Studio** (kostenlos): https://obsproject.com/
- **Xbox Game Bar**: `Windows + G`

### Mac:
- **QuickTime**: `Cmd + Shift + 5`

### Linux:
- **SimpleScreenRecorder**: `sudo apt-get install simplescreenrecorder`

**Recording-Tipps:**
- 1920x1080 Resolution
- 30 FPS ausreichend
- 2-3 Minuten Länge
- Zeige alle Features
- Upload zu YouTube (Unlisted)

---

## ✅ Checklist

- [ ] Python 3.7+ installiert
- [ ] Chrome installiert
- [ ] Selenium installiert (`pip install selenium`)
- [ ] ChromeDriver installiert
- [ ] `auto_screenshot.py` ausgeführt
- [ ] Screenshots in `screenshots/` vorhanden
- [ ] Beste Screenshots ausgewählt
- [ ] Zu Devpost uploaded

---

**Made with 📸 for AI Champion Ship Hackathon**
