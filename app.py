"""
Agent Battle Simulator - Flask WebApp
Main application file
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import secrets
import os
from battle_storage import BattleStorage
from game import Agent, get_all_actions, Battle, get_all_battle_bots, get_battle_bot, get_bot_skins, get_unlocked_skins

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Battle storage with TTL + cleanup
battle_storage = BattleStorage()


@app.before_request
def prune_battles():
    """Periodically prune expired battles when using in-memory store."""
    battle_storage.prune_expired()

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
    battle_storage.save_battle(battle_id, battle)
    
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

    battle, error_reason = battle_storage.get_battle(battle_id) if battle_id else (None, 'not_found')
    if error_reason:
        status_code = 410 if error_reason == 'expired' else 404
        return jsonify({'error': 'Battle abgelaufen oder nicht gefunden', 'code': f'battle_{error_reason}'}), status_code

    action1_id = data.get('action1_id') or data.get('action_id', 1)
    action2_id = data.get('action2_id', 1)
    
    # Execute turn
    result = battle.execute_turn(action1_id, action2_id)

    # Persist updated state and refresh TTL
    battle_storage.save_battle(battle_id, battle)

    commentary = '; '.join([action.get('comment', action.get('action', '')) for action in result.get('actions', [])])
    response_payload = {
        'round': result.get('round'),
        'actions': result.get('actions'),
        'agent1': result.get('agent1_state'),
        'agent2': result.get('agent2_state'),
        'battle_over': result.get('battle_over'),
        'winner': result.get('winner'),
        'commentary': commentary
    }

    return jsonify(response_payload)

@app.route('/api/battle/summary/<battle_id>', methods=['GET'])
def get_battle_summary(battle_id):
    """Get battle summary"""
    battle, error_reason = battle_storage.get_battle(battle_id)
    if error_reason:
        status_code = 410 if error_reason == 'expired' else 404
        return jsonify({'error': 'Battle abgelaufen oder nicht gefunden', 'code': f'battle_{error_reason}'}), status_code

    return jsonify(battle.get_battle_summary())

@app.route('/api/battle/ai-action', methods=['POST'])
def get_ai_action():
    """Get AI-recommended action"""
    data = request.json
    battle_id = data.get('battle_id') or session.get('battle_id')

    battle, error_reason = battle_storage.get_battle(battle_id) if battle_id else (None, 'not_found')
    if error_reason:
        status_code = 410 if error_reason == 'expired' else 404
        return jsonify({'error': 'Battle abgelaufen oder nicht gefunden', 'code': f'battle_{error_reason}'}), status_code

    battle_storage.save_battle(battle_id, battle)
    agent = battle.agent2  # AI is always agent2
    
    # Simple AI logic
    actions = get_all_actions()
    
    # Filter actions by stamina
    available_actions = [a for a in actions if a['stamina_cost'] <= agent.stamina]
    
    if not available_actions:
        # If no stamina, pick cheapest action
        available_actions = sorted(actions, key=lambda x: x['stamina_cost'])[:1]
    
    # AI strategy: prefer high damage when HP is high, defensive when low
    if agent.hp < agent.max_hp * 0.3:
        # Low HP: prefer healing/defensive
        defensive = [a for a in available_actions if 'heal' in a['effects'] or 'buff_defense' in a['effects']]
        if defensive:
            action = defensive[0]
        else:
            action = available_actions[0]
    else:
        # High HP: prefer offensive
        offensive = [a for a in available_actions if 'burn' in a['effects'] or 'debuff_attack' in a['effects']]
        if offensive:
            action = offensive[0]
        else:
            # Pick highest damage
            action = max(available_actions, key=lambda x: x['damage_range'][1])
    
    return jsonify({'action_id': action['id']})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
