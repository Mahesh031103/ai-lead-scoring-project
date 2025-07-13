import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def generate_lead_data(num_rows=10000):
    data = []

    age_groups = ["18-25", "26-35", "36-50", "51+"]
    family_status = ["Single", "Married", "Divorced"]

    for _ in range(num_rows):
        phone = fake.phone_number()
        email = fake.email()
        credit_score = np.random.randint(300, 851)
        age_group = random.choice(age_groups)
        family = random.choice(family_status)
        income = np.random.randint(100000, 1000001)

        # Simple rule for intent: high income + high credit = higher chance
        intent = 1 if credit_score > 650 and income > 500000 else 0

        row = {
            "Phone Number": phone,
            "Email": email,
            "Credit Score": credit_score,
            "Age Group": age_group,
            "Family Background": family,
            "Income": income,
            "Lead Intent": intent
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_lead_data(10000)
    df.to_csv("../data/synthetic_leads.csv", index=False)
    print("Synthetic dataset saved as synthetic_leads.csv in /data folder.")
