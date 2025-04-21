from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import get_suggestions

app = FastAPI()

class SpellCheckRequest(BaseModel):
    word: str

class SpellCheckResponse(BaseModel):
    suggestions: list[str]

@app.post("/spellcheck", response_model=SpellCheckResponse)
def spell_check(req: SpellCheckRequest):
    if not req.word.strip():
        raise HTTPException(status_code=400, detail="Word cannot be empty.")
    
    suggestions = get_suggestions(req.word.strip())
    return SpellCheckResponse(suggestions=suggestions)