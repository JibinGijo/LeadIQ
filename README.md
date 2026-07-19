# LeadIQ

AI-powered sales intelligence tool. Enter any company URL and ask questions about it — LeadIQ scrapes the website, builds a knowledge base, and lets you have a full conversation about the company.

## What it does
- Scrapes any company website in real time
- Builds a RAG pipeline over the scraped content
- Lets sales reps ask natural language questions about the company
- Maintains full conversation context across multiple questions
- Session persists on refresh, resets on tab close

## How it works
1. User enters a company URL
2. Backend scrapes the page using BeautifulSoup
3. Text is split into chunks and stored in a FAISS vector database
4. User asks a question — relevant chunks are retrieved
5. Chunks + conversation history sent to Groq LLM (Llama 3.1)
6. LLM answers based on actual website content

## Tech Stack
### Backend
- Python, FastAPI, LangChain
- FAISS (vector database)
- HuggingFace Embeddings (all-MiniLM-L6-v2)
- Groq API (Llama 3.1)
- BeautifulSoup (web scraping)

### Frontend
- React + TypeScript (Vite)
- sessionStorage for session persistence

## How to run locally

### Backend
1. `cd leadiq-backend`
2. `pip install -r requirements.txt`
3. Create `.env` with `GROQ_API_KEY=your_key`
4. `python -m uvicorn main:app --reload`

### Frontend
1. `cd leadiq-frontend`
2. `npm install`
3. `npm run dev`
4. Open `http://localhost:5173`