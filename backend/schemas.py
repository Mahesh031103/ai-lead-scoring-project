from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class LeadInput(BaseModel):
    phone_number: constr(regex=r'^\+?[0-9\- ]{10,20}$') # type: ignore
    email: EmailStr
    credit_score: int
    age_group: str
    family_background: str
    income: int
    comments: Optional[str] = ""

    class Config:
        schema_extra = {
            "example": {
                "phone_number": "+91-9876543210",
                "email": "john.doe@test.com",
                "credit_score": 720,
                "age_group": "26-35",
                "family_background": "Single",
                "income": 600000,
                "comments": "urgent callback"
            }
        }

class ScoreOutput(BaseModel):
    initial_score: float
    reranked_score: float
