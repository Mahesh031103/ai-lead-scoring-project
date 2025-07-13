import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib

# Create synthetic dataset
np.random.seed(42)
n = 10000

age_groups = ["18-25", "26-35", "36-50", "51+"]
family_backgrounds = ["Single", "Married", "Divorced"]

data = pd.DataFrame({
    "phone_number": ["+91" + str(9000000000 + i) for i in range(n)],
    "email": [f"user{i}@test.com" for i in range(n)],
    "credit_score": np.random.randint(300, 851, size=n),
    "age_group": np.random.choice(age_groups, size=n),
    "family_background": np.random.choice(family_backgrounds, size=n),
    "income": np.random.randint(100000, 1000000, size=n),
})

data["high_intent"] = ((data["credit_score"] > 650) & (data["income"] > 500000)).astype(int)

X = data[["credit_score", "income", "age_group", "family_background"]]
y = data["high_intent"]

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_cat = encoder.fit_transform(X[["age_group", "family_background"]])
X_num = X[["credit_score", "income"]].values
X_final = np.hstack([X_num, X_cat])

X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

model = GradientBoostingClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "lead_scoring_model.pkl")
joblib.dump(encoder, "encoder.pkl")

print("Model and encoder saved successfully.")

