// Agent Battle Simulator - Game Logic
// Frontend JavaScript

class GameController {
    constructor() {
        this.battleId = null;
        this.agent1 = null;
        this.agent2 = null;
        this.actions = [];
        this.currentRound = 0;
        this.isProcessing = false;
        
        this.init();
    }
    
    init() {
        // Load actions
        this.loadActions();
        
        // Event listeners
        document.getElementById('start-battle-btn').addEventListener('click', () => this.startBattle());
        document.getElementById('new-battle-btn').addEventListener('click', () => this.resetGame());
    }
    
    async loadActions() {
        try {
            const response = await fetch('/api/actions');
            this.actions = await response.json();
            console.log('Actions loaded:', this.actions);
        } catch (error) {
            console.error('Error loading actions:', error);
        }
    }
    
    async startBattle() {
        const agent1Name = document.getElementById('agent1-name').value.trim() || 'Agent Alpha';
        const agent2Name = document.getElementById('agent2-name').value.trim() || 'Agent Beta';
        
        try {
            const response = await fetch('/api/battle/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent1_name: agent1Name,
                    agent2_name: agent2Name
                })
            });
            
            const data = await response.json();
            this.battleId = data.battle_id;
            this.agent1 = data.agent1;
            this.agent2 = data.agent2;
            this.currentRound = 0;
            
            // Update UI
            this.showScreen('battle-screen');
            this.updateAgentDisplay();
            this.renderActions();
            this.clearBattleLog();
            
        } catch (error) {
            console.error('Error starting battle:', error);
            alert('Fehler beim Starten des Kampfes!');
        }
    }
    
    renderActions() {
        const grid = document.getElementById('actions-grid');
        grid.innerHTML = '';
        
        this.actions.forEach(action => {
            const btn = document.createElement('button');
            btn.className = 'action-btn';
            btn.dataset.actionId = action.id;
            
            // Check if enough stamina
            if (this.agent1.stamina < action.stamina_cost) {
                btn.classList.add('disabled');
            }
            
            btn.innerHTML = `
                <div class="action-name">${action.name}</div>
                <div class="action-desc">${action.description}</div>
                <div class="action-cost">⚡ Stamina: ${action.stamina_cost}</div>
                <div class="action-damage">💥 Schaden: ${action.damage_range[0]}-${action.damage_range[1]}</div>
            `;
            
            btn.addEventListener('click', () => this.selectAction(action.id));
            grid.appendChild(btn);
        });
    }
    
    async selectAction(actionId) {
        if (this.isProcessing) return;
        
        // Check if action is available
        const action = this.actions.find(a => a.id === actionId);
        if (this.agent1.stamina < action.stamina_cost) {
            this.addLogEntry('system', '⚠️ Nicht genug Stamina!', 'log-warning');
            return;
        }
        
        this.isProcessing = true;
        
        try {
            // Get AI action
            const aiResponse = await fetch('/api/battle/ai-action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ battle_id: this.battleId })
            });
            const aiData = await aiResponse.json();
            
            // Execute turn
            const response = await fetch('/api/battle/turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    battle_id: this.battleId,
                    action1_id: actionId,
                    action2_id: aiData.action_id
                })
            });
            
            const result = await response.json();
            this.processTurnResult(result);
            
        } catch (error) {
            console.error('Error executing turn:', error);
            alert('Fehler beim Ausführen der Aktion!');
        } finally {
            this.isProcessing = false;
        }
    }
    
    processTurnResult(result) {
        this.currentRound = result.round;
        this.agent1 = result.agent1_state;
        this.agent2 = result.agent2_state;
        
        // Update round number
        document.getElementById('round-number').textContent = this.currentRound;
        
        // Process actions
        result.actions.forEach((actionResult, index) => {
            setTimeout(() => {
                this.displayAction(actionResult);
            }, index * 1000);
        });
        
        // Update display after animations
        setTimeout(() => {
            this.updateAgentDisplay();
            this.renderActions();
            
            // Check if battle is over
            if (result.battle_over) {
                setTimeout(() => {
                    this.showVictory(result.winner);
                }, 1500);
            }
        }, result.actions.length * 1000 + 500);
    }
    
    displayAction(actionResult) {
        const agentClass = actionResult.attacker === this.agent1.name ? 'agent1' : 'agent2';
        
        let html = `
            <div class="log-action">${actionResult.attacker}: ${actionResult.action}</div>
            <div class="log-damage">💥 Schaden: ${actionResult.damage}</div>
        `;
        
        if (actionResult.effects && actionResult.effects.length > 0) {
            actionResult.effects.forEach(effect => {
                html += `<div class="log-effect">${effect}</div>`;
            });
        }
        
        html += `<div class="log-comment">${actionResult.comment}</div>`;
        
        this.addLogEntry(agentClass, html);
    }
    
    addLogEntry(agentClass, content, extraClass = '') {
        const log = document.getElementById('battle-log');
        const entry = document.createElement('div');
        entry.className = `log-entry ${agentClass} ${extraClass}`;
        entry.innerHTML = content;
        log.appendChild(entry);
        
        // Auto-scroll to bottom
        log.scrollTop = log.scrollHeight;
    }
    
    clearBattleLog() {
        document.getElementById('battle-log').innerHTML = '';
        this.addLogEntry('system', '⚔️ Der Kampf beginnt!', 'log-system');
    }
    
    updateAgentDisplay() {
        // Agent 1
        document.getElementById('agent1-name-display').textContent = this.agent1.name;
        document.getElementById('agent1-level').textContent = this.agent1.level;
        document.getElementById('agent1-attack').textContent = this.agent1.attack;
        document.getElementById('agent1-defense').textContent = this.agent1.defense;
        
        const hp1Percent = (this.agent1.hp / this.agent1.max_hp) * 100;
        document.getElementById('agent1-hp-fill').style.width = hp1Percent + '%';
        document.getElementById('agent1-hp-text').textContent = `${this.agent1.hp}/${this.agent1.max_hp}`;
        
        const stamina1Percent = (this.agent1.stamina / this.agent1.max_stamina) * 100;
        document.getElementById('agent1-stamina-fill').style.width = stamina1Percent + '%';
        document.getElementById('agent1-stamina-text').textContent = `${this.agent1.stamina}/${this.agent1.max_stamina}`;
        
        this.updateEffects('agent1', this.agent1);
        
        // Agent 2
        document.getElementById('agent2-name-display').textContent = this.agent2.name;
        document.getElementById('agent2-level').textContent = this.agent2.level;
        document.getElementById('agent2-attack').textContent = this.agent2.attack;
        document.getElementById('agent2-defense').textContent = this.agent2.defense;
        
        const hp2Percent = (this.agent2.hp / this.agent2.max_hp) * 100;
        document.getElementById('agent2-hp-fill').style.width = hp2Percent + '%';
        document.getElementById('agent2-hp-text').textContent = `${this.agent2.hp}/${this.agent2.max_hp}`;
        
        const stamina2Percent = (this.agent2.stamina / this.agent2.max_stamina) * 100;
        document.getElementById('agent2-stamina-fill').style.width = stamina2Percent + '%';
        document.getElementById('agent2-stamina-text').textContent = `${this.agent2.stamina}/${this.agent2.max_stamina}`;
        
        this.updateEffects('agent2', this.agent2);
    }
    
    updateEffects(agentId, agentData) {
        const container = document.getElementById(`${agentId}-effects`);
        container.innerHTML = '';
        
        // Buffs
        if (agentData.buffs && agentData.buffs.length > 0) {
            agentData.buffs.forEach(buff => {
                const badge = document.createElement('span');
                badge.className = 'effect-badge effect-buff';
                badge.textContent = `✨ ${buff.name}`;
                container.appendChild(badge);
            });
        }
        
        // Debuffs
        if (agentData.debuffs && agentData.debuffs.length > 0) {
            agentData.debuffs.forEach(debuff => {
                const badge = document.createElement('span');
                badge.className = 'effect-badge effect-debuff';
                badge.textContent = `💀 ${debuff.name}`;
                container.appendChild(badge);
            });
        }
    }
    
    showVictory(winnerName) {
        const title = document.getElementById('victory-title');
        const message = document.getElementById('victory-message');
        const statsContent = document.getElementById('victory-stats-content');
        
        if (winnerName === this.agent1.name) {
            title.textContent = '🏆 SIEG!';
            title.style.color = '#00ff00';
            message.textContent = `${winnerName} hat gewonnen!`;
        } else {
            title.textContent = '💀 NIEDERLAGE!';
            title.style.color = '#ff0000';
            message.textContent = `${winnerName} hat gewonnen!`;
        }
        
        statsContent.innerHTML = `
            <div class="stat-line">📊 Runden: ${this.currentRound}</div>
            <div class="stat-line">🔵 ${this.agent1.name}: ${this.agent1.hp} HP übrig</div>
            <div class="stat-line">🔴 ${this.agent2.name}: ${this.agent2.hp} HP übrig</div>
            <div class="stat-line">⭐ XP gewonnen: ${this.agent1.level * 50}</div>
        `;
        
        this.showScreen('victory-screen');
    }
    
    resetGame() {
        this.battleId = null;
        this.agent1 = null;
        this.agent2 = null;
        this.currentRound = 0;
        this.showScreen('start-screen');
    }
    
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.game = new GameController();
});
