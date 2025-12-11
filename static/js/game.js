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
        const legacyStartBtn = document.getElementById('start-battle-btn');
        if (legacyStartBtn) {
            legacyStartBtn.addEventListener('click', () => this.startBattleLegacy());
        }

        const nameInputs = [
            document.getElementById('agent1-name-input'),
            document.getElementById('agent2-name-input'),
            document.getElementById('agent1-name'),
            document.getElementById('agent2-name')
        ].filter(Boolean);

        nameInputs.forEach(input => {
            input.addEventListener('input', () => this.validateSelection());
        });

        this.validateSelection();
    }
    
    async loadBots() {
        try {
            const response = await fetch('/api/bots');
            const { data, rawText } = await this.parseJson(response);
            if (!response.ok) {
                throw new Error(data?.message || rawText || 'Bots konnten nicht geladen werden');
            }

            if (!data) {
                throw new Error('Ungültige Antwort beim Laden der Bots.');
            }

            this.bots = data;
            console.log('Bots loaded:', this.bots.length);
            this.renderBotSelection();
        } catch (error) {
            console.error('Error loading bots:', error);
            this.showToast(error.message || 'Fehler beim Laden der Bots.', 'error');
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

        this.validateSelection();
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

            this.validateSelection();
        }
    }
    
    async loadActions() {
        try {
            const response = await fetch('/api/actions');
            const { data, rawText } = await this.parseJson(response);
            if (!response.ok) {
                throw new Error(data?.message || rawText || 'Aktionen konnten nicht geladen werden');
            }

            if (!data) {
                throw new Error('Ungültige Antwort beim Laden der Aktionen.');
            }

            this.actions = data;
            console.log('Actions loaded:', this.actions);
        } catch (error) {
            console.error('Error loading actions:', error);
            this.showToast(error.message || 'Fehler beim Laden der Aktionen.', 'error');
        }
    }
    
    async confirmSelection() {
        if (!this.isSelectionValid()) {
            this.showToast('Bitte gültige Agentennamen und Bots auswählen.', 'error');
            return;
        }

        const agent1Name = document.getElementById('agent1-name-input').value.trim() || 'Agent Alpha';
        const agent2Name = document.getElementById('agent2-name-input').value.trim() || 'Agent Beta';

        await this.startBattleWithOptions({
            agent1Name,
            agent2Name,
            agent1Bot: this.selectedBot1,
            agent2Bot: this.selectedBot2
        });
    }

    async startBattleLegacy() {
        const agent1Name = document.getElementById('agent1-name')?.value.trim() || 'Agent Alpha';
        const agent2Name = document.getElementById('agent2-name')?.value.trim() || 'Agent Beta';

        await this.startBattleWithOptions({
            agent1Name,
            agent2Name,
            agent1Bot: this.selectedBot1 || 'mende',
            agent2Bot: this.selectedBot2 || 'regulus'
        });
    }

    async startBattleWithOptions({ agent1Name, agent2Name, agent1Bot, agent2Bot }) {
        try {
            console.log('Starting battle with:', { agent1Name, agent2Name, agent1Bot, agent2Bot });
            const response = await fetch('/api/battle/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent1_name: agent1Name,
                    agent2_name: agent2Name,
                    agent1_bot: agent1Bot,
                    agent2_bot: agent2Bot
                })
            });

            const { data, rawText } = await this.parseJson(response);
            console.log('Battle start response:', { data, rawText });
            if (!response.ok) {
                throw new Error(data?.message || rawText || 'Fehler beim Starten des Kampfes');
            }

            if (!data) {
                throw new Error('Ungültige Server-Antwort.');
            }

            this.battleId = data.battle_id;
            this.agent1 = data.agent1;
            this.agent2 = data.agent2;
            this.currentRound = 1;
            console.log('Battle initialized:', { battleId: this.battleId, agent1: this.agent1?.name, agent2: this.agent2?.name });

            // Switch to battle screen
            this.showScreen('battle-screen');
            this.updateBattleUI();
            this.renderActionButtons();

        } catch (error) {
            console.error('Error starting battle:', error);
            this.showToast(error.message || 'Fehler beim Starten des Kampfes!', 'error');
        }
    }
    
    renderActionButtons() {
        const container = document.getElementById('actions-grid');
        if (!container) return;
        container.innerHTML = '';
        
        this.actions.forEach((action, index) => {
            const button = document.createElement('button');
            button.className = 'action-btn';
            button.innerHTML = `
                <div class="action-number">${index + 1}</div>
                <div class="action-name">${action.name}</div>
                <div class="action-details">
                    <span class="stamina-cost">⚡ ${action.stamina_cost}</span>
                    <span class="damage-range">💥 ${action.damage_range[0]}-${action.damage_range[1]}</span>
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

            const { data, rawText } = await this.parseJson(response);
            if (!response.ok) {
                throw new Error(data?.message || rawText || 'Fehler beim Ausführen der Aktion');
            }

            if (!data) {
                throw new Error('Ungültige Server-Antwort.');
            }
            
            // Update agents from API response
            // API returns agent1_state and agent2_state (not battle_state)
            window.debugLog?.('🔍 BEFORE agent assignment', {
                hasAgent1State: !!data.agent1_state,
                hasAgent2State: !!data.agent2_state,
                hasAgent1Direct: !!data.agent1,
                hasAgent2Direct: !!data.agent2
            });
            
            this.agent1 = data.agent1_state || data.agent1;
            this.agent2 = data.agent2_state || data.agent2;
            this.currentRound = data.round;
            
            window.debugLog?.('✅ AFTER agent assignment', {
                agent1HP: this.agent1?.hp,
                agent2HP: this.agent2?.hp,
                agent1Stamina: this.agent1?.stamina,
                agent2Stamina: this.agent2?.stamina
            });
            
            // Update UI
            this.updateBattleUI();
            
            // Add combat log entries for each action
            if (data.actions && Array.isArray(data.actions)) {
                data.actions.forEach(action => {
                    const logText = `${action.attacker}: ${action.action} (${action.damage} Schaden) - ${action.comment}`;
                    this.addCombatLog(logText);
                });
            }
            
            // Check for winner
            if (data.winner) {
                setTimeout(() => this.showVictoryScreen(data.winner), 1500);
            }
            
        } catch (error) {
            console.error('Error executing action:', error);
            this.showToast(error.message || 'Fehler beim Ausführen der Aktion!', 'error');
        } finally {
            this.isProcessing = false;
        }
    }
    
    updateBattleUI() {
        window.debugLog?.('🔄 updateBattleUI called', {
            round: this.currentRound,
            agent1HP: this.agent1?.hp,
            agent2HP: this.agent2?.hp,
            agent1Stamina: this.agent1?.stamina,
            agent2Stamina: this.agent2?.stamina
        });
        
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
        const log = document.getElementById('battle-log');
        if (!log) return;
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.textContent = `⚔️ ${commentary}`;
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
    }

    showVictoryScreen(winner) {
        const winnerNameEl = document.getElementById('winner-name');
        const victoryMessageEl = document.getElementById('victory-message');

        if (winnerNameEl) {
            winnerNameEl.textContent = winner;
        }

        if (victoryMessageEl) {
            victoryMessageEl.textContent = `Glückwunsch, ${winner}!`;
        }

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
        document.getElementById('battle-log').innerHTML = '';
        this.showScreen('agent-selection-screen');
    }

    isSelectionValid() {
        const namePattern = /^[A-Za-z0-9ÄÖÜäöüß\s\-_.]{1,20}$/;
        const agent1Input = document.getElementById('agent1-name-input') || document.getElementById('agent1-name');
        const agent2Input = document.getElementById('agent2-name-input') || document.getElementById('agent2-name');

        const agent1Name = agent1Input?.value.trim();
        const agent2Name = agent2Input?.value.trim();

        const namesValid = Boolean(agent1Name && agent2Name && namePattern.test(agent1Name) && namePattern.test(agent2Name));
        const botsValid = Boolean(this.selectedBot1 && this.selectedBot2);

        return namesValid && botsValid;
    }

    validateSelection() {
        const confirmBtn = document.getElementById('confirm-selection-btn');
        const legacyBtn = document.getElementById('start-battle-btn');

        const isValid = this.isSelectionValid();
        if (confirmBtn) {
            confirmBtn.disabled = !isValid;
        }
        if (legacyBtn) {
            legacyBtn.disabled = !isValid;
        }
    }

    async parseJson(response) {
        try {
            const rawText = await response.text();
            try {
                const data = rawText ? JSON.parse(rawText) : null;
                return { data, rawText };
            } catch (parseError) {
                console.warn('Failed to parse JSON response', parseError);
                return { data: null, rawText };
            }
        } catch (error) {
            console.warn('Failed to read response', error);
            return { data: null, rawText: '' };
        }
    }

    showToast(message, type = 'info') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 50);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.game = new GameController();
});
