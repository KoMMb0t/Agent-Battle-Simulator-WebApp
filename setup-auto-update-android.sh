#!/data/data/com.termux/files/usr/bin/bash
# ========================================
# Auto-Update Setup - Android (Termux)
# ========================================

set -e

echo ""
echo "========================================"
echo " Auto-Update Setup (Android/Termux)"
echo "========================================"
echo ""

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "[ERROR] Dieses Script muss in Termux ausgefuehrt werden!"
    exit 1
fi

# Install cronie if not installed
if ! command -v crond &> /dev/null; then
    echo "Installiere cronie..."
    pkg install cronie -y
fi

# Get current directory
REPO_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Repository: $REPO_PATH"
echo ""

# Create update script
echo "Creating update script..."

cat > "$REPO_PATH/auto-update.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

REPO_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_PATH"

# Check for local changes
if [[ -n $(git status -s) ]]; then
    echo "[SKIP] Lokale Aenderungen gefunden, ueberspringe Update" >> "$REPO_PATH/update.log"
    exit 0
fi

# Fetch and pull
git fetch origin > /dev/null 2>&1

LOCAL=$(git rev-parse @ 2>/dev/null)
REMOTE=$(git rev-parse @{u} 2>/dev/null)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "[UPDATE] Neue Version gefunden, pulling..." >> "$REPO_PATH/update.log"
    git pull origin main > /dev/null 2>&1 || git pull origin master > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "[OK] Update erfolgreich: $(date)" >> "$REPO_PATH/update.log"
    else
        echo "[ERROR] Update fehlgeschlagen: $(date)" >> "$REPO_PATH/update.log"
    fi
else
    echo "[OK] Bereits aktuell: $(date)" >> "$REPO_PATH/update.log"
fi
EOF

chmod +x "$REPO_PATH/auto-update.sh"

echo "[OK] Update script erstellt!"
echo ""

# Setup cron job
echo "========================================"
echo " Erstelle Cron Job..."
echo "========================================"
echo ""

# Create crontab directory if not exists
mkdir -p ~/.termux/boot

# Remove existing cron job if exists
crontab -l 2>/dev/null | grep -v "auto-update.sh" | crontab - 2>/dev/null || true

# Add new cron job (every 10 minutes)
(crontab -l 2>/dev/null; echo "*/10 * * * * $REPO_PATH/auto-update.sh") | crontab -

# Start crond if not running
if ! pgrep crond > /dev/null; then
    crond
    echo "[OK] Cron Daemon gestartet"
fi

echo ""
echo "========================================"
echo " Auto-Update aktiviert!"
echo "========================================"
echo ""
echo "Das Repository wird jetzt automatisch"
echo "alle 10 Minuten aktualisiert!"
echo ""
echo "Log-Datei: $REPO_PATH/update.log"
echo ""
echo "WICHTIG:"
echo "  Termux muss im Hintergrund laufen!"
echo "  Aktiviere 'Acquire wakelock' in Termux"
echo "  Einstellungen fuer zuverlaessige Updates."
echo ""
echo "Zum Deaktivieren:"
echo "  crontab -e"
echo "  (Zeile mit auto-update.sh loeschen)"
echo ""
echo "Zum Testen:"
echo "  ./auto-update.sh"
echo "  cat update.log"
echo ""
echo "========================================"
