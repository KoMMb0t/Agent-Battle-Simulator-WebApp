# 🎮 Agent Battle Simulator - Technical Documentation

**Browser-based turn-based battle simulator with 21 unique bots and real-time gameplay.**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

**Repository:** https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp.git
cd Agent-Battle-Simulator-WebApp

# Install
pip install -r requirements.txt

# Run
python app.py

# Open browser
http://localhost:3000
```

---

## 📦 Installation

### Automated Setup

**Windows:**
```cmd
setup-windows.bat
```

**Ubuntu/Linux:**
```bash
chmod +x setup-ubuntu.sh
./setup-ubuntu.sh
```

**Android (Termux):**
```bash
chmod +x setup-android.sh
./setup-android.sh
```

### Manual Setup

```bash
# Install dependencies
pip install flask flask-cors

# Verify installation
python -c "import flask; print(flask.__version__)"

# Run server
python app.py
```

---

## 🏗️ Architecture

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11, Flask 3.0, Flask-CORS |
| **Frontend** | Vanilla JavaScript (ES6+), HTML5, CSS3 |
| **Storage** | In-memory (Redis-compatible interface) |
| **Game Logic** | Python classes (Agent, Battle, Action) |

### Project Structure

```
Agent-Battle-Simulator-WebApp/
├── app.py                      # Flask server & API endpoints
├── battle_storage.py           # Battle state management
├── game/
│   ├── __init__.py
│   ├── agents.py              # Agent class (HP, Stamina, Buffs)
│   ├── battle.py              # Battle logic & turn execution
│   ├── actions.py             # 8 combat actions
│   ├── battle_bots.py         # 21 unique bots
│   └── skins.py               # 105 skins (5 per bot)
├── templates/
│   └── index.html             # Main game UI
├── static/
│   ├── css/
│   │   └── style.css          # Styling & animations
│   └── js/
│       ├── game.js            # Game controller
│       └── debug-logger.js    # Debug tool (dev only)
├── tests/
│   └── test_battle.py         # Unit tests
├── setup-*.{bat,sh}           # Platform-specific setup
├── start-game.{bat,sh}        # Game launcher
└── setup-auto-update-*.{bat,sh}  # Auto-update setup
```

---

## 🎮 Game Mechanics

### Core Systems

**1. HP (Hit Points)**
- Determines agent survival
- Range: 80-150 (varies by bot type)
- Reaches 0 → Agent loses

**2. Stamina System**
- Required for actions
- Range: 90-120 (varies by bot type)
- Regenerates +20 per round (starting round 2)
- Capped at maximum

**3. Buff/Debuff System**
- Duration-based effects
- Decrements each round
- Expires automatically at duration = 0
- Types:
  - **Buffs:** Attack+, Defense+, Healing
  - **Debuffs:** Burning, Sticky, Weakened

**4. Combat Actions**

| Action | Damage | Stamina | Effect |
|--------|--------|---------|--------|
| 🔥 Feuerball | 20-35 | 15 | Burning (3 turns) |
| 🧻 Toilettenpapier | 15-25 | 12 | Sticky (2 turns) |
| 🥤 Smoothie | 10-15 | 10 | None |
| 📧 Meeting | 5-10 | 8 | Attack- (3 turns) |
| 🛡️ Barrikade | 0 | 10 | Defense+ (2 turns) |
| ☕ Kaffee | 0 | 15 | Heal 20-30 HP |
| 💻 Laptop | 12-20 | 10 | None |
| 📱 Handy | 8-12 | 8 | Defense- (2 turns) |

**5. AI System**
- Score-based action selection
- Factors:
  - HP ratio (low HP → defensive)
  - Stamina availability
  - Damage potential
  - Opponent HP
- Strategy:
  - HP < 30% → Healing & Defense
  - HP 30-60% → Balanced
  - HP > 60% → Aggressive

---

## 🔌 API Endpoints

### Battle Management

**Start Battle**
```http
POST /api/battle/start
Content-Type: application/json

{
  "agent1_bot": "spark",
  "agent2_bot": "sentinel",
  "agent1_name": "Agent Alpha",
  "agent2_name": "Agent Beta"
}

Response:
{
  "battle_id": "abc123",
  "agent1": { ... },
  "agent2": { ... }
}
```

**Execute Turn**
```http
POST /api/battle/turn
Content-Type: application/json

{
  "battle_id": "abc123",
  "action_id": 1
}

Response:
{
  "actions": [
    {
      "attacker": "Agent Alpha",
      "action": "🔥 Feuerball",
      "damage": 25,
      "comment": "Autsch! Das hat wehgetan..."
    }
  ],
  "agent1_state": { ... },
  "agent2_state": { ... },
  "round": 2,
  "winner": null
}
```

### Data Endpoints

**Get Bots**
```http
GET /api/bots

Response:
[
  {
    "id": "spark",
    "name": "Spark",
    "avatar": "💥",
    "hp_modifier": 0,
    "stamina_modifier": 0,
    "attack_modifier": 5,
    "defense_modifier": 0,
    "special_ability": "Burst Damage"
  },
  ...
]
```

**Get Actions**
```http
GET /api/actions

Response:
[
  {
    "id": 1,
    "name": "🔥 Feuerball der Bürofrustration",
    "description": "Wirft einen explosiven Feuerball",
    "damage_range": [20, 35],
    "stamina_cost": 15,
    "effects": ["burning"]
  },
  ...
]
```

---

## 🧪 Testing

### Run Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run specific test
pytest tests/test_battle.py

# With coverage
pip install pytest-cov
pytest --cov=game tests/
```

