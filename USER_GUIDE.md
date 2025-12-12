# 🎮 Agent Battle Simulator - Benutzerhandbuch

**Einfache Anleitung für Einsteiger** - Keine Programmierkenntnisse erforderlich!

---

## 📖 Was ist das?

**Agent Battle Simulator** ist ein Browserspiel, bei dem du **21 einzigartige Kampf-Bots** gegeneinander antreten lassen kannst. Jeder Bot hat besondere Fähigkeiten und du kannst ihre Aktionen in Echtzeit verfolgen!

**Keine Installation nötig** - läuft direkt im Browser! 🌐

---

## 🚀 Schnellstart (3 Schritte)

### Schritt 1: Herunterladen

**Windows:**
1. Gehe zu: https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp
2. Klicke auf den grünen **"Code"** Button
3. Wähle **"Download ZIP"**
4. Entpacke die ZIP-Datei (Rechtsklick → "Alle extrahieren...")

**Ubuntu/Linux:**
```bash
# Terminal öffnen und eingeben:
git clone https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp.git
cd Agent-Battle-Simulator-WebApp
```

**Android (mit Termux):**
1. Installiere **Termux** von F-Droid: https://f-droid.org/packages/com.termux/
2. Öffne Termux und gib ein:
```bash
git clone https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp.git
cd Agent-Battle-Simulator-WebApp
```

---

### Schritt 2: Installieren

**Windows:**
1. Doppelklick auf: **`setup-windows.bat`**
2. Warte bis "Installation erfolgreich!" erscheint
3. Fertig! ✅

**Ubuntu/Linux:**
```bash
./setup-ubuntu.sh
```

**Android (Termux):**
```bash
./setup-android.sh
```

---

### Schritt 3: Spielen!

**Windows:**
1. Doppelklick auf: **`start-game.bat`**
2. Warte bis "Starte Server..." erscheint
3. Öffne deinen Browser (Chrome, Firefox, Edge, etc.)
4. Gehe zu: **http://localhost:3000**
5. **Fertig!** Das Spiel läuft! 🎮

**Ubuntu/Linux/Android:**
```bash
./start-game.sh
```
Dann im Browser: **http://localhost:3000**

---

## 🎮 Wie spielt man?

### 1. **Bots auswählen**
- Links siehst du **21 verschiedene Bots**
- Klicke auf einen Bot für **Agent 1** (dein Team)
- Scrolle runter und klicke auf einen Bot für **Agent 2** (Gegner)
- Jeder Bot hat:
  - **HP** (Lebenspunkte) - Wenn 0, verliert er!
  - **Stamina** (Ausdauer) - Für Aktionen
  - **ATK** (Angriff) - Wie stark er ist
  - **DEF** (Verteidigung) - Wie gut er sich schützt

### 2. **Battle starten**
- Scrolle ganz nach unten
- Klicke auf den großen **"Kampf Starten"** Button
- Der Battle-Screen öffnet sich!

### 3. **Aktionen wählen**
- Du siehst **8 verschiedene Aktionen**:
  - 🔥 **Feuerball** - Viel Schaden + Brennend-Effekt
  - 🧻 **Toilettenpapier-Tsunami** - Mittel Schaden + Klebrig
  - 🥤 **Smoothie-Attacke** - Wenig Schaden, wenig Stamina
  - 📧 **Meeting-Demoralisierung** - Schwächt Angriff
  - 🛡️ **Schreibtisch-Barrikade** - Erhöht Verteidigung
  - ☕ **Kaffee-Boost** - Heilt HP
  - 💻 **Laptop-Wurf** - Mittlerer Schaden
  - 📱 **Handy-Ablenkung** - Schwächt Gegner

- Klicke auf eine Aktion!
- Beide Agents führen gleichzeitig ihre Aktionen aus
- Schau zu wie HP/Stamina sich ändern!

### 4. **Gewinnen!**
- Der erste Agent der **0 HP** erreicht, verliert
- Der Victory-Screen zeigt den Gewinner! 🏆

---

## 🔄 Automatische Updates (Optional)

