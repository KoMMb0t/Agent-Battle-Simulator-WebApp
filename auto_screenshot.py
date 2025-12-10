#!/usr/bin/env python3
"""
Automatic Screenshot Generator for Agent Battle Simulator
Creates screenshots for Hackathon submission automatically
"""

import os
import time
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Configuration
BASE_URL = "http://localhost:3000"
SCREENSHOT_DIR = "screenshots"
FLASK_PORT = 3000

def setup_directories():
    """Create screenshots directory"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
        print(f"✅ Created directory: {SCREENSHOT_DIR}/")
    else:
        print(f"✅ Directory exists: {SCREENSHOT_DIR}/")

def start_flask_server():
    """Start Flask server in background"""
    print("🚀 Starting Flask server...")
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # Wait for server to start
    print(f"✅ Flask server started on {BASE_URL}")
    return process

def setup_driver():
    """Setup Chrome WebDriver with headless mode"""
    print("🌐 Setting up Chrome WebDriver...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome WebDriver ready")
        return driver
    except Exception as e:
        print(f"❌ Error setting up WebDriver: {e}")
        print("💡 Install ChromeDriver: sudo apt-get install chromium-chromedriver")
        sys.exit(1)

def take_screenshot(driver, name, description):
    """Take a screenshot and save it"""
    filepath = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(filepath)
    print(f"📸 Screenshot saved: {name}.png - {description}")
    time.sleep(1)

def main():
    """Main automation flow"""
    print("=" * 60)
    print("🎮 Agent Battle Simulator - Auto Screenshot Generator")
    print("=" * 60)
    print()
    
    # Setup
    setup_directories()
    flask_process = start_flask_server()
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. Bot Selection Screen
        print("\n📍 Step 1: Bot Selection Screen")
        driver.get(BASE_URL)
        time.sleep(3)
        take_screenshot(driver, "01_bot_selection", "Bot Selection Screen with 21 bots")
        
        # Select bots
        print("   Selecting bots...")
        # Select Mende for Agent 1 (should be pre-selected)
        # Select Sentinel for Agent 2
        try:
            sentinel_card = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-agent="2"][data-bot-id="sentinel"]'))
            )
            sentinel_card.click()
            time.sleep(1)
            take_screenshot(driver, "02_bots_selected", "Bots selected (Mende vs Sentinel)")
        except:
            print("   ⚠️  Could not select specific bot, using defaults")
        
        # 2. Start Battle
        print("\n📍 Step 2: Starting Battle")
        try:
            start_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "confirm-selection-btn"))
            )
            start_btn.click()
            time.sleep(2)
            take_screenshot(driver, "03_battle_start", "Battle Screen - Round 1")
        except:
            print("   ⚠️  Could not start battle")
        
        # 3. Battle Screen - Initial State
        print("\n📍 Step 3: Battle Screen Details")
        time.sleep(1)
        take_screenshot(driver, "04_battle_ui", "Battle UI with HP/Stamina/XP bars")
        
        # 4. Execute Action
        print("\n📍 Step 4: Executing Action")
        try:
            # Click first action button (Feuerball)
            action_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-btn"))
            )
            action_btn.click()
            time.sleep(2)
            take_screenshot(driver, "05_action_executed", "After action - HP/Stamina updated")
        except:
            print("   ⚠️  Could not execute action")
        
        # 5. Mid-Battle
        print("\n📍 Step 5: Mid-Battle State")
        try:
            # Execute 2 more actions
            for i in range(2):
                action_btn = driver.find_element(By.CSS_SELECTOR, ".action-btn")
                action_btn.click()
                time.sleep(2)
            take_screenshot(driver, "06_mid_battle", "Mid-battle with buffs/debuffs")
        except:
            print("   ⚠️  Could not continue battle")
        
        # 6. Continue until victory
        print("\n📍 Step 6: Fighting to Victory")
        try:
            max_rounds = 20
            for round_num in range(max_rounds):
                # Check if battle is over
                try:
                    victory_screen = driver.find_element(By.ID, "victory-screen")
                    if "active" in victory_screen.get_attribute("class"):
                        print(f"   ✅ Victory achieved in {round_num} rounds!")
                        break
                except:
                    pass
                
                # Execute action
                try:
                    action_btn = driver.find_element(By.CSS_SELECTOR, ".action-btn")
                    action_btn.click()
                    time.sleep(1.5)
                except:
                    print(f"   ⚠️  Could not execute action in round {round_num}")
                    break
            
            time.sleep(2)
            take_screenshot(driver, "07_victory_screen", "Victory Screen with stats")
        except Exception as e:
            print(f"   ⚠️  Error during battle: {e}")
        
        # 7. Final Screenshot
        print("\n📍 Step 7: Final Screenshot")
        take_screenshot(driver, "08_final_state", "Final game state")
        
        print("\n" + "=" * 60)
        print("✅ ALL SCREENSHOTS COMPLETED!")
        print(f"📁 Location: {os.path.abspath(SCREENSHOT_DIR)}/")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during automation: {e}")
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        driver.quit()
        flask_process.terminate()
        flask_process.wait()
        print("✅ Cleanup complete")

if __name__ == "__main__":
    main()
