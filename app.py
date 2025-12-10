"""
Agent Battle Simulator - Flask WebApp
Main application file
"""

import json
import os
import secrets
import sqlite3
import time
from typing import Optional

from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS

from game import (
    Agent,
    Battle,
    get_all_actions,
    get_all_battle_bots,
    get_battle_bot,
    get_bot_skins,
    get_unlocked_skins,
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

DB_PATH = os.environ.get('BATTLE_DB_PATH', 'battles.db')
BATTLE_TTL_SECONDS = int(os.environ.get('BATTLE_TTL_SECONDS', 3600))


def get_db_connection():
    """Create a SQLite connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables if needed"""
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS battles (
                battle_id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_stats (
                agent_name TEXT PRIMARY KEY,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
            """
        )


def cleanup_expired_battles():
    """Remove battles older than the TTL"""
    expiration_threshold = time.time() - BATTLE_TTL_SECONDS
    with get_db_connection() as conn:
        conn.execute("DELETE FROM battles WHERE updated_at < ?", (expiration_threshold,))


def battle_to_dict(battle: Battle) -> dict:
    """Serialize a Battle instance into a JSON-friendly dict"""
    return {
        'current_round': battle.current_round,
        'agent1': battle.agent1.to_dict(),
        'agent2': battle.agent2.to_dict(),
        'battle_log': battle.battle_log,
        'winner': battle.winner.to_dict() if battle.winner else None,
    }


def battle_from_dict(data: dict) -> Battle:
    """Rehydrate a Battle instance from stored state"""
    agent1 = Agent.from_dict(data['agent1'])
    agent2 = Agent.from_dict(data['agent2'])

    battle = Battle(agent1, agent2, reset_agents=False)
    battle.current_round = data.get('current_round', 0)
    battle.battle_log = data.get('battle_log', [])

    winner_data = data.get('winner')
    battle.winner = Agent.from_dict(winner_data) if winner_data else None

    return battle


def save_battle(battle_id: str, battle: Battle):
    """Persist battle state and refresh TTL"""
    cleanup_expired_battles()
    payload = json.dumps(battle_to_dict(battle))
    with get_db_connection() as conn:
        conn.execute(
            "REPLACE INTO battles (battle_id, data, updated_at) VALUES (?, ?, ?)",
            (battle_id, payload, time.time()),
        )


def load_battle(battle_id: str) -> Optional[Battle]:
    """Load battle from storage"""
    cleanup_expired_battles()
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT data FROM battles WHERE battle_id = ?", (battle_id,)
        ).fetchone()

    if not row:
        return None

    return battle_from_dict(json.loads(row['data']))


def remove_battle(battle_id: str):
    """Delete battle from storage"""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM battles WHERE battle_id = ?", (battle_id,))


def record_agent_result(agent_name: str, won: bool):
    """Update aggregated agent win/loss counts"""
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO agent_stats (agent_name, wins, losses)
            VALUES (?, ?, ?)
            ON CONFLICT(agent_name) DO UPDATE SET
                wins = wins + excluded.wins,
                losses = losses + excluded.losses
            """,
            (agent_name, 1 if won else 0, 0 if won else 1),
        )


init_db()


@app.before_request
def prune_expired_battles():
    """Ensure expired battles are removed before every request."""
    cleanup_expired_battles()


def get_battle_or_error(battle_id: Optional[str]):
    """Load a battle or return a tuple with an error response and status."""
    if not battle_id:
        return None, jsonify({'error': 'Battle not found'}), 404

    battle = load_battle(battle_id)
    if not battle:
        return None, jsonify({'error': 'Battle not found'}), 404

    return battle, None, None

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
    save_battle(battle_id, battle)

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

    battle, error_response, status = get_battle_or_error(battle_id)
    if error_response:
        return error_response, status
    
    action1_id = data.get('action1_id', 1)
    action2_id = data.get('action2_id', 1)
    
    # Execute turn
    result = battle.execute_turn(action1_id, action2_id)

    # Persist updated battle
    save_battle(battle_id, battle)

    # Clean up if battle is over
    if result['battle_over']:
        # Persist aggregated stats
        if battle.winner:
            record_agent_result(battle.agent1.name, battle.winner is battle.agent1)
            record_agent_result(battle.agent2.name, battle.winner is battle.agent2)

        # Keep battle for summary but mark timestamp via save_battle already
        pass

    return jsonify(result)

@app.route('/api/battle/summary/<battle_id>', methods=['GET'])
def get_battle_summary(battle_id):
    """Get battle summary"""
    battle, error_response, status = get_battle_or_error(battle_id)
    if error_response:
        return error_response, status
    return jsonify(battle.get_battle_summary())

@app.route('/api/battle/ai-action', methods=['POST'])
def get_ai_action():
    """Get AI-recommended action"""
    data = request.json
    battle_id = data.get('battle_id') or session.get('battle_id')

    battle, error_response, status = get_battle_or_error(battle_id)
    if error_response:
        return error_response, status
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
