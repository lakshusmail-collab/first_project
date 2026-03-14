from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyCFPPK7Ky0wJ2Y4xhPe9BLc8S5fiDf3NLc")

# Load your image
with open("Thrissur.jpg.jpeg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        "What is happening in this image?"
    ]
)

print(response.text)