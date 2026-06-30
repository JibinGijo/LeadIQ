from fastapi import FastAPI
from pydantic import BaseModel
from rag import *
from scraper import *

app = FastAPI()

class LeadRequest(BaseModel):
    url: str
    question: str

@app.post("/analyze")
def analyze(request: LeadRequest):
    text = scrape_url(request.url)
    chunks = split_character(text)
    vectorstore = create_vectorstore(chunks)
    answer = answer_question(vectorstore, request.question)
    return {"answer": answer}