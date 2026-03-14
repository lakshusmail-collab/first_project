import speech_recognition as sr

def run_stt_demo():
    recognizer = sr.Recognizer()
    
    # TIP: If it fails, we can list microphones to find the right ID
    # print(sr.Microphone.list_microphone_names())

    try:
        with sr.Microphone() as source:
            print("\n[Status] Adjusting for background noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.energy_threshold = 300 # Sensitivity level
            
            print("[Status] Microphone is LIVE. Say something...")
            audio_data = recognizer.listen(source, timeout=10)
            
            print("[Status] Recognizing...")
            # Using Google Web Speech API (Free, no API key needed for light use)
            text = recognizer.recognize_google(audio_data)
            print(f"\n>> You said: {text}")
            return text

    except sr.RequestError:
        print("API was unreachable. Check your internet connection.")
    except sr.UnknownValueError:
        print("Unable to recognize speech. Try speaking clearer or check mic volume.")
    except AttributeError:
        print("PyAudio not found. Run: pip install pyaudio")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_stt_demo()