"""
Agent Battle Simulator - Agent Classes
Adapted for WebApp
"""

import random
from typing import Dict, List, Optional

from .battle_bots import get_battle_bot

class Agent:
    def __init__(self, name: str, agent_type: str = "ninja", level: int = 1, agent_type_data: Dict = None):
        self.name = name
        self.agent_type = agent_type  # Agent type ID
        self.level = level
        self.agent_type_data = agent_type_data or {}
        
        # Get bonuses from agent type
        stats_bonus = self.agent_type_data.get('stats', {})
        hp_bonus = stats_bonus.get('hp_bonus', 0)
        stamina_bonus = stats_bonus.get('stamina_bonus', 0)
        attack_bonus = stats_bonus.get('attack_bonus', 0)
        defense_bonus = stats_bonus.get('defense_bonus', 0)
        
        # Base stats with agent type bonuses
        self.max_hp = 100 + (level - 1) * 20 + hp_bonus
        self.hp = self.max_hp
        self.max_stamina = 100 + (level - 1) * 10 + stamina_bonus
        self.stamina = self.max_stamina
        self.attack = 10 + (level - 1) * 2 + attack_bonus
        self.defense = 10 + (level - 1) * 2 + defense_bonus
        
        # XP System
        self.xp = 0
        self.xp_to_next_level = self.calculate_xp_needed(level)
        
        # Battle stats
        self.buffs: List[Dict] = []
        self.debuffs: List[Dict] = []
        self.wins = 0
        self.losses = 0
        
    def calculate_xp_needed(self, level: int) -> int:
        """Calculate XP needed for next level"""
        return int(100 * (1.5 ** (level - 1)))
    
    def add_xp(self, amount: int) -> bool:
        """Add XP and check for level up"""
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            return self.level_up()
        return False
    
    def level_up(self) -> bool:
        """Level up the agent"""
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = self.calculate_xp_needed(self.level)
        
        # Increase stats
        self.max_hp += 20
        self.hp = self.max_hp
        self.max_stamina += 10
        self.stamina = self.max_stamina
        self.attack += 2
        self.defense += 2
        
        return True
    
    def add_buff(self, buff: Dict):
        """Add a buff to the agent"""
        self.buffs.append(buff)
    
    def add_debuff(self, debuff: Dict):
        """Add a debuff to the agent"""
        self.debuffs.append(debuff)
    
    def get_effective_attack(self) -> int:
        """Calculate attack with buffs/debuffs"""
        attack = self.attack
        for buff in self.buffs:
            if 'attack' in buff:
                attack += buff['attack']
        for debuff in self.debuffs:
            if 'attack' in debuff:
                attack += debuff['attack']  # debuffs are negative
        return max(1, attack)
    
    def get_effective_defense(self) -> int:
        """Calculate defense with buffs/debuffs"""
        defense = self.defense
        for buff in self.buffs:
            if 'defense' in buff:
                defense += buff['defense']
        for debuff in self.debuffs:
            if 'defense' in debuff:
                defense += debuff['defense']  # debuffs are negative
        return max(1, defense)
    
    def take_damage(self, damage: int) -> int:
        """Take damage and return actual damage taken"""
        actual_damage = max(1, damage - self.get_effective_defense() // 2)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int):
        """Heal the agent"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def use_stamina(self, amount: int) -> bool:
        """Use stamina, return False if not enough"""
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False
    
    def restore_stamina(self, amount: int):
        """Restore stamina"""
        self.stamina = min(self.max_stamina, self.stamina + amount)
    
    def is_alive(self) -> bool:
        """Check if agent is still alive"""
        return self.hp > 0
    
    def reset_for_battle(self):
        """Reset HP/Stamina for new battle"""
        self.hp = self.max_hp
        self.stamina = self.max_stamina
        self.buffs = []
        self.debuffs = []
    
    def to_dict(self) -> Dict:
        """Convert agent to dictionary for JSON"""
        return {
            'name': self.name,
            'type': self.agent_type,
            'type_name': self.agent_type_data.get('name', 'Unknown'),
            'avatar': self.agent_type_data.get('avatar', '🤖'),
            'color': self.agent_type_data.get('color', '#00ff00'),
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'stamina': self.stamina,
            'max_stamina': self.max_stamina,
            'attack': self.attack,
            'defense': self.defense,
            'xp': self.xp,
            'xp_to_next_level': self.xp_to_next_level,
            'xp_percentage': int((self.xp / self.xp_to_next_level) * 100) if self.xp_to_next_level > 0 else 0,
            'buffs': self.buffs,
            'debuffs': self.debuffs,
            'wins': self.wins,
            'losses': self.losses
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Agent":
        """Create an agent instance from stored state"""
        agent_type = data.get('type', 'ninja')
        agent_type_data = get_battle_bot(agent_type) or {}

        agent = cls(
            data.get('name', 'Agent'),
            agent_type=agent_type,
            level=data.get('level', 1),
            agent_type_data=agent_type_data,
        )

        # Restore stats and progress
        for attr in [
            'max_hp', 'hp', 'max_stamina', 'stamina',
            'attack', 'defense', 'xp', 'xp_to_next_level',
            'wins', 'losses'
        ]:
            if attr in data:
                setattr(agent, attr, data[attr])

        agent.buffs = data.get('buffs', [])
        agent.debuffs = data.get('debuffs', [])

        return agent
