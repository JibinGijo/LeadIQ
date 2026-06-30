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

def answer_question(vectorstore,question):
    llm=ChatGroq(api_key=os.getenv("GROQ_API_KEY"),model_name="llama-3.1-8b-instant")
    retriever=vectorstore.as_retriever()
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"Answer the question based on the context below.\n\nContext: {context}\n\nQuestion: {question}"
    response = llm.invoke(prompt)
    return response.content