Damit das Spiel sich automatisch aktualisiert wenn neue Versionen rauskommen:

**Windows:**
1. Doppelklick auf: **`setup-auto-update-windows.bat`**
2. **WICHTIG:** Als Administrator ausführen (Rechtsklick → "Als Administrator ausführen")
3. Fertig! Das Spiel aktualisiert sich jetzt alle 10 Minuten automatisch

**Ubuntu/Linux:**
```bash
./setup-auto-update-ubuntu.sh
```

**Android (Termux):**
```bash
./setup-auto-update-android.sh
```

**Hinweis:** Termux muss im Hintergrund laufen! Aktiviere "Acquire wakelock" in den Termux-Einstellungen.

---

## ❓ Häufige Fragen

### **Das Spiel startet nicht!**
- **Windows:** Hast du Python installiert? (https://www.python.org/downloads/)
  - Bei Installation **"Add Python to PATH"** ankreuzen!
- **Ubuntu:** Installiere Python mit: `sudo apt install python3 python3-pip`
- **Android:** Installiere Termux von F-Droid (NICHT von Google Play!)

### **"localhost:3000" funktioniert nicht!**
- Läuft der Server? Schau ins Terminal-Fenster
- Steht da "Running on http://0.0.0.0:3000"? → Dann funktioniert es!
- Versuche: http://127.0.0.1:3000

### **Der Battle freezed!**
- Das ist gefixt! Lade die neueste Version herunter
- Oder aktiviere Auto-Update (siehe oben)

### **Ich sehe "undefined" im Spiel!**
- Das ist auch gefixt! Lade die neueste Version
- Oder aktiviere Auto-Update

### **Wie beende ich das Spiel?**
- **Windows:** Schließe das schwarze Terminal-Fenster
- **Ubuntu/Android:** Drücke `CTRL+C` im Terminal

---

## 🎨 Die 21 Bots

| Bot | Spezialität | Besonderheit |
|-----|-------------|--------------|
| 🔥 **Spark** | Burst Damage | Hoher Schaden in kurzer Zeit |
| 🛡️ **Sentinel** | Tank | Viel HP, hohe Verteidigung |
| ⚡ **Blitz** | Speed | Schnelle Aktionen |
| 🧊 **Frost** | Control | Verlangsamt Gegner |
| 🌪️ **Tempest** | AoE | Flächenschaden |
| 🎭 **Mimic** | Versatile | Kopiert Gegner-Fähigkeiten |
| 🦾 **Titan** | Powerhouse | Rohe Kraft |
| 🧠 **Sage** | Strategic | Intelligente Züge |
| 🩹 **Medic** | Support | Heilt sich selbst |
| ⚗️ **Alchemist** | DoT | Schaden über Zeit |
| 🎯 **Sniper** | Precision | Kritische Treffer |
| 🌊 **Tsunami** | Overwhelming | Überwältigende Kraft |
| 🔮 **Oracle** | Foresight | Sieht Züge voraus |
| 🎪 **Jester** | Chaos | Unvorhersehbar |
| 🦅 **Falcon** | Mobility | Hohe Beweglichkeit |
| 🐻 **Grizzly** | Brawler | Nahkampf-Spezialist |
| 🦊 **Vixen** | Cunning | Listig und clever |
| 🐉 **Dragon** | Legendary | Legendäre Kraft |
| 🦈 **Shark** | Predator | Jäger-Instinkt |
| 😏 **Mende** | Sarcastic | Schwächt mit Sarkasmus |
| 🌟 **Nova** | Explosive | Explosive Kraft |

---

## 🆘 Hilfe & Support

**Probleme?**
- GitHub Issues: https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp/issues
- Email: kommuniverse@gmail.com

**Mehr Info:**
- Technische Doku: Siehe **README.md** (für Programmierer)
- Hackathon Projekt: https://github.com/KoMMb0t/Hackaton

---

## 🎉 Viel Spaß!

**Das Spiel ist komplett kostenlos und Open Source!**

Wenn es dir gefällt, gib dem Projekt einen ⭐ auf GitHub! 😊

---

*Erstellt mit ❤️ für den Manus Hackathon 2024*