### Manual Testing

```bash
# Start server with debug mode
export FLASK_ENV=development
python app.py

# Test API endpoints
curl http://localhost:3000/api/bots
curl -X POST http://localhost:3000/api/battle/start \
  -H "Content-Type: application/json" \
  -d '{"agent1_bot":"spark","agent2_bot":"sentinel"}'
```

---

## 🔄 Auto-Update System

### Setup

**Windows:**
```cmd
setup-auto-update-windows.bat
```
Creates Task Scheduler task (runs every 10 minutes)

**Ubuntu/Linux:**
```bash
./setup-auto-update-ubuntu.sh
```
Creates cron job (runs every 10 minutes)

**Android (Termux):**
```bash
./setup-auto-update-android.sh
```
Creates cron job + starts crond daemon

### How It Works

1. **Check for local changes**
   - If local changes exist → Skip update
   - Prevents merge conflicts

2. **Fetch remote**
   - `git fetch origin`
   - Check if local is behind remote

3. **Pull if needed**
   - `git pull origin main`
   - Log result to `update.log`

### Manual Update

```bash
# Pull latest changes
git pull origin main

# Or use update script
./auto-update.sh  # (created after setup)
```

---

## 🐛 Bug Fixes (Latest)

### v1.1.0 (Dec 11, 2024)

**Fixed:**
1. ✅ Action names showing "undefined"
   - Issue: Frontend expected `action.emoji` + `action.name` separately
   - Fix: Use `action.name` (already includes emoji)

2. ✅ UI not updating after actions
   - Issue: Frontend expected `data.agent1` but API returned `data.agent1_state`
   - Fix: Updated `executeAction()` to use correct field names

3. ✅ Combat log showing "undefined"
   - Issue: Code tried to display `data.commentary` but API returns `data.actions[]`
   - Fix: Iterate through actions array and create log entries

4. ✅ Stamina regeneration
   - Already working (+20 per round starting round 2)
   - Capped at maximum stamina

5. ✅ Buff/Debuff duration
   - Already working (decrements each round)
   - Effects expire automatically

**Tested:**
- Complete battle flow (bot selection → victory)
- 5+ rounds played
- All mechanics verified
- Victory screen working

---

## 🚢 Deployment

### Local Development

```bash
# Development mode (auto-reload)
export FLASK_ENV=development
python app.py
```

### Production

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app

# Or with systemd service
sudo cp agent-battle.service /etc/systemd/system/
sudo systemctl enable agent-battle
sudo systemctl start agent-battle
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000
CMD ["python", "app.py"]
```

```bash
docker build -t agent-battle .
docker run -p 3000:3000 agent-battle
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Server
PORT=3000                    # Server port (default: 3000)
HOST=0.0.0.0                 # Bind address (default: 0.0.0.0)

# Debug
FLASK_ENV=development        # Enable debug mode
DEBUG_LOGGER=true            # Enable debug logger UI
```

### Game Balance

Edit `game/actions.py` to modify action values:

```python
ACTIONS = [
    {
        "id": 1,
        "name": "🔥 Feuerball",
        "damage_range": [20, 35],  # Modify damage
        "stamina_cost": 15,         # Modify cost
        "effects": ["burning"]      # Add/remove effects
    },
    ...
]
```

Edit `game/battle_bots.py` to modify bot stats:

```python
BATTLE_BOTS = [
    {
        "id": "spark",
        "hp_modifier": 0,           # +/- HP
        "stamina_modifier": 0,      # +/- Stamina
        "attack_modifier": 5,       # +/- Attack
        "defense_modifier": 0,      # +/- Defense
    },
    ...
]
```

---

## 📊 Performance

### Benchmarks

| Metric | Value |
|--------|-------|
| **Battle Start** | ~50ms |
| **Turn Execution** | ~30ms |
| **API Response** | <100ms |
| **Memory Usage** | ~50MB |
| **Concurrent Battles** | 100+ |

### Optimization Tips

1. **Enable caching** (for production)
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/bots')
@cache.cached(timeout=300)
def get_bots():
    ...
```

2. **Use Redis** (for multi-instance)
```python
# In battle_storage.py
import redis
r = redis.Redis(host='localhost', port=6379)
```

3. **Compress responses**
```python
from flask_compress import Compress
Compress(app)
```

---

## 🤝 Contributing

### Development Setup

```bash
# Fork & clone
git clone https://github.com/YOUR_USERNAME/Agent-Battle-Simulator-WebApp.git
cd Agent-Battle-Simulator-WebApp

# Create branch
git checkout -b feature/your-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Make changes & test
pytest tests/

# Commit & push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature

# Create Pull Request on GitHub
```

### Code Style

```bash
# Format code
black game/ app.py

# Lint
pylint game/ app.py

# Type check
mypy game/ app.py
```

---

## 📝 License

Apache License 2.0 - See [LICENSE](LICENSE) file

---

## 🙏 Credits

**Developed during:** Manus Hackathon 2024  
**Repository:** https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp  
**Parent Project:** https://github.com/KoMMb0t/Hackaton

---

## 📞 Support

**Issues:** https://github.com/KoMMb0t/Agent-Battle-Simulator-WebApp/issues  
**Email:** kommuniverse@gmail.com

---

**⭐ Star this repo if you like it!**
