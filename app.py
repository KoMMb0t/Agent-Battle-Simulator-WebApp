"""
Agent Battle Simulator - Flask WebApp
Main application file
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import secrets
import os
from game import Agent, get_all_actions, Battle

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Store active battles in memory (in production, use Redis or database)
battles = {}

@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')

@app.route('/api/actions', methods=['GET'])
def get_actions():
    """Get all available actions"""
    return jsonify(get_all_actions())

@app.route('/api/battle/start', methods=['POST'])
def start_battle():
    """Start a new battle"""
    data = request.json
    
    # Create agents
    agent1_name = data.get('agent1_name', 'Agent Alpha')
    agent2_name = data.get('agent2_name', 'Agent Beta')
    
    agent1 = Agent(agent1_name, agent_type='attacker', level=1)
    agent2 = Agent(agent2_name, agent_type='defender', level=1)
    
    # Create battle
    battle = Battle(agent1, agent2)
    
    # Generate battle ID
    battle_id = secrets.token_urlsafe(16)
    battles[battle_id] = battle
    
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
    
    if not battle_id or battle_id not in battles:
        return jsonify({'error': 'Battle not found'}), 404
    
    battle = battles[battle_id]
    
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
    if battle_id not in battles:
        return jsonify({'error': 'Battle not found'}), 404
    
    battle = battles[battle_id]
    return jsonify(battle.get_battle_summary())

@app.route('/api/battle/ai-action', methods=['POST'])
def get_ai_action():
    """Get AI-recommended action"""
    data = request.json
    battle_id = data.get('battle_id') or session.get('battle_id')
    
    if not battle_id or battle_id not in battles:
        return jsonify({'error': 'Battle not found'}), 404
    
    battle = battles[battle_id]
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
