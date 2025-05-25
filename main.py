from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from utils import get_suggestions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpellCheckRequest(BaseModel):
    text: str

class SuggestionItem(BaseModel):
    word: str
    suggestions: list[str]

class SpellCheckResponse(BaseModel):
    suggestions: List[SuggestionItem]

@app.post("/spellcheck", response_model=SpellCheckResponse)
def spell_check(req: SpellCheckRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    words = req.text.split()
    misspelled = []

    for word in words:
        stripped_word = word.strip()
        suggestions = get_suggestions(stripped_word)
        if suggestions:
            misspelled.append({
                "word": stripped_word,
                "suggestions": suggestions
            })

    return SpellCheckResponse(suggestions=misspelled)