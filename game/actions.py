"""
Agent Battle Simulator - Action System
Absurde Kampfaktionen mit Effekten
"""

import random
from typing import Dict, List

ACTIONS = [
    {
        "id": 1,
        "name": "🔥 Feuerball der Bürofrustration",
        "description": "Wirft einen brennenden Feuerball aus aufgestauter Wut!",
        "stamina_cost": 15,
        "damage_range": (20, 35),
        "effects": ["burn"],
        "comments": [
            "Der Schaden ist real! Genau wie die Bugs in Production!",
            "Autsch! Das hat wehgetan... emotional!",
            "Und da trifft der Angriff mitten ins Ego!"
        ]
    },
    {
        "id": 2,
        "name": "🧻 Toilettenpapier-Tsunami",
        "description": "Überflutet den Gegner mit endlosen Rollen!",
        "stamina_cost": 20,
        "damage_range": (25, 40),
        "effects": ["slow"],
        "comments": [
            "Das Publikum (also niemand) ist begeistert!",
            "Ein taktisches Manöver! Oder doch nur Glück?",
            "Beide Kämpfer sind erschöpft... Zeit für eine Kaffeepause?"
        ]
    },
    {
        "id": 3,
        "name": "🥤 Smoothie-Attacke",
        "description": "Wirft einen überteuerten Smoothie!",
        "stamina_cost": 10,
        "damage_range": (10, 20),
        "effects": ["sticky"],
        "comments": [
            "Beide geben alles! Wie bei einem Merge-Conflict!",
            "Das war... unerwartet effektiv!",
            "Critical Hit! Oder war's ein Bug?"
        ]
    },
    {
        "id": 4,
        "name": "📧 Meeting-Demoralisierung",
        "description": "Lädt zu einem unnötigen Meeting ein!",
        "stamina_cost": 18,
        "damage_range": (15, 30),
        "effects": ["debuff_attack"],
        "comments": [
            "Der Gegner verliert den Willen zu leben!",
            "Effektiver als gedacht!",
            "Das tut weh... psychologisch!"
        ]
    },
    {
        "id": 5,
        "name": "🧲 Magnetische Feldverwirrung",
        "description": "Verwirrt den Angreifer mit magnetischen Feldern!",
        "stamina_cost": 12,
        "damage_range": (15, 25),
        "effects": ["debuff_defense"],
        "comments": [
            "Verwirrung ist die beste Verteidigung!",
            "Der Gegner weiß nicht mehr wo oben ist!",
            "Chaos regiert!"
        ]
    },
    {
        "id": 6,
        "name": "🧠 Gedankenlesen",
        "description": "Liest die Gedanken des Gegners und kontert perfekt!",
        "stamina_cost": 18,
        "damage_range": (20, 35),
        "effects": ["buff_defense"],
        "comments": [
            "Vorausschauend wie ein guter Debugger!",
            "Der perfekte Konter!",
            "Mind = Blown!"
        ]
    },
    {
        "id": 7,
        "name": "⚔️ Zynischer Gegenangriff",
        "description": "Kontert mit sarkastischen Bemerkungen!",
        "stamina_cost": 15,
        "damage_range": (18, 30),
        "effects": ["debuff_defense"],
        "comments": [
            "Sarkasmus als Waffe!",
            "Das trifft härter als erwartet!",
            "Emotionaler Schaden: Maximum!"
        ]
    },
    {
        "id": 8,
        "name": "☕ Kaffee-Konter",
        "description": "Ein heißer Espresso bringt neue Energie!",
        "stamina_cost": 12,
        "damage_range": (8, 15),
        "effects": ["heal"],
        "comments": [
            "Koffein ist die beste Medizin!",
            "Energie zurück!",
            "Zweite Luft!"
        ]
    }
]

def get_action(action_id: int) -> Dict:
    """Get action by ID"""
    for action in ACTIONS:
        if action['id'] == action_id:
            return action.copy()
    return ACTIONS[0].copy()

def calculate_damage(action: Dict, attacker, defender) -> int:
    """Calculate damage for an action"""
    base_damage = random.randint(*action['damage_range'])
    attack_bonus = attacker.get_effective_attack() // 5
    defense_reduction = defender.get_effective_defense() // 10
    
    total_damage = max(1, base_damage + attack_bonus - defense_reduction)
    return total_damage

def apply_effects(action: Dict, attacker, defender) -> List[str]:
    """Apply action effects and return messages"""
    messages = []
    
    for effect in action['effects']:
        if effect == 'burn':
            debuff = {'name': 'Brennend', 'attack': -3, 'duration': 2}
            defender.add_debuff(debuff)
            messages.append(f"💀 {defender.name} erhält Debuff: Brennend!")
            
        elif effect == 'slow':
            debuff = {'name': 'Verlangsamt', 'defense': -4, 'duration': 2}
            defender.add_debuff(debuff)
            messages.append(f"💀 {defender.name} erhält Debuff: Verlangsamt!")
            
        elif effect == 'sticky':
            debuff = {'name': 'Klebrig', 'attack': -2, 'duration': 1}
            defender.add_debuff(debuff)
            messages.append(f"💀 {defender.name} ist klebrig!")
            
        elif effect == 'debuff_attack':
            debuff = {'name': 'Demoralisiert', 'attack': -5, 'duration': 3}
            defender.add_debuff(debuff)
            messages.append(f"💀 {defender.name} ist demoralisiert!")
            
        elif effect == 'debuff_defense':
            debuff = {'name': 'Geschwächt', 'defense': -6, 'duration': 2}
            defender.add_debuff(debuff)
            messages.append(f"💀 {defender.name} erhält Debuff: -6 Defense!")
            
        elif effect == 'buff_defense':
            buff = {'name': 'Fokussiert', 'defense': 5, 'duration': 2}
            attacker.add_buff(buff)
            messages.append(f"✨ {attacker.name} erhält Buff: +5 Defense!")
            
        elif effect == 'heal':
            heal_amount = 15
            attacker.heal(heal_amount)
            messages.append(f"💚 {attacker.name} heilt {heal_amount} HP!")
    
    return messages

def get_random_comment(action: Dict) -> str:
    """Get random battle comment"""
    return random.choice(action['comments'])

def get_all_actions() -> List[Dict]:
    """Get all available actions"""
    return [action.copy() for action in ACTIONS]
