import subprocess
import sys
import os
import platform

# --- STEP 1: AUTO-INSTALLER ---
def install_gtts():
    try:
        import gtts
        print("✅ gTTS is already installed.")
    except ImportError:
        print("📥 gTTS not found. Installing now...")
        # This installs it to the exact Python version you are currently using
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gtts"])
        print("✅ Installation complete!")

install_gtts()
from gtts import gTTS

# --- STEP 2: ROBUST SPEECH FUNCTION ---
def speak_now(text):
    filename = "speech_output.mp3"
    
    # Generate the audio
    print(f"🎙️ Generating voice for: {text[:30]}...")
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)
    
    # Playback based on Operating System
    current_os = platform.system()
    print(f"🔊 Playing on {current_os}...")
    
    try:
        if current_os == "Windows":
            os.startfile(filename) # Better than os.system for Windows
        elif current_os == "Darwin": # macOS
            os.system(f"afplay {filename}")
        else: # Linux
            os.system(f"mpg123 {filename} || paplay {filename} || aplay {filename}")
    except Exception as e:
        print(f"❌ Playback failed: {e}")
        print(f"📂 File saved as {os.path.abspath(filename)}. You can play it manually.")

# --- TEST IT ---
test_text = "Hello? How are you?."
speak_now(test_text)