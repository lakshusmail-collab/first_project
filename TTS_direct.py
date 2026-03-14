import io
import time
import pygame
from gtts import gTTS

def speak_directly(text):
    # 1. Initialize the mixer
    pygame.mixer.init()
    
    # 2. Create an in-memory "file"
    mp3_buffer = io.BytesIO()
    
    # 3. Write gTTS output to the buffer instead of a file
    print("🎙️ Generating audio in memory...")
    tts = gTTS(text=text, lang='en')
    tts.write_to_fp(mp3_buffer)
    
    # 4. Rewind the buffer to the beginning so pygame can read it
    mp3_buffer.seek(0)
    
    # 5. Load and Play
    pygame.mixer.music.load(mp3_buffer, "mp3")
    pygame.mixer.music.play()
    
    # 6. Keep the script alive until the audio finishes
    print("🔊 Playing...")
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# --- Test ---
sample_text = "In the LangChain ecosystem, a Document is the primary abstraction for representing a piece of text and its associated metadata. It is the foundational building block for retrieval-augmented generation (RAG) and other document-processing workflows. ."
speak_directly(sample_text)