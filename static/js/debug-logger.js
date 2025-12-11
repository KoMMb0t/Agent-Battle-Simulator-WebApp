// Debug Logger - Captures all logs visually
(function() {
    // Create log container
    const logContainer = document.createElement('div');
    logContainer.id = 'debug-log-container';
    logContainer.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        width: 400px;
        max-height: 600px;
        background: rgba(0, 0, 0, 0.9);
        color: #0f0;
        font-family: monospace;
        font-size: 11px;
        padding: 10px;
        overflow-y: auto;
        z-index: 99999;
        border: 2px solid #0f0;
        border-radius: 5px;
    `;
    document.body.appendChild(logContainer);

    // Log function
    window.debugLog = function(message, data = null) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.style.cssText = 'margin-bottom: 5px; border-bottom: 1px solid #333; padding-bottom: 3px;';
        
        let content = `[${timestamp}] ${message}`;
        if (data !== null) {
            try {
                content += '\n' + JSON.stringify(data, null, 2);
            } catch(e) {
                content += '\n[Cannot stringify: ' + e.message + ']';
            }
        }
        
        logEntry.textContent = content;
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
        
        // Also log to console (if it works)
        console.log(message, data);
    };

    window.debugLog('🚀 Debug Logger initialized');

    // Wrap fetch to log all API calls
    const originalFetch = window.fetch;
    window.fetch = async function(...args) {
        const url = args[0];
        const options = args[1] || {};
        
        debugLog('📡 FETCH REQUEST', { url, method: options.method || 'GET' });
        
        try {
            const response = await originalFetch(...args);
            const clonedResponse = response.clone();
            
            try {
                const text = await clonedResponse.text();
                debugLog('📥 FETCH RESPONSE', { 
                    url, 
                    status: response.status,
                    ok: response.ok,
                    bodyLength: text.length,
                    bodyPreview: text.substring(0, 200)
                });
                
                // Try to parse as JSON
                try {
                    const json = JSON.parse(text);
                    debugLog('✅ PARSED JSON', json);
                } catch(e) {
                    debugLog('⚠️ Not JSON or parse failed');
                }
            } catch(e) {
                debugLog('❌ Failed to read response body', e.message);
            }
            
            return response;
        } catch(error) {
            debugLog('❌ FETCH ERROR', { url, error: error.message });
            throw error;
        }
    };

    // Wrap GameController methods
    window.addEventListener('load', () => {
        setTimeout(() => {
            if (window.game) {
                debugLog('🎮 Game controller found, wrapping methods...');
                
                // Wrap startBattleWithOptions
                const originalStart = window.game.startBattleWithOptions.bind(window.game);
                window.game.startBattleWithOptions = async function(options) {
                    debugLog('🏁 startBattleWithOptions called', options);
                    try {
                        const result = await originalStart(options);
                        debugLog('✅ startBattleWithOptions completed', {
                            battleId: this.battleId,
                            agent1Name: this.agent1?.name,
                            agent2Name: this.agent2?.name,
                            agent1Hp: this.agent1?.hp,
                            agent2Hp: this.agent2?.hp
                        });
                        return result;
                    } catch(error) {
                        debugLog('❌ startBattleWithOptions error', error.message);
                        throw error;
                    }
                };

                // Wrap executeAction
                const originalExecute = window.game.executeAction.bind(window.game);
                window.game.executeAction = async function(actionId) {
                    debugLog('⚔️ executeAction called', { actionId });
                    try {
                        const result = await originalExecute(actionId);
                        debugLog('✅ executeAction completed', {
                            agent1Hp: this.agent1?.hp,
                            agent2Hp: this.agent2?.hp,
                            round: this.currentRound
                        });
                        return result;
                    } catch(error) {
                        debugLog('❌ executeAction error', error.message);
                        throw error;
                    }
                };

                debugLog('✅ Methods wrapped successfully');
            } else {
                debugLog('⚠️ Game controller not found');
            }
        }, 1000);
    });

    // Catch all errors
    window.addEventListener('error', (event) => {
        debugLog('❌ GLOBAL ERROR', {
            message: event.message,
            filename: event.filename,
            lineno: event.lineno,
            colno: event.colno
        });
    });

    window.addEventListener('unhandledrejection', (event) => {
        debugLog('❌ UNHANDLED PROMISE REJECTION', {
            reason: event.reason?.message || event.reason
        });
    });

})();
