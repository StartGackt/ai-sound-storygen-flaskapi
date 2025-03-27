from fastapi import APIRouter
from pydantic import BaseModel
from services.story_service import generate_story, text_to_speech

router = APIRouter()

class StoryRequest(BaseModel):
    theme: str
    length: str

@router.post("/generate_story")
async def create_story(request: StoryRequest):
    story = generate_story(request.theme, request.length)
    audio_path = text_to_speech(story)
    return {"story": story, "audio_url": f"http://localhost:8000/{audio_path}"}
