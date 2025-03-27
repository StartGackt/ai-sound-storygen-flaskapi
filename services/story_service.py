import os
from openai import OpenAI
from dotenv import load_dotenv
from gtts import gTTS
import uuid
import requests.exceptions

# Load environment variables
load_dotenv()
# Initialize DeepSeek client using OpenAI SDK
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

def generate_story(theme: str, length: str) -> str:
    try:
        # Map length to token count
        max_tokens = {
            "short": 500,
            "medium": 1000,
            "long": 1500
        }.get(length.lower(), 1000)
        
        # Create prompt
        prompt = f"Write a {length} story about {theme}. Make it interesting and engaging."
        
        # Generate text using DeepSeek API with OpenAI SDK
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            stream=False
        )
        
        story = response.choices[0].message.content.strip()
        return story
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        return "Error: Connection timeout or network error. Please try again."
    except ImportError as e:
        return f"Error: Missing required dependency - {str(e)}"
    except Exception as e:
        # Check for insufficient balance error (402)
        error_str = str(e)
        if "402" in error_str and "Insufficient Balance" in error_str:
            return "Error: Unable to generate story - The API account has insufficient balance. Please contact the administrator."
        return f"Error: Story generation failed - {str(e)}"

def text_to_speech(story_text: str) -> str:
    try:
        if not story_text.startswith("Error"):
            tts = gTTS(text=story_text, lang="en", timeout=30)
            filename = f"{uuid.uuid4().hex}.mp3"
            file_path = f"static/{filename}"
            tts.save(file_path)
            return file_path
        return "Error: Invalid story text"
    except requests.exceptions.RequestException:
        return "Error: Network error while converting text to speech"
    except Exception as e:
        return f"Error: Text-to-speech conversion failed - {str(e)}"