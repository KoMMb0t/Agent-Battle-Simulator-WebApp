"""
Agent Battle Simulator - Flask WebApp
Main application file
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import secrets
import os
import random
from typing import Dict, List, Optional
from battle_storage import BattleStorage
from game import Agent, get_all_actions, Battle, get_all_battle_bots, get_battle_bot, get_bot_skins, get_unlocked_skins

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Battle storage with TTL + cleanup
battle_storage = BattleStorage()


def _get_ai_profile(agent: Agent) -> str:
    """Return deterministic AI profile (aggressive/defensive) based on bot ID."""
    profile_hash = sum(ord(char) for char in agent.agent_type)
    return 'aggressive' if profile_hash % 2 else 'defensive'


def _get_action_category(action: Dict) -> str:
    """Classify an action into offensive/debuff/defensive categories."""
    debuff_effects = {'burn', 'slow', 'sticky', 'debuff_attack', 'debuff_defense'}
    defensive_effects = {'heal', 'buff_defense'}

    action_effects = set(action.get('effects', []))
    if action_effects & defensive_effects:
        return 'defensive'
    if action_effects & debuff_effects:
        return 'debuff'
    return 'offensive'


def _has_named_effect(effects: List[Dict], name: str) -> bool:
    """Check if a list of buffs/debuffs contains an entry by name."""
    return any(effect.get('name') == name for effect in effects)


def select_ai_action(agent: Agent, opponent: Agent, rng: Optional[random.Random] = None,
                     actions: Optional[List[Dict]] = None) -> Dict:
    """Choose an AI action with weighted randomness and awareness of current effects."""

    rng = rng or random
    actions = actions or get_all_actions()

    # Filter actions by stamina
    available_actions = [a for a in actions if a['stamina_cost'] <= agent.stamina]

    if not available_actions:
        return sorted(actions, key=lambda x: x['stamina_cost'])[0]

    profile = _get_ai_profile(agent)
    base_profile_weights = {
        'aggressive': {'offensive': 1.2, 'debuff': 1.0, 'defensive': 0.85},
        'defensive': {'offensive': 0.9, 'debuff': 1.0, 'defensive': 1.25},
    }

    profile_weights = base_profile_weights.get(profile, base_profile_weights['aggressive'])
    type_randomness = {category: profile_weights[category] * rng.uniform(0.85, 1.15)
                       for category in ['offensive', 'debuff', 'defensive']}

    opponent_burning = _has_named_effect(opponent.debuffs, 'Brennend')
    agent_sticky = _has_named_effect(agent.debuffs, 'Klebrig')
    low_hp = agent.hp < agent.max_hp * 0.4

    defensive_options = [a for a in available_actions if _get_action_category(a) == 'defensive']
    if profile == 'defensive' and low_hp and defensive_options:
        available_actions = defensive_options

    if agent_sticky:
        min_cost = min(action['stamina_cost'] for action in available_actions)
        cheap_cap = min_cost + 5
        available_actions = [a for a in available_actions if a['stamina_cost'] <= cheap_cap]

    action_weights = []
    for action in available_actions:
        category = _get_action_category(action)
        weight = type_randomness[category]

        if profile == 'aggressive' and category == 'offensive':
            weight *= 1.1

        if profile == 'defensive' and category == 'defensive':
            weight *= 1.2

        if low_hp and category == 'defensive':
            weight *= 1.35

        if opponent_burning and category == 'debuff':
            weight *= 1.25

        if agent_sticky:
            weight *= 1 / (1 + (action['stamina_cost'] / 12))

        weight *= 1 + (action['damage_range'][1] / 60)
        weight *= 1 + max(0, (40 - action['stamina_cost'])) / 220

        action_weights.append(weight)

    return rng.choices(available_actions, weights=action_weights, k=1)[0]

@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')

@app.route('/api/actions', methods=['GET'])
def get_actions():
    """Get all available actions"""
    return jsonify(get_all_actions())

@app.route('/api/bots', methods=['GET'])
def get_bots():
    """Get all available battle bots"""
    return jsonify(get_all_battle_bots())

@app.route('/api/bots/<bot_id>/skins', methods=['GET'])
def get_skins(bot_id):
    """Get all skins for a bot"""
    return jsonify(get_bot_skins(bot_id))

@app.route('/api/bots/<bot_id>/unlocked-skins/<int:level>', methods=['GET'])
def get_unlocked(bot_id, level):
    """Get unlocked skins for a bot at given level"""
    return jsonify(get_unlocked_skins(bot_id, level))

@app.route('/api/battle/start', methods=['POST'])
def start_battle():
    """Start a new battle"""
    data = request.json
    
    # Create agents
    agent1_name = data.get('agent1_name', 'Agent Alpha')
    agent2_name = data.get('agent2_name', 'Agent Beta')
    agent1_bot = data.get('agent1_bot', 'mende')
    agent2_bot = data.get('agent2_bot', 'regulus')
    
    # Get bot data
    agent1_bot_data = get_battle_bot(agent1_bot)
    agent2_bot_data = get_battle_bot(agent2_bot)
    
    agent1 = Agent(agent1_name, agent_type=agent1_bot, level=1, agent_type_data=agent1_bot_data)
    agent2 = Agent(agent2_name, agent_type=agent2_bot, level=1, agent_type_data=agent2_bot_data)
    
    # Create battle
    battle = Battle(agent1, agent2)
    
    # Generate battle ID
    battle_id = secrets.token_urlsafe(16)
    battle_storage.set(battle_id, battle)
    
    # Store in session
    session['battle_id'] = battle_id
    
    return jsonify({
        'battle_id': battle_id,
        'agent1': agent1.to_dict(),
        'agent2': agent2.to_dict()
    })

@app.route('/api/battle/turn', methods=['POST'])
def execute_turn():
    """Execute one turn of battle"""
    data = request.json
    battle_id = data.get('battle_id') or session.get('battle_id')
    
    if not battle_id or not battle_storage.has(battle_id):
        return jsonify({'error': 'Battle not found'}), 404

    battle = battle_storage.get(battle_id)
    
    action1_id = data.get('action1_id', 1)
    action2_id = data.get('action2_id', 1)
    
    # Execute turn
    result = battle.execute_turn(action1_id, action2_id)
    
    # Clean up if battle is over
    if result['battle_over']:
        # Keep battle for a while for summary
        pass
    
    return jsonify(result)

@app.route('/api/battle/summary/<battle_id>', methods=['GET'])
def get_battle_summary(battle_id):
    """Get battle summary"""
    if not battle_storage.has(battle_id):
        return jsonify({'error': 'Battle not found'}), 404

    battle = battle_storage.get(battle_id)
    return jsonify(battle.get_battle_summary())

@app.route('/api/battle/ai-action', methods=['POST'])
def get_ai_action():
    """Get AI-recommended action"""
    data = request.json
    battle_id = data.get('battle_id') or session.get('battle_id')
    
    if not battle_id or not battle_storage.has(battle_id):
        return jsonify({'error': 'Battle not found'}), 404

    battle = battle_storage.get(battle_id)
    agent = battle.agent2  # AI is always agent2
    opponent = battle.agent1

    action = select_ai_action(agent, opponent)

    return jsonify({'action_id': action['id']})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
