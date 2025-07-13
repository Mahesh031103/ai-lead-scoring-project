from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import LeadInput, ScoreOutput
from ml_utils import compute_initial_score, apply_reranker
from mangum import Mangum # type: ignore

app = FastAPI(title="AI Lead Scoring Engine", version="1.0")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

leads_db = {}

@app.post("/score", response_model=ScoreOutput)
def score_lead(lead: LeadInput):
    initial_score = compute_initial_score(lead.dict())
    reranked_score = apply_reranker(initial_score, lead.comments)
    leads_db[lead.email] = {
        "phone_number": lead.phone_number,
        "initial_score": initial_score,
        "reranked_score": reranked_score,
        "comments": lead.comments,
    }
    return ScoreOutput(initial_score=initial_score, reranked_score=reranked_score)

print("FastAPI server ready.")

handler = Mangum(app)