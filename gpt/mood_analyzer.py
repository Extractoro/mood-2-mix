import json
import os
import re

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def analyze_mood(prompt: str) -> dict:
    try:
        if not prompt:
            raise HTTPException(status_code=500, detail="Empty prompt")

        system_msg = (
            "You are a music-oriented emotion analyst. The user provides a free-form emotional"
            "description (in any tone or length).\n"
            "Your task is to extract and return **only** a strict JSON object "
            "with the following fields:\n"
            "- mood: a one-word description of the emotional state"
            "(e.g., 'happy', 'frustrated', 'melancholic')\n"
            "- valence: a float between 0.0 and 1.0 representing emotional positivity"
            "(0 = negative, 1 = positive)\n"
            "- energy: a float between 0.0 and 1.0 representing arousal or activity level"
            "(0 = calm, 1 = energetic)\n"
            "- genres: a list of 2–4 music genres that fit the emotion and could "
            "help express or regulate it "
            "(e.g., ['lofi', 'indie', 'pop'])\n"
            "- query: a concise text search query that reflects the emotional state and"
            "could be used to search for "
            "matching songs (e.g., 'uplifting indie pop', 'calm piano', 'aggressive rock')\n"
            "The query should be based on the mood and suitable for use in"
            "YouTube Music or Spotify search.\n"
            "Respond with valid JSON **only**."
            "No preamble, explanation, or formatting — just raw JSON."
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        )

        raw_content = response.choices[0].message.content
        cleaned = re.sub(r"```json|```", "", raw_content).strip()
        parsed_data = json.loads(cleaned)

        return parsed_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON returned by GPT")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"analyze_mood error: {str(e)}")
