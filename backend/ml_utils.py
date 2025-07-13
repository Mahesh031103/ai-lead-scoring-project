import joblib
import numpy as np
import pandas as pd

model = joblib.load("lead_scoring_model.pkl")
encoder = joblib.load("encoder.pkl")

def compute_initial_score(lead_data: dict) -> float:
    data = pd.DataFrame([{ 
        "credit_score": lead_data["credit_score"],
        "income": lead_data["income"],
        "age_group": lead_data["age_group"],
        "family_background": lead_data["family_background"],
    }])

    cat_encoded = encoder.transform(data[["age_group", "family_background"]])
    X_num = data[["credit_score", "income"]].values
    X_final = np.hstack([X_num, cat_encoded])

    prob = model.predict_proba(X_final)[0][1]
    return round(prob * 100, 2)

def apply_reranker(initial_score: float, comments: str) -> float:
    score = initial_score
    comments_lower = comments.lower() if comments else ""

    if "urgent" in comments_lower:
        score += 10
    if "not interested" in comments_lower:
        score -= 10

    score = max(0, min(100, score))
    return round(score, 2)
