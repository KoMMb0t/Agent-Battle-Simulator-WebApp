import random
import unittest

from app import select_ai_action
from game import Agent, get_all_actions, get_battle_bot


def _make_agent(bot_id: str, name: str = None) -> Agent:
    bot_data = get_battle_bot(bot_id)
    return Agent(name or bot_data['name'], agent_type=bot_id, level=1, agent_type_data=bot_data)


class TestAiDecisionLogic(unittest.TestCase):
    def test_prefers_debuff_when_opponent_is_burning(self):
        rng = random.Random(123)
        ai_agent = _make_agent('regulus')
        opponent = _make_agent('mende')
        opponent.add_debuff({'name': 'Brennend', 'attack': -3, 'duration': 2})

        chosen_action = select_ai_action(ai_agent, opponent, rng=rng)

        self.assertTrue(
            any(effect in {'burn', 'slow', 'sticky', 'debuff_attack', 'debuff_defense'}
                for effect in chosen_action['effects'])
        )

    def test_prefers_lower_cost_when_sticky(self):
        rng = random.Random(42)
        ai_agent = _make_agent('spark')
        opponent = _make_agent('eco')
        ai_agent.add_debuff({'name': 'Klebrig', 'attack': -2, 'duration': 1})

        chosen_action = select_ai_action(ai_agent, opponent, rng=rng)

        stamina_costs = [action['stamina_cost'] for action in get_all_actions()
                         if action['stamina_cost'] <= ai_agent.stamina]
        self.assertEqual(chosen_action['stamina_cost'], min(stamina_costs))

    def test_profiles_change_weighted_outcome(self):
        rng = random.Random(7)
        defensive_agent = _make_agent('sentinel')
        defensive_agent.hp = defensive_agent.max_hp * 0.2
        opponent = _make_agent('eco')

        # Limit actions to a clear offensive vs defensive choice
        actions = [
            next(a for a in get_all_actions() if 'burn' in a['effects']),
            next(a for a in get_all_actions() if 'heal' in a['effects'])
        ]

        defensive_choice = select_ai_action(defensive_agent, opponent, rng=rng, actions=actions)

        # Reset RNG to replicate randomness for different profile
        rng = random.Random(7)
        aggressive_agent = _make_agent('spark')
        aggressive_agent.hp = aggressive_agent.max_hp * 0.8

        aggressive_choice = select_ai_action(aggressive_agent, opponent, rng=rng, actions=actions)

        self.assertNotEqual(defensive_choice['id'], aggressive_choice['id'])


if __name__ == '__main__':
    unittest.main()
