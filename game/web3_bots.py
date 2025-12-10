"""
Agent Battle Simulator - 21 Web3 Bots
Mixed themes: Office Warriors, AI Agents, Gaming Legends
"""

WEB3_BOTS = [
    {
        "id": "mende",
        "name": "Mende",
        "title": "Der Sarkastische Meeting-Killer",
        "description": "Tötet Gegner mit sarkastischen Bemerkungen und Meeting-Einladungen",
        "avatar": "😏",
        "color": "#00ffff",
        "theme": "Office Warrior",
        "stats": {
            "hp_bonus": 10,
            "stamina_bonus": 15,
            "attack_bonus": 6,
            "defense_bonus": 3
        },
        "abilities": [
            "Sarkasmus-Schlag: +20% Schaden gegen demoralisierte Gegner",
            "Meeting-Einladung: Verlangsamt Gegner für 2 Runden",
            "+20% XP Gain"
        ],
        "special": "Spottet Gegner automatisch (Debuff Attack -2)"
    },
    {
        "id": "effi",
        "name": "Effi",
        "title": "Der Effizienz-Fanatiker",
        "description": "Optimiert jeden Angriff auf maximale Effizienz",
        "avatar": "⚡",
        "color": "#00ff00",
        "theme": "Speedrunner",
        "stats": {
            "hp_bonus": 5,
            "stamina_bonus": 25,
            "attack_bonus": 5,
            "defense_bonus": 2
        },
        "abilities": [
            "Stamina-Optimierung: -15% Stamina Kosten für alle Aktionen",
            "Quick Strike: Chance auf Doppel-Angriff (20%)",
            "Effizienz-Boost: +10% Schaden"
        ],
        "special": "Alle Aktionen kosten 15% weniger Stamina"
    },
    {
        "id": "prophet",
        "name": "Prophet",
        "title": "Der Vorhersage-Algorithmus",
        "description": "Sieht die Zukunft und trifft immer ins Schwarze",
        "avatar": "🔮",
        "color": "#0080ff",
        "theme": "AI Agent",
        "stats": {
            "hp_bonus": 8,
            "stamina_bonus": 12,
            "attack_bonus": 7,
            "defense_bonus": 4
        },
        "abilities": [
            "Kritischer Treffer: +20% Critical Hit Chance",
            "Vorhersage: Sieht Gegner-Aktion voraus (Dodge +15%)",
            "Trend-Analyse: +15% Schaden"
        ],
        "special": "+20% Critical Hit Chance"
    },
    {
        "id": "regulus",
        "name": "Regulus",
        "title": "Der Regelwächter",
        "description": "Bestraft Regelbrecher mit eiserner Faust",
        "avatar": "⚖️",
        "color": "#ff4444",
        "theme": "Gaming Legend",
        "stats": {
            "hp_bonus": 20,
            "stamina_bonus": 5,
            "attack_bonus": 4,
            "defense_bonus": 8
        },
        "abilities": [
            "Regel-Durchsetzung: Reflektiert 20% des erhaltenen Schadens",
            "Bestrafung: +25% Schaden gegen Buff-Gegner",
            "Unbestechlich: Immun gegen Debuffs (50% Chance)"
        ],
        "special": "Reflektiert 20% Schaden zurück"
    },
    {
        "id": "resource",
        "name": "Resource",
        "title": "Der Ressourcen-Horter",
        "description": "Sammelt und verwaltet Ressourcen wie ein Drache sein Gold",
        "avatar": "💰",
        "color": "#ffaa00",
        "theme": "Office Warrior",
        "stats": {
            "hp_bonus": 15,
            "stamina_bonus": 20,
            "attack_bonus": 3,
            "defense_bonus": 5
        },
        "abilities": [
            "Ressourcen-Sammlung: +5 Stamina pro Runde",
            "Gold-Panzer: +15% Defense",
            "Investition: Heilt 3 HP pro Runde"
        ],
        "special": "Regeneriert 5 Stamina pro Runde"
    },
    {
        "id": "insight",
        "name": "Insight",
        "title": "Der Daten-Analyst",
        "description": "Analysiert Schwachstellen und nutzt sie gnadenlos aus",
        "avatar": "📊",
        "color": "#8800ff",
        "theme": "AI Agent",
        "stats": {
            "hp_bonus": 7,
            "stamina_bonus": 18,
            "attack_bonus": 8,
            "defense_bonus": 3
        },
        "abilities": [
            "Schwachstellen-Analyse: +30% Schaden gegen geschwächte Gegner",
            "Daten-Mining: Sieht Gegner-Stats",
            "Präzisions-Schlag: Ignoriert 25% Defense"
        ],
        "special": "Ignoriert 25% der Gegner-Defense"
    },
    {
        "id": "sentinel",
        "name": "Sentinel",
        "title": "Der Unzerstörbare Wächter",
        "description": "Steht wie eine Mauer und lässt niemanden durch",
        "avatar": "🛡️",
        "color": "#ff0044",
        "theme": "Gaming Tank",
        "stats": {
            "hp_bonus": 35,
            "stamina_bonus": 0,
            "attack_bonus": 2,
            "defense_bonus": 10
        },
        "abilities": [
            "Eiserne Mauer: -25% erhaltener Schaden",
            "Gegen-Schlag: Kontert Angriffe (30% Chance)",
            "Unerschütterlich: +20% Defense"
        ],
        "special": "Nimmt 25% weniger Schaden von allen Angriffen"
    },
    {
        "id": "eco",
        "name": "Eco",
        "title": "Der Nachhaltige Kämpfer",
        "description": "Kämpft im Einklang mit der Natur und regeneriert sich selbst",
        "avatar": "🌱",
        "color": "#00ff44",
        "theme": "Green Fighter",
        "stats": {
            "hp_bonus": 12,
            "stamina_bonus": 15,
            "attack_bonus": 4,
            "defense_bonus": 6
        },
        "abilities": [
            "Regeneration: Heilt 5 HP pro Runde",
            "Natur-Kraft: +15% Schaden",
            "Recycling: Konvertiert Schaden zu Stamina (10%)"
        ],
        "special": "Regeneriert 5 HP pro Runde"
    },
    {
        "id": "spark",
        "name": "Spark",
        "title": "Der Burst-Damage Dealer",
        "description": "Entfesselt explosive Schadens-Kombos",
        "avatar": "💥",
        "color": "#ff8800",
        "theme": "Gaming DPS",
        "stats": {
            "hp_bonus": 5,
            "stamina_bonus": 10,
            "attack_bonus": 10,
            "defense_bonus": 1
        },
        "abilities": [
            "Burst-Combo: +40% Schaden alle 3 Runden",
            "Kritischer Funke: +25% Critical Hit Chance",
            "Glass Cannon: +20% Schaden, -10% Defense"
        ],
        "special": "+40% Schaden alle 3 Runden (Burst)"
    },
    {
        "id": "connect",
        "name": "Connect",
        "title": "Der Team-Koordinator",
        "description": "Koordiniert Angriffe und stärkt Verbündete",
        "avatar": "🤝",
        "color": "#00aaff",
        "theme": "Support",
        "stats": {
            "hp_bonus": 10,
            "stamina_bonus": 20,
            "attack_bonus": 4,
            "defense_bonus": 5
        },
        "abilities": [
            "Team-Buff: +10% Stats für alle Verbündeten",
            "Koordination: Reduziert Cooldowns um 1 Runde",
            "Moral-Boost: Heilt 10 HP bei Sieg"
        ],
        "special": "Buffs halten 1 Runde länger"
    },
    {
        "id": "mentor",
        "name": "Mentor",
        "title": "Der Weise Lehrer",
        "description": "Lehrt Gegner das Fürchten durch überlegene Technik",
        "avatar": "📚",
        "color": "#4400ff",
        "theme": "Wise Fighter",
        "stats": {
            "hp_bonus": 15,
            "stamina_bonus": 15,
            "attack_bonus": 5,
            "defense_bonus": 6
        },
        "abilities": [
            "Weisheit: +30% XP Gain",
            "Lehrstunde: Debufft Gegner-Attack (-3)",
            "Erfahrung: +10% Stats pro Level"
        ],
        "special": "+30% XP Gain nach jedem Kampf"
    },
    {
        "id": "scholar",
        "name": "Scholar",
        "title": "Der Blockchain-Forscher",
        "description": "Erforscht Kampfmuster und optimiert Strategien",
        "avatar": "🔬",
        "color": "#aa00ff",
        "theme": "Researcher",
        "stats": {
            "hp_bonus": 8,
            "stamina_bonus": 22,
            "attack_bonus": 6,
            "defense_bonus": 4
        },
        "abilities": [
            "Forschung: Lernt Gegner-Muster (Dodge +20%)",
            "Analyse: +25% Schaden nach 3 Runden",
            "Wissen: Debuffs dauern 1 Runde länger"
        ],
        "special": "Debuffs auf Gegner dauern 1 Runde länger"
    },
    {
        "id": "fisc",
        "name": "Fisc",
        "title": "Der Buchhalter des Schmerzes",
        "description": "Rechnet jeden Schaden genau ab",
        "avatar": "🧮",
        "color": "#ffff00",
        "theme": "Office Warrior",
        "stats": {
            "hp_bonus": 10,
            "stamina_bonus": 18,
            "attack_bonus": 7,
            "defense_bonus": 4
        },
        "abilities": [
            "Präzisions-Rechnung: Schaden ist immer genau berechenbar (kein RNG)",
            "Steuer-Rückzahlung: Heilt 15% des verursachten Schadens",
            "Audit: Sieht alle Gegner-Buffs/Debuffs"
        ],
        "special": "Heilt 15% des verursachten Schadens"
    },
    {
        "id": "aura",
        "name": "Aura",
        "title": "Der Mystische Koordinator",
        "description": "Umgibt sich mit mächtigen Auren",
        "avatar": "✨",
        "color": "#ff44aa",
        "theme": "Mystic",
        "stats": {
            "hp_bonus": 12,
            "stamina_bonus": 16,
            "attack_bonus": 5,
            "defense_bonus": 7
        },
        "abilities": [
            "Schutz-Aura: -15% erhaltener Schaden",
            "Angriffs-Aura: +15% Schaden",
            "Mystische Präsenz: Buffs sind 50% effektiver"
        ],
        "special": "Alle Buffs sind 50% effektiver"
    },
    {
        "id": "flow",
        "name": "Flow",
        "title": "Der Fließende Kämpfer",
        "description": "Bewegt sich wie Wasser und weicht allem aus",
        "avatar": "🌊",
        "color": "#00ffaa",
        "theme": "Martial Artist",
        "stats": {
            "hp_bonus": 8,
            "stamina_bonus": 25,
            "attack_bonus": 6,
            "defense_bonus": 3
        },
        "abilities": [
            "Fließende Bewegung: +30% Dodge Chance",
            "Wasser-Schlag: Ignoriert Panzerung",
            "Im Flow: +20% Stamina Regeneration"
        ],
        "special": "+30% Dodge Chance"
    },
    {
        "id": "pulse",
        "name": "Pulse",
        "title": "Der Rhythmus-Krieger",
        "description": "Kämpft im Takt und trifft jeden Beat",
        "avatar": "🎵",
        "color": "#ff0088",
        "theme": "Rhythm Fighter",
        "stats": {
            "hp_bonus": 10,
            "stamina_bonus": 15,
            "attack_bonus": 8,
            "defense_bonus": 3
        },
        "abilities": [
            "Rhythmus-Combo: +10% Schaden pro Treffer (stackt)",
            "Beat Drop: Massive Schaden-Spitze (50% mehr)",
            "Takt-Gefühl: +15% Critical Hit Chance"
        ],
        "special": "Schaden steigt mit jedem Treffer (+10%)"
    },
    {
        "id": "deal",
        "name": "Deal",
        "title": "Der Verhandlungs-Meister",
        "description": "Verhandelt selbst im Kampf und findet immer einen Vorteil",
        "avatar": "🤑",
        "color": "#aa4400",
        "theme": "Negotiator",
        "stats": {
            "hp_bonus": 15,
            "stamina_bonus": 12,
            "attack_bonus": 6,
            "defense_bonus": 5
        },
        "abilities": [
            "Verhandlung: Reduziert Gegner-Schaden um 20%",
            "Win-Win: Heilt beide Kämpfer (aber sich selbst mehr)",
            "Geschäftssinn: +25% XP Gain"
        ],
        "special": "Reduziert Gegner-Schaden um 20%"
    },
    {
        "id": "aegis",
        "name": "Aegis",
        "title": "Der Schild-Träger",
        "description": "Trägt einen unzerstörbaren Schild",
        "avatar": "🛡️",
        "color": "#0044ff",
        "theme": "Guardian",
        "stats": {
            "hp_bonus": 30,
            "stamina_bonus": 5,
            "attack_bonus": 3,
            "defense_bonus": 12
        },
        "abilities": [
            "Aegis-Schild: Blockt ersten Angriff jeder Runde (50%)",
            "Schild-Schlag: Kontert mit Defense-Wert",
            "Unbreakable: +25% Defense"
        ],
        "special": "50% Chance ersten Angriff zu blocken"
    },
    {
        "id": "certify",
        "name": "Certify",
        "title": "Der Qualitäts-Prüfer",
        "description": "Prüft jeden Angriff auf Qualität",
        "avatar": "✅",
        "color": "#44ff00",
        "theme": "Quality Assurance",
        "stats": {
            "hp_bonus": 12,
            "stamina_bonus": 18,
            "attack_bonus": 7,
            "defense_bonus": 4
        },
        "abilities": [
            "Qualitäts-Check: Angriffe haben garantierten Mindest-Schaden",
            "Bug-Fix: Entfernt negative Debuffs",
            "Zertifizierung: +20% Schaden"
        ],
        "special": "Angriffe haben garantierten Mindest-Schaden"
    },
    {
        "id": "volt",
        "name": "Volt",
        "title": "Der Elektro-Schock",
        "description": "Lädt sich auf und entlädt explosive Energie",
        "avatar": "⚡",
        "color": "#ffaa44",
        "theme": "Electric Fighter",
        "stats": {
            "hp_bonus": 8,
            "stamina_bonus": 20,
            "attack_bonus": 9,
            "defense_bonus": 2
        },
        "abilities": [
            "Aufladung: +5% Schaden pro Runde (stackt)",
            "Elektro-Schock: Betäubt Gegner (Skip Turn 20%)",
            "Überspannung: +30% Schaden bei voller Stamina"
        ],
        "special": "Schaden steigt jede Runde (+5%)"
    },
    {
        "id": "genesis",
        "name": "Genesis",
        "title": "Der Schöpfer",
        "description": "Erschafft neue Kampfstrategien aus dem Nichts",
        "avatar": "🌟",
        "color": "#8844ff",
        "theme": "Creator",
        "stats": {
            "hp_bonus": 15,
            "stamina_bonus": 15,
            "attack_bonus": 7,
            "defense_bonus": 6
        },
        "abilities": [
            "Schöpfung: Generiert zufälligen Buff jede Runde",
            "Neustart: Heilt 20 HP alle 5 Runden",
            "Allmacht: Alle Stats +10%"
        ],
        "special": "Generiert zufälligen Buff jede Runde"
    }
]

def get_web3_bot(bot_id: str):
    """Get bot by ID"""
    for bot in WEB3_BOTS:
        if bot['id'] == bot_id:
            return bot
    return WEB3_BOTS[3]  # Default: Regulus

def get_all_web3_bots():
    """Get all available bots"""
    return WEB3_BOTS
