"""
Craig-CODA server — ChatKit session endpoint + future graph-native runtime.
Run: uvicorn server:app --reload --port 8000
"""
import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Craig-CODA", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CHATKIT_WORKFLOW_ID = "wf_69ed7b947a5c8190b01872f8eec1f6e40f834c1a4ab142ae"


@app.post("/api/chatkit/session")
def create_chatkit_session():
    key = os.environ["OPENAI_API_KEY"]
    resp = httpx.post(
        "https://api.openai.com/v1/chatkit/sessions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "chatkit_beta=v1",
        },
        json={
            "workflow": {
                "id": CHATKIT_WORKFLOW_ID,
            },
            "user": "default-user",
        },
        timeout=10,
    )
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return {"client_secret": resp.json()["client_secret"]}


@app.get("/health")
def health():
    return {"status": "ok"}
