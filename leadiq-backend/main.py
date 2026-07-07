from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import *
from scraper import *
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

class LoadRequest(BaseModel):
    url: str

class AskRequest(BaseModel):
    session_id: str
    question: str

@app.post("/load")
def load(request: LoadRequest):
    text = scrape_url(request.url)
    chunks = split_character(text)
    vectorstore = create_vectorstore(chunks)
    session_id = str(uuid.uuid4())
    sessions[session_id] = vectorstore
    return {"session_id": session_id, "message": "Company loaded successfully"}

@app.post("/ask")
def ask(request: AskRequest):
    vectorstore = sessions.get(request.session_id)
    if not vectorstore:
        return {"error": "Session not found. Please load a URL first."}
    answer = answer_question(vectorstore, request.question)
    return {"answer": answer}