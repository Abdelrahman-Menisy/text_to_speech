from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from gtts import gTTS
import io

app = FastAPI()

@app.post("/tts/")
async def text_to_speech(request: Request, text: str, lang: str):
    
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    if not lang:
        raise HTTPException(status_code=400, detail="Language code is required")

    # List of supported languages by gTTS
    supported_languages = ['ar', 'en', 'es', 'fr', 'de']  # Add more as needed

    if lang not in supported_languages:
        raise HTTPException(status_code=400, detail="Unsupported language code")

    # Generate speech
    tts = gTTS(text=text, lang=lang)
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)

    # Set the filename for the downloadable file
    filename = "output.mp3"

    return StreamingResponse(
        audio_file,
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# To run the server: uvicorn filename:app --reload
