// Agent Battle Simulator - Game Controller
// Frontend JavaScript

class GameController {
    constructor() {
        this.battleId = null;
        this.agent1 = null;
        this.agent2 = null;
        this.actions = [];
        this.bots = [];
        this.selectedBot1 = null;
        this.selectedBot2 = null;
        this.currentRound = 0;
        this.isProcessing = false;
        
        this.init();
    }
    
    async init() {
        // Load bots and actions
        await this.loadBots();
        await this.loadActions();
        
        // Event listeners
        document.getElementById('confirm-selection-btn').addEventListener('click', () => this.confirmSelection());
        document.getElementById('new-battle-btn').addEventListener('click', () => this.resetGame());
    }
    
    async loadBots() {
        try {
            const response = await fetch('/api/bots');
            this.bots = await response.json();
            console.log('Bots loaded:', this.bots.length);
            this.renderBotSelection();
        } catch (error) {
            console.error('Error loading bots:', error);
        }
    }
    
    renderBotSelection() {
        const agent1Grid = document.getElementById('agent1-types');
        const agent2Grid = document.getElementById('agent2-types');
        
        agent1Grid.innerHTML = '';
        agent2Grid.innerHTML = '';
        
        this.bots.forEach(bot => {
            // Agent 1 bot card
            const card1 = this.createBotCard(bot, 1);
            agent1Grid.appendChild(card1);
            
            // Agent 2 bot card
            const card2 = this.createBotCard(bot, 2);
            agent2Grid.appendChild(card2);
        });
        
        // Select default bots
        this.selectBot('mende', 1);
        this.selectBot('regulus', 2);
    }
    
    createBotCard(bot, agentNum) {
        const card = document.createElement('div');
        card.className = 'bot-card';
        card.dataset.botId = bot.id;
        card.dataset.agent = agentNum;
        
        card.innerHTML = `
            <div class="bot-avatar" style="font-size: 3rem;">${bot.avatar}</div>
            <div class="bot-name">${bot.name}</div>
            <div class="bot-title">${bot.title}</div>
            <div class="bot-stats">
                <div>HP: +${bot.stats.hp_bonus}</div>
                <div>ATK: +${bot.stats.attack_bonus}</div>
                <div>DEF: +${bot.stats.defense_bonus}</div>
                <div>STA: +${bot.stats.stamina_bonus}</div>
            </div>
            <div class="bot-special">${bot.special}</div>
        `;
        
        card.style.borderColor = bot.color;
        
        card.addEventListener('click', () => this.selectBot(bot.id, agentNum));
        
        return card;
    }
    
    selectBot(botId, agentNum) {
        // Remove previous selection
        const grid = document.getElementById(`agent${agentNum}-types`);
        grid.querySelectorAll('.bot-card').forEach(c => c.classList.remove('selected'));
        
        // Select new bot
        const card = grid.querySelector(`[data-bot-id="${botId}"]`);
        if (card) {
            card.classList.add('selected');
            if (agentNum === 1) {
                this.selectedBot1 = botId;
            } else {
                this.selectedBot2 = botId;
            }
        }
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
    
    async confirmSelection() {
        if (!this.selectedBot1 || !this.selectedBot2) {
            alert('Bitte wähle Bots für beide Agents!');
            return;
        }
        
        const agent1Name = document.getElementById('agent1-name-input').value.trim() || 'Agent Alpha';
        const agent2Name = document.getElementById('agent2-name-input').value.trim() || 'Agent Beta';
        
        try {
            const response = await fetch('/api/battle/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent1_name: agent1Name,
                    agent2_name: agent2Name,
                    agent1_bot: this.selectedBot1,
                    agent2_bot: this.selectedBot2
                })
            });
            
            const data = await response.json();
            this.battleId = data.battle_id;
            this.agent1 = data.agent1;
            this.agent2 = data.agent2;
            this.currentRound = 1;
            
