#!/bin/bash
# ========================================
# Agent Battle Simulator - Ubuntu Setup
# ========================================

set -e  # Exit on error

echo ""
echo "========================================"
echo " Agent Battle Simulator - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 ist nicht installiert!"
    echo ""
    echo "Installation mit:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[OK] Python gefunden!"
python3 --version
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git ist nicht installiert!"
    echo ""
    echo "Installation mit:"
    echo "  sudo apt update"
    echo "  sudo apt install git"
    echo ""
    exit 1
fi

echo "[OK] Git gefunden!"
git --version
echo ""

# Install dependencies
echo "========================================"
echo " Installiere Abhaengigkeiten..."
echo "========================================"
echo ""

pip3 install -r requirements.txt

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
echo "  ./setup-auto-update-ubuntu.sh"
echo ""
echo "========================================"
