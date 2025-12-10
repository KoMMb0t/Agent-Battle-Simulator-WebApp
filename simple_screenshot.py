#!/usr/bin/env python3
"""
Simple Screenshot Generator for Agent Battle Simulator
Works on Windows without headless mode
"""

import os
import time
import subprocess
import sys

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("❌ Selenium not installed!")
    print("Run: pip install selenium webdriver-manager")
    sys.exit(1)

# Configuration
BASE_URL = "http://localhost:3000"
SCREENSHOT_DIR = "screenshots"

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
    print("⏳ Please wait 5 seconds...")
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(5)
    print(f"✅ Flask server started on {BASE_URL}")
    return process

def setup_driver():
    """Setup Chrome WebDriver WITHOUT headless mode"""
    print("🌐 Setting up Chrome WebDriver...")
    print("📌 Chrome window will open (this is normal!)")
    
    chrome_options = Options()
    # NO HEADLESS MODE - Window will be visible
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        # Try with webdriver-manager first
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            # Fallback to default
            driver = webdriver.Chrome(options=chrome_options)
        
        print("✅ Chrome WebDriver ready")
        return driver
    except Exception as e:
        print(f"❌ Error setting up WebDriver: {e}")
        print("💡 Make sure Chrome is installed")
        print("💡 Install ChromeDriver: pip install webdriver-manager")
        sys.exit(1)

def take_screenshot(driver, name, description):
    """Take a screenshot and save it"""
    filepath = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(filepath)
    print(f"📸 Screenshot saved: {name}.png - {description}")
    time.sleep(2)  # Longer wait for stability

def main():
    """Main automation flow"""
    print("=" * 60)
    print("🎮 Agent Battle Simulator - Simple Screenshot Generator")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANT: Chrome window will open!")
    print("⚠️  DO NOT close it manually!")
    print("⚠️  Let the script finish automatically!")
    print()
    
    # Setup
    setup_directories()
    flask_process = start_flask_server()
    
    input("Press ENTER to start Chrome and begin screenshots...")
    
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        # 1. Bot Selection Screen
        print("\n📍 Step 1: Opening Bot Selection Screen...")
        driver.get(BASE_URL)
        time.sleep(4)
        take_screenshot(driver, "01_bot_selection", "Bot Selection Screen with 21 bots")
        
        # 2. Select bots
        print("\n📍 Step 2: Selecting bots...")
        try:
            # Try to select Sentinel for Agent 2
            sentinel_card = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-agent="2"][data-bot-id="sentinel"]'))
            )
            sentinel_card.click()
            time.sleep(2)
            take_screenshot(driver, "02_bots_selected", "Bots selected")
        except Exception as e:
            print(f"   ⚠️  Could not select bot: {e}")
            take_screenshot(driver, "02_bots_selected", "Default bots")
        
        # 3. Start Battle
        print("\n📍 Step 3: Starting Battle...")
        try:
            start_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "confirm-selection-btn"))
            )
            start_btn.click()
            time.sleep(3)
            take_screenshot(driver, "03_battle_start", "Battle Screen - Round 1")
        except Exception as e:
            print(f"   ⚠️  Could not start battle: {e}")
        
        # 4. Battle Screen Details
        print("\n📍 Step 4: Capturing Battle UI...")
        time.sleep(2)
        take_screenshot(driver, "04_battle_ui", "Battle UI with HP/Stamina/XP bars")
        
        # 5. Execute Actions
        print("\n📍 Step 5: Executing actions...")
        for i in range(3):
            try:
                action_btn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-btn"))
                )
                action_btn.click()
                time.sleep(3)
                if i == 0:
                    take_screenshot(driver, "05_action_executed", "After first action")
                elif i == 2:
                    take_screenshot(driver, "06_mid_battle", "Mid-battle state")
            except Exception as e:
                print(f"   ⚠️  Could not execute action {i+1}: {e}")
                break
        
        # 6. Continue to victory
        print("\n📍 Step 6: Fighting to victory...")
        print("   (This may take a while...)")
        
        max_rounds = 25
        for round_num in range(max_rounds):
            try:
                # Check if victory
                victory_screen = driver.find_element(By.ID, "victory-screen")
                if "active" in victory_screen.get_attribute("class"):
                    print(f"   ✅ Victory achieved!")
                    time.sleep(2)
                    take_screenshot(driver, "07_victory_screen", "Victory Screen")
                    break
            except:
                pass
            
            # Execute action
            try:
                action_btn = driver.find_element(By.CSS_SELECTOR, ".action-btn")
                action_btn.click()
                time.sleep(2)
            except:
                print(f"   ⚠️  Battle ended at round {round_num}")
                break
        
        # 7. Final screenshot
        print("\n📍 Step 7: Final screenshot...")
        take_screenshot(driver, "08_final_state", "Final game state")
        
        print("\n" + "=" * 60)
        print("✅ ALL SCREENSHOTS COMPLETED!")
        print(f"📁 Location: {os.path.abspath(SCREENSHOT_DIR)}/")
        print("=" * 60)
        print()
        print("You can now close Chrome window.")
        
    except Exception as e:
        print(f"\n❌ Error during automation: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        input("Press ENTER to close Chrome and stop server...")
        driver.quit()
        flask_process.terminate()
        flask_process.wait()
        print("✅ Cleanup complete")

if __name__ == "__main__":
    main()
