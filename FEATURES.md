# 🎮 Agent Battle Simulator - Feature Overview

## ✨ Neue Features (v2.0)

### 🤖 21 Einzigartige Bots

Jeder Bot hat:
- **Einzigartige Stats** (HP, Attack, Defense, Stamina Bonuses)
- **3 Spezielle Fähigkeiten**
- **1 Passive Fähigkeit** (Special)
- **Eigene Farbe** für visuelle Unterscheidung
- **Thematische Rolle** (Office Warrior, AI Agent, Gaming Legend, etc.)

#### Bot-Liste:

1. **Mende** - Der Sarkastische Meeting-Killer (Office Warrior)
   - Special: Spottet Gegner automatisch (Debuff Attack -2)
   - Farbe: Cyan (#00ffff)

2. **Effi** - Der Effizienz-Fanatiker (Speedrunner)
   - Special: Alle Aktionen kosten 15% weniger Stamina
   - Farbe: Grün (#00ff00)

3. **Prophet** - Der Vorhersage-Algorithmus (AI Agent)
   - Special: +20% Critical Hit Chance
   - Farbe: Blau (#0080ff)

4. **Regulus** - Der Regelwächter (Gaming Legend)
   - Special: Reflektiert 20% Schaden zurück
   - Farbe: Rot (#ff4444)

5. **Resource** - Der Ressourcen-Horter (Office Warrior)
   - Special: Regeneriert 5 Stamina pro Runde
   - Farbe: Orange (#ffaa00)

6. **Insight** - Der Daten-Analyst (AI Agent)
   - Special: Ignoriert 25% der Gegner-Defense
   - Farbe: Lila (#8800ff)

7. **Sentinel** - Der Unzerstörbare Wächter (Gaming Tank)
   - Special: Nimmt 25% weniger Schaden von allen Angriffen
   - Farbe: Dunkelrot (#ff0044)

8. **Eco** - Der Nachhaltige Kämpfer (Green Fighter)
   - Special: Regeneriert 5 HP pro Runde
   - Farbe: Hellgrün (#00ff44)

9. **Spark** - Der Burst-Damage Dealer (Gaming DPS)
   - Special: +40% Schaden alle 3 Runden (Burst)
   - Farbe: Orange-Rot (#ff8800)

10. **Connect** - Der Team-Koordinator (Support)
    - Special: Buffs halten 1 Runde länger
    - Farbe: Hellblau (#00aaff)

11. **Mentor** - Der Weise Lehrer (Wise Fighter)
    - Special: +30% XP Gain nach jedem Kampf
    - Farbe: Dunkelblau (#4400ff)

12. **Scholar** - Der Kampf-Forscher (Researcher)
    - Special: Debuffs auf Gegner dauern 1 Runde länger
    - Farbe: Magenta (#aa00ff)

13. **Fisc** - Der Buchhalter des Schmerzes (Office Warrior)
    - Special: Heilt 15% des verursachten Schadens
    - Farbe: Gelb (#ffff00)

14. **Aura** - Der Mystische Koordinator (Mystic)
    - Special: Alle Buffs sind 50% effektiver
    - Farbe: Pink (#ff44aa)

15. **Flow** - Der Fließende Kämpfer (Martial Artist)
    - Special: +30% Dodge Chance
    - Farbe: Türkis (#00ffaa)

16. **Pulse** - Der Rhythmus-Krieger (Rhythm Fighter)
    - Special: Schaden steigt mit jedem Treffer (+10%)
    - Farbe: Pink-Rot (#ff0088)

17. **Deal** - Der Verhandlungs-Meister (Negotiator)
    - Special: Reduziert Gegner-Schaden um 20%
    - Farbe: Braun-Orange (#aa4400)

18. **Aegis** - Der Schild-Träger (Guardian)
    - Special: 50% Chance ersten Angriff zu blocken
    - Farbe: Königsblau (#0044ff)

19. **Certify** - Der Qualitäts-Prüfer (Quality Assurance)
    - Special: Angriffe haben garantierten Mindest-Schaden
    - Farbe: Gelbgrün (#44ff00)

20. **Volt** - Der Elektro-Schock (Electric Fighter)
    - Special: Schaden steigt jede Runde (+5%)
    - Farbe: Gold (#ffaa44)

21. **Genesis** - Der Schöpfer (Creator)
    - Special: Generiert zufälligen Buff jede Runde
    - Farbe: Violett (#8844ff)

---

### 🎨 Skin-System

Jeder Bot hat **5 Skins**, die durch Level-Ups freigeschaltet werden:

- **Level 1**: Standard Skin (immer verfügbar)
- **Level 5**: Skin 2 freigeschaltet
- **Level 10**: Skin 3 freigeschaltet
- **Level 15**: Skin 4 freigeschaltet
- **Level 20**: Legendary Skin freigeschaltet

**Beispiel (Mende):**
1. Standard - 😏
2. Business - 🤵
3. Troll - 👹
4. King - 🤴
5. Legend - 👑

---

### 📊 Level-Progression System

- **XP Bar** im Battle Screen
- **XP Gain** nach jedem Kampf
- **Level-Up** erhöht alle Stats:
  - +20 Max HP
  - +10 Max Stamina
  - +2 Attack
  - +2 Defense
- **Skin-Unlocks** bei bestimmten Levels

---

### 🎮 Bot-Auswahl Screen

- **Visuelles Grid** mit allen 21 Bots
- **Hover-Effekte** für bessere UX
- **Stats-Anzeige** für jeden Bot
- **Special-Fähigkeit** sichtbar
- **Farb-Kodierung** für visuelle Unterscheidung
- **Responsive Design** (Desktop & Mobile)

---

### ⚔️ Battle Screen Updates

- **Bot-Avatare** angezeigt (Emoji-basiert)
- **XP Bar** unter jedem Agent
- **Farb-Kodierung** basierend auf Bot
- **Level-Anzeige** prominent
- **Buff/Debuff Badges** mit Icons

---

## 🔧 Technische Details

### Backend (Python/Flask)
- `game/battle_bots.py` - 21 Bot-Definitionen
- `game/skins.py` - Skin-System mit Level-Unlocks
- `app.py` - Neue API Endpoints:
  - `GET /api/bots` - Alle Bots
  - `GET /api/bots/<id>/skins` - Alle Skins für Bot
  - `GET /api/bots/<id>/unlocked-skins/<level>` - Freigeschaltete Skins

### Frontend (Vanilla JS)
- `static/js/game.js` - Bot-Auswahl Logic
- `static/css/style.css` - Bot-Card Styles
- `templates/index.html` - Bot-Selection Screen

---

## 🎯 Hackathon-Ready Features

✅ **Multi-Agent System** (21 einzigartige Bots)  
✅ **Progression System** (Level-Ups, Skin-Unlocks)  
✅ **Visual Polish** (Avatare, Farben, Animationen)  
✅ **Strategic Depth** (Einzigartige Fähigkeiten pro Bot)  
✅ **Responsive Design** (Desktop & Mobile)  
✅ **RESTful API** (Gut dokumentiert)  
✅ **Open Source** (Apache 2.0 License)  

---

## 📈 Stats

- **21 Bots** mit einzigartigen Fähigkeiten
- **105 Skins** total (5 pro Bot)
- **63 Unique Abilities** (3 pro Bot)
- **21 Special Powers** (1 pro Bot)
- **8 Themen** (Office Warrior, AI Agent, Gaming Legend, etc.)
- **~3,000 Lines of Code** (Python + JavaScript + CSS)

---

## 🚀 Next Steps

1. **Teste lokal** auf deinem PC
2. **Deploy auf Replit/Render** für öffentliche Demo
3. **Submit zum Hackathon** auf Devpost
4. **Optional**: CLI Integration, Tournament System

---

**Made with ☕ and 🔥 for AI Champion Ship Hackathon**
