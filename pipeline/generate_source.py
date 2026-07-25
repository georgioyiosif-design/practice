import pandas as pd
from faker import Faker
import random
from pathlib import Path

# Το Faker φτιάχνει ψεύτικα αλλά ρεαλιστικά δεδομένα
fake = Faker()
random.seed(42)  # ώστε τα δεδομένα να είναι ίδια κάθε φορά

rows = []
for i in range(1000):
    rows.append({
        "order_id":    i + 1,
        "customer_id": random.randint(1, 100),
        "customer_name": fake.name(),
        "product":     random.choice(["Laptop", "Mouse", "Monitor", "Keyboard", "Headset"]),
        "quantity":    random.randint(1, 10),
        "unit_price":  round(random.uniform(10, 1500), 2),
        "order_date":  fake.date_between(start_date="-1y", end_date="today"),
        "status":      random.choice(["completed", "pending", "cancelled", None]),  # εσκεμμένα NULL
        "country":     random.choice(["GR", "DE", "IT", "FR", None]),  # εσκεμμένα NULL
    })

df = pd.DataFrame(rows)

# Αποθήκευση στον φάκελο source — αυτό είναι η «πηγή μας»
Path("data/source").mkdir(parents=True, exist_ok=True)
df.to_csv("data/source/orders.csv", index=False)

print(f"✅ Δημιουργήθηκαν {len(df)} εγγραφές")
print(df.head())
print(f"\nNull τιμές:\n{df.isnull().sum()}")