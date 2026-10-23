import ast
import json
from pathlib import Path

import pandas as pd

CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1wdNo9snBePx0XzwdndhOKxUpBL4Z7DkK55gIjuIzsU0/export?format=csv"
)

OUTPUT = Path("experiments/robots.json")

df = pd.read_csv(CSV_URL)

robots = []

for _, row in df.iterrows():
    robots.append(
        {
            "name": row["Name"],
            "timestamp": row["Timestamp"],
            "robot": ast.literal_eval(row["Robot"]),
        }
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w") as f:
    json.dump(
        {
            "downloaded_at": pd.Timestamp.now().isoformat(),
            "robots": robots,
        },
        f,
        indent=2,
    )

print(f"Saved {len(robots)} robots.")
