from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def split_character(text):
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    chunks=splitter.split_text(text)
    return chunks

def create_vectorstore(chunks):
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore=FAISS.from_texts(chunks,embeddings)
    return vectorstore

def answer_question(vectorstore, question, history=[]):
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant")
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])
    
    history_text = ""
    for msg in history:
        history_text += f"User: {msg['question']}\nAssistant: {msg['answer']}\n\n"
    
    prompt = f"""Answer the question based on the context below.
    
    Context: {context}

    Previous conversation:
    {history_text}

    Current question: {question}"""
    
    response = llm.invoke(prompt)
    return response.content