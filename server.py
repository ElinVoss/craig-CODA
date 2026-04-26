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

CHATKIT_WORKFLOW_ID = "wf_69ed7b947a5c8190b01872f8eec1f6e40f834c1a4ab142ae"
CHATKIT_WORKFLOW_VERSION = "1"


@app.post("/api/chatkit/session")
def create_chatkit_session():
    try:
        session = _openai.chatkit.sessions.create(
            workflow_id=CHATKIT_WORKFLOW_ID,
            workflow_version=CHATKIT_WORKFLOW_VERSION,
        )
        return {"client_secret": session.client_secret}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
