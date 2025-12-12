#!/data/data/com.termux/files/usr/bin/bash
# ========================================
# Agent Battle Simulator - Android Setup
# (Requires Termux)
# ========================================

set -e  # Exit on error

echo ""
echo "========================================"
echo " Agent Battle Simulator - Android Setup"
echo " (via Termux)"
echo "========================================"
echo ""

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "[ERROR] Dieses Script muss in Termux ausgefuehrt werden!"
    echo ""
    echo "Bitte installiere Termux von:"
    echo "  F-Droid: https://f-droid.org/packages/com.termux/"
    echo ""
    exit 1
fi

echo "[OK] Termux erkannt!"
echo ""

# Update package list
echo "========================================"
echo " Update Termux Pakete..."
echo "========================================"
echo ""
pkg update -y

# Install Python
if ! command -v python &> /dev/null; then
    echo "Installiere Python..."
    pkg install python -y
fi

echo "[OK] Python gefunden!"
python --version
echo ""

# Install Git
if ! command -v git &> /dev/null; then
    echo "Installiere Git..."
    pkg install git -y
fi

echo "[OK] Git gefunden!"
git --version
echo ""

# Install dependencies
echo "========================================"
echo " Installiere Abhaengigkeiten..."
echo "========================================"
echo ""

pip install -r requirements.txt

echo ""
echo "========================================"
echo " Installation erfolgreich!"
echo "========================================"
echo ""
echo "Das Spiel ist jetzt bereit!"
echo ""
echo "Zum Starten:"
echo "  ./start-game.sh"
echo ""
echo "Zum Auto-Update aktivieren:"
echo "  ./setup-auto-update-android.sh"
echo ""
echo "HINWEIS:"
echo "  Oeffne im Browser: http://localhost:3000"
echo ""
echo "========================================"
