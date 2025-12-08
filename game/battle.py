"""
Agent Battle Simulator - Battle Engine
Handles battle logic and state
"""

import random
from typing import Dict, List, Optional
from .agents import Agent
from .actions import get_action, calculate_damage, apply_effects, get_random_comment

class Battle:
    def __init__(self, agent1: Agent, agent2: Agent):
        self.agent1 = agent1
        self.agent2 = agent2
        self.current_round = 0
        self.battle_log: List[Dict] = []
        self.winner: Optional[Agent] = None
        
        # Reset agents for battle
        self.agent1.reset_for_battle()
        self.agent2.reset_for_battle()
    
    def execute_turn(self, action1_id: int, action2_id: int) -> Dict:
        """Execute one turn of battle"""
        self.current_round += 1
        
        turn_result = {
            'round': self.current_round,
            'actions': [],
            'agent1_state': None,
            'agent2_state': None,
            'battle_over': False,
            'winner': None
        }
        
        # Get actions
        action1 = get_action(action1_id)
        action2 = get_action(action2_id)
        
        # Check stamina
        can_use_1 = self.agent1.use_stamina(action1['stamina_cost'])
        can_use_2 = self.agent2.use_stamina(action2['stamina_cost'])
        
        # Execute actions (random order for fairness)
        agents = [(self.agent1, self.agent2, action1, can_use_1),
                  (self.agent2, self.agent1, action2, can_use_2)]
        random.shuffle(agents)
        
        for attacker, defender, action, can_use in agents:
            if not can_use:
                turn_result['actions'].append({
                    'attacker': attacker.name,
                    'action': 'Keine Stamina!',
                    'damage': 0,
                    'effects': [],
                    'comment': f"{attacker.name} hat keine Stamina mehr!"
                })
                continue
            
            # Calculate damage
            damage = calculate_damage(action, attacker, defender)
            actual_damage = defender.take_damage(damage)
            
            # Apply effects
            effect_messages = apply_effects(action, attacker, defender)
            
            # Get comment
            comment = get_random_comment(action)
            
            turn_result['actions'].append({
                'attacker': attacker.name,
                'action': action['name'],
                'description': action['description'],
                'damage': actual_damage,
                'effects': effect_messages,
                'comment': comment
            })
            
            # Check if battle is over
            if not defender.is_alive():
                turn_result['battle_over'] = True
                turn_result['winner'] = attacker.name
                self.winner = attacker
                
                # Award XP
                attacker.add_xp(defender.level * 50)
                defender.add_xp(defender.level * 25)  # Consolation prize
                
                # Update wins/losses
                attacker.wins += 1
                defender.losses += 1
                
                break
        
        # Update states
        turn_result['agent1_state'] = self.agent1.to_dict()
        turn_result['agent2_state'] = self.agent2.to_dict()
        
        # Add to battle log
        self.battle_log.append(turn_result)
        
        return turn_result
    
    def get_battle_summary(self) -> Dict:
        """Get summary of the battle"""
        return {
            'rounds': self.current_round,
            'winner': self.winner.name if self.winner else None,
            'agent1': self.agent1.to_dict(),
            'agent2': self.agent2.to_dict(),
            'battle_log': self.battle_log
        }