            // Switch to battle screen
            this.showScreen('battle-screen');
            this.updateBattleUI();
            this.renderActionButtons();
            
        } catch (error) {
            console.error('Error starting battle:', error);
            alert('Fehler beim Starten des Kampfes!');
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
                    agent2_name: agent2Name,
                    agent1_bot: 'mende',
                    agent2_bot: 'regulus'
                })
            });
            
            const data = await response.json();
            this.battleId = data.battle_id;
            this.agent1 = data.agent1;
            this.agent2 = data.agent2;
            this.currentRound = 1;
            
            // Switch to battle screen
            this.showScreen('battle-screen');
            this.updateBattleUI();
            this.renderActionButtons();
            
        } catch (error) {
            console.error('Error starting battle:', error);
            alert('Fehler beim Starten des Kampfes!');
        }
    }
    
    renderActionButtons() {
        const container = document.getElementById('action-buttons');
        container.innerHTML = '';
        
        this.actions.forEach((action, index) => {
            const button = document.createElement('button');
            button.className = 'action-btn';
            button.innerHTML = `
                <div class="action-number">${index + 1}</div>
                <div class="action-name">${action.emoji} ${action.name}</div>
                <div class="action-details">
                    <span class="stamina-cost">⚡ ${action.stamina_cost}</span>
                    <span class="damage-range">💥 ${action.damage_min}-${action.damage_max}</span>
                </div>
            `;
            
            button.addEventListener('click', () => this.executeAction(action.id));
            container.appendChild(button);
        });
    }
    
    async executeAction(actionId) {
        if (this.isProcessing) return;
        
        // Check if battle is over
        if (!this.agent1.hp || !this.agent2.hp || this.agent1.hp <= 0 || this.agent2.hp <= 0) {
            return;
        }
        
        this.isProcessing = true;
        
        try {
            const response = await fetch('/api/battle/turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    battle_id: this.battleId,
                    action_id: actionId
                })
            });
            
            const data = await response.json();
            
            // Update agents
            this.agent1 = data.agent1;
            this.agent2 = data.agent2;
            this.currentRound = data.round;
            
            // Update UI
            this.updateBattleUI();
            this.addCombatLog(data.commentary);
            
            // Check for winner
            if (data.winner) {
                setTimeout(() => this.showVictoryScreen(data.winner), 1500);
            }
            
        } catch (error) {
            console.error('Error executing action:', error);
            alert('Fehler beim Ausführen der Aktion!');
        } finally {
            this.isProcessing = false;
        }
    }
    
    updateBattleUI() {
        // Update round
        document.getElementById('round-number').textContent = this.currentRound;
        
        // Update Agent 1
        this.updateAgentDisplay(this.agent1, 1);
        
        // Update Agent 2
        this.updateAgentDisplay(this.agent2, 2);
    }
    
    updateAgentDisplay(agent, num) {
        // Name & Level
        document.getElementById(`agent${num}-name-display`).textContent = agent.name;
        document.getElementById(`agent${num}-level`).textContent = agent.level;
        
        // Avatar
        const avatar = document.getElementById(`agent${num}-avatar`);
        if (avatar) {
            avatar.textContent = agent.avatar || '🤖';
            avatar.style.color = agent.color || '#00ff00';
        }
        
        // HP
        const hpPercent = (agent.hp / agent.max_hp) * 100;
        document.getElementById(`agent${num}-hp-fill`).style.width = `${hpPercent}%`;
        document.getElementById(`agent${num}-hp-text`).textContent = `${agent.hp}/${agent.max_hp}`;
        
        // Stamina
        const staminaPercent = (agent.stamina / agent.max_stamina) * 100;
        document.getElementById(`agent${num}-stamina-fill`).style.width = `${staminaPercent}%`;
        document.getElementById(`agent${num}-stamina-text`).textContent = `${agent.stamina}/${agent.max_stamina}`;
        
        // XP
        const xpPercent = agent.xp_percentage || 0;
        document.getElementById(`agent${num}-xp-fill`).style.width = `${xpPercent}%`;
        document.getElementById(`agent${num}-xp-text`).textContent = `${agent.xp}/${agent.xp_to_next_level}`;
        
        // Stats
        document.getElementById(`agent${num}-attack`).textContent = agent.attack;
        document.getElementById(`agent${num}-defense`).textContent = agent.defense;
        
        // Effects (Buffs/Debuffs)
        this.updateEffects(agent, num);
    }
    
    updateEffects(agent, num) {
        const container = document.getElementById(`agent${num}-effects`);
        container.innerHTML = '';
        
        // Buffs
        agent.buffs.forEach(buff => {
            const badge = document.createElement('span');
            badge.className = 'effect-badge buff';
            badge.textContent = `✨ ${buff.name}`;
            container.appendChild(badge);
        });
        
        // Debuffs
        agent.debuffs.forEach(debuff => {
            const badge = document.createElement('span');
            badge.className = 'effect-badge debuff';
            badge.textContent = `💀 ${debuff.name}`;
            container.appendChild(badge);
        });
    }
    
    addCombatLog(commentary) {
        const log = document.getElementById('combat-log');
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.textContent = `⚔️ ${commentary}`;
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
    }
    
    showVictoryScreen(winner) {
        document.getElementById('winner-name').textContent = winner;
        this.showScreen('victory-screen');
    }
    
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }
    
    resetGame() {
        this.battleId = null;
        this.agent1 = null;
        this.agent2 = null;
        this.currentRound = 0;
        document.getElementById('combat-log').innerHTML = '';
        this.showScreen('agent-selection-screen');
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.game = new GameController();
});
