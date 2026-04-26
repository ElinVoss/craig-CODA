"""
Craig-CODA server — ChatKit session endpoint + future graph-native runtime.
Run: uvicorn server:app --reload --port 8000
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Craig-CODA", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.post("/api/chatkit/session")
def create_chatkit_session():
    try:
        session = _openai.chatkit.sessions.create(
            model="gpt-4o",
            instructions=(
                "You are Craig-CODA, a graph-native AI assistant. "
                "You reason transparently, surface contradictions, and "
                "cite sources when possible."
            ),
        )
        return {"client_secret": session.client_secret}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
