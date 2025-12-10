"""
Agent Battle Simulator - Skin System
Skins werden durch Level-Ups freigeschaltet
"""

# Skin-Definitionen für jeden Bot
# Format: bot_id -> [skins]
BOT_SKINS = {
    "mende": [
        {"id": 1, "name": "Standard", "avatar": "😏", "unlock_level": 1},
        {"id": 2, "name": "Business", "avatar": "🤵", "unlock_level": 5},
        {"id": 3, "name": "Troll", "avatar": "👹", "unlock_level": 10},
        {"id": 4, "name": "King", "avatar": "🤴", "unlock_level": 15},
        {"id": 5, "name": "Legend", "avatar": "👑", "unlock_level": 20}
    ],
    "effi": [
        {"id": 1, "name": "Standard", "avatar": "⚡", "unlock_level": 1},
        {"id": 2, "name": "Turbo", "avatar": "🚀", "unlock_level": 5},
        {"id": 3, "name": "Lightning", "avatar": "⚡", "unlock_level": 10},
        {"id": 4, "name": "Flash", "avatar": "💨", "unlock_level": 15},
        {"id": 5, "name": "Sonic", "avatar": "🌪️", "unlock_level": 20}
    ],
    "prophet": [
        {"id": 1, "name": "Standard", "avatar": "🔮", "unlock_level": 1},
        {"id": 2, "name": "Mystic", "avatar": "🧙", "unlock_level": 5},
        {"id": 3, "name": "Oracle", "avatar": "👁️", "unlock_level": 10},
        {"id": 4, "name": "Seer", "avatar": "🌙", "unlock_level": 15},
        {"id": 5, "name": "Omniscient", "avatar": "✨", "unlock_level": 20}
    ],
    "regulus": [
        {"id": 1, "name": "Standard", "avatar": "⚖️", "unlock_level": 1},
        {"id": 2, "name": "Judge", "avatar": "👨‍⚖️", "unlock_level": 5},
        {"id": 3, "name": "Enforcer", "avatar": "🚔", "unlock_level": 10},
        {"id": 4, "name": "Warden", "avatar": "🏛️", "unlock_level": 15},
        {"id": 5, "name": "Supreme", "avatar": "⚡", "unlock_level": 20}
    ],
    "resource": [
        {"id": 1, "name": "Standard", "avatar": "💰", "unlock_level": 1},
        {"id": 2, "name": "Banker", "avatar": "🏦", "unlock_level": 5},
        {"id": 3, "name": "Tycoon", "avatar": "💎", "unlock_level": 10},
        {"id": 4, "name": "Mogul", "avatar": "🤑", "unlock_level": 15},
        {"id": 5, "name": "Dragon", "avatar": "🐉", "unlock_level": 20}
    ],
    "insight": [
        {"id": 1, "name": "Standard", "avatar": "📊", "unlock_level": 1},
        {"id": 2, "name": "Analyst", "avatar": "📈", "unlock_level": 5},
        {"id": 3, "name": "Detective", "avatar": "🕵️", "unlock_level": 10},
        {"id": 4, "name": "Mastermind", "avatar": "🧠", "unlock_level": 15},
        {"id": 5, "name": "AI Core", "avatar": "🤖", "unlock_level": 20}
    ],
    "sentinel": [
        {"id": 1, "name": "Standard", "avatar": "🛡️", "unlock_level": 1},
        {"id": 2, "name": "Knight", "avatar": "⚔️", "unlock_level": 5},
        {"id": 3, "name": "Paladin", "avatar": "🏰", "unlock_level": 10},
        {"id": 4, "name": "Guardian", "avatar": "👼", "unlock_level": 15},
        {"id": 5, "name": "Titan", "avatar": "🗿", "unlock_level": 20}
    ],
    "eco": [
        {"id": 1, "name": "Standard", "avatar": "🌱", "unlock_level": 1},
        {"id": 2, "name": "Gardener", "avatar": "🌿", "unlock_level": 5},
        {"id": 3, "name": "Druid", "avatar": "🍃", "unlock_level": 10},
        {"id": 4, "name": "Nature", "avatar": "🌳", "unlock_level": 15},
        {"id": 5, "name": "Gaia", "avatar": "🌍", "unlock_level": 20}
    ],
    "spark": [
        {"id": 1, "name": "Standard", "avatar": "💥", "unlock_level": 1},
        {"id": 2, "name": "Bomber", "avatar": "💣", "unlock_level": 5},
        {"id": 3, "name": "Explosive", "avatar": "🧨", "unlock_level": 10},
        {"id": 4, "name": "Nuclear", "avatar": "☢️", "unlock_level": 15},
        {"id": 5, "name": "Supernova", "avatar": "🌟", "unlock_level": 20}
    ],
    "connect": [
        {"id": 1, "name": "Standard", "avatar": "🤝", "unlock_level": 1},
        {"id": 2, "name": "Networker", "avatar": "🌐", "unlock_level": 5},
        {"id": 3, "name": "Leader", "avatar": "👔", "unlock_level": 10},
        {"id": 4, "name": "Commander", "avatar": "🎖️", "unlock_level": 15},
        {"id": 5, "name": "Hivemind", "avatar": "🧬", "unlock_level": 20}
    ],
    "mentor": [
        {"id": 1, "name": "Standard", "avatar": "📚", "unlock_level": 1},
        {"id": 2, "name": "Teacher", "avatar": "👨‍🏫", "unlock_level": 5},
        {"id": 3, "name": "Professor", "avatar": "🎓", "unlock_level": 10},
        {"id": 4, "name": "Master", "avatar": "🧙‍♂️", "unlock_level": 15},
        {"id": 5, "name": "Sage", "avatar": "👴", "unlock_level": 20}
    ],
    "scholar": [
        {"id": 1, "name": "Standard", "avatar": "🔬", "unlock_level": 1},
        {"id": 2, "name": "Researcher", "avatar": "🧪", "unlock_level": 5},
        {"id": 3, "name": "Scientist", "avatar": "👨‍🔬", "unlock_level": 10},
        {"id": 4, "name": "Genius", "avatar": "💡", "unlock_level": 15},
        {"id": 5, "name": "Einstein", "avatar": "🌌", "unlock_level": 20}
    ],
    "fisc": [
        {"id": 1, "name": "Standard", "avatar": "🧮", "unlock_level": 1},
        {"id": 2, "name": "Accountant", "avatar": "💼", "unlock_level": 5},
        {"id": 3, "name": "Auditor", "avatar": "📋", "unlock_level": 10},
        {"id": 4, "name": "CFO", "avatar": "💵", "unlock_level": 15},
        {"id": 5, "name": "Taxman", "avatar": "👨‍💼", "unlock_level": 20}
    ],
    "aura": [
        {"id": 1, "name": "Standard", "avatar": "✨", "unlock_level": 1},
        {"id": 2, "name": "Mystic", "avatar": "🔮", "unlock_level": 5},
        {"id": 3, "name": "Enchanter", "avatar": "🪄", "unlock_level": 10},
        {"id": 4, "name": "Archmage", "avatar": "🧙‍♀️", "unlock_level": 15},
        {"id": 5, "name": "Celestial", "avatar": "⭐", "unlock_level": 20}
    ],
    "flow": [
        {"id": 1, "name": "Standard", "avatar": "🌊", "unlock_level": 1},
        {"id": 2, "name": "Stream", "avatar": "💧", "unlock_level": 5},
        {"id": 3, "name": "River", "avatar": "🏞️", "unlock_level": 10},
        {"id": 4, "name": "Ocean", "avatar": "🌊", "unlock_level": 15},
        {"id": 5, "name": "Tsunami", "avatar": "🌀", "unlock_level": 20}
    ],
    "pulse": [
        {"id": 1, "name": "Standard", "avatar": "🎵", "unlock_level": 1},
        {"id": 2, "name": "DJ", "avatar": "🎧", "unlock_level": 5},
        {"id": 3, "name": "Rockstar", "avatar": "🎸", "unlock_level": 10},
        {"id": 4, "name": "Maestro", "avatar": "🎼", "unlock_level": 15},
        {"id": 5, "name": "Symphony", "avatar": "🎻", "unlock_level": 20}
    ],
    "deal": [
        {"id": 1, "name": "Standard", "avatar": "🤑", "unlock_level": 1},
        {"id": 2, "name": "Trader", "avatar": "📈", "unlock_level": 5},
        {"id": 3, "name": "Broker", "avatar": "💹", "unlock_level": 10},
        {"id": 4, "name": "Tycoon", "avatar": "🏢", "unlock_level": 15},
        {"id": 5, "name": "Monopoly", "avatar": "🎩", "unlock_level": 20}
    ],
    "aegis": [
        {"id": 1, "name": "Standard", "avatar": "🛡️", "unlock_level": 1},
        {"id": 2, "name": "Defender", "avatar": "🔰", "unlock_level": 5},
        {"id": 3, "name": "Protector", "avatar": "🦾", "unlock_level": 10},
        {"id": 4, "name": "Fortress", "avatar": "🏰", "unlock_level": 15},
        {"id": 5, "name": "Invincible", "avatar": "⚡", "unlock_level": 20}
    ],
    "certify": [
        {"id": 1, "name": "Standard", "avatar": "✅", "unlock_level": 1},
        {"id": 2, "name": "Tester", "avatar": "🧪", "unlock_level": 5},
        {"id": 3, "name": "QA Lead", "avatar": "📋", "unlock_level": 10},
        {"id": 4, "name": "Inspector", "avatar": "🔍", "unlock_level": 15},
        {"id": 5, "name": "Perfect", "avatar": "💯", "unlock_level": 20}
    ],
    "volt": [
        {"id": 1, "name": "Standard", "avatar": "⚡", "unlock_level": 1},
        {"id": 2, "name": "Static", "avatar": "🔌", "unlock_level": 5},
        {"id": 3, "name": "Thunder", "avatar": "⛈️", "unlock_level": 10},
        {"id": 4, "name": "Storm", "avatar": "🌩️", "unlock_level": 15},
        {"id": 5, "name": "Zeus", "avatar": "⚡", "unlock_level": 20}
    ],
    "genesis": [
        {"id": 1, "name": "Standard", "avatar": "🌟", "unlock_level": 1},
        {"id": 2, "name": "Creator", "avatar": "🎨", "unlock_level": 5},
        {"id": 3, "name": "Architect", "avatar": "🏗️", "unlock_level": 10},
        {"id": 4, "name": "God", "avatar": "👁️", "unlock_level": 15},
        {"id": 5, "name": "Universe", "avatar": "🌌", "unlock_level": 20}
    ]
}

def get_bot_skins(bot_id: str):
    """Get all skins for a bot"""
    return BOT_SKINS.get(bot_id, BOT_SKINS["mende"])

def get_unlocked_skins(bot_id: str, level: int):
    """Get all unlocked skins for a bot at given level"""
    all_skins = get_bot_skins(bot_id)
    return [skin for skin in all_skins if skin['unlock_level'] <= level]

def get_current_skin(bot_id: str, level: int, skin_id: int = None):
    """Get current skin or best unlocked skin"""
    unlocked = get_unlocked_skins(bot_id, level)
    if not unlocked:
        return get_bot_skins(bot_id)[0]  # Return standard skin
    
    if skin_id:
        for skin in unlocked:
            if skin['id'] == skin_id:
                return skin
    
    # Return highest unlocked skin
    return max(unlocked, key=lambda s: s['unlock_level'])
