from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from utils import get_suggestions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpellCheckSingleRequest(BaseModel):
    word: str
    max_distance: int = 2
    max_results: int = 5

@app.post("/spellcheck")
def check_spelling(request: SpellCheckSingleRequest) -> Dict[str, List[str]]:
    suggestions = get_suggestions(
        request.word,
        max_distance=request.max_distance,
        max_results=request.max_results
    )
    return {request.word: suggestions}


class SpellCheckRequest(BaseModel):
    text: str
    max_distance: int = 2
    max_results: int = 5

@app.post("/spellcheck_bulk")
def bulk_spellcheck(request: SpellCheckRequest) -> Dict[str, List[str]]:
    words = request.text.strip().split()
    seen = set()
    result = {}

    for word in words:
        if word in seen:
            continue
        seen.add(word)
        suggestions = get_suggestions(word, max_distance=request.max_distance, max_results=request.max_results)
        if suggestions:
            result[word] = suggestions

    return result
