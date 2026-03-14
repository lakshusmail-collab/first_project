from google import genai
from google.genai import types

# 1. Setup the Client
client = genai.Client(api_key="AIzaSyCFPPK7Ky0wJ2Y4xhPe9BLc8S5fiDf3NLc")
MODEL_ID = "gemini-2.5-flash"

def summarize_youtube_video(video_url):
    print(f"🎬 Analyzing video: {video_url}...")
    
    # 2. Define the prompt
    # We ask for both a transcription check and a summary
    prompt = """
    Please watch this video and provide the following:
    1. A concise summary of the main topics.
    2. A structured transcript or outline of key points with timestamps.
    3. The overall tone and target audience of the video.
    """

    # 3. Call the model
    # Gemini 2.5 Flash supports direct YouTube URIs
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[
            types.Part.from_uri(
                file_uri=video_url,
                mime_type="video/mp4" # Required even for YT links
            ),
            prompt
        ],
        config=types.GenerateContentConfig(
            temperature=0.2, # Low temperature for factual accuracy
        )
    )

    return response.text

# --- Execution ---
url = "https://www.youtube.com/watch?v=ItIM_cjBMy4"
try:
    result = summarize_youtube_video(url)
    print("\n--- VIDEO ANALYSIS ---\n")
    print(result)
except Exception as e:
    print(f"An error occurred: {e}")