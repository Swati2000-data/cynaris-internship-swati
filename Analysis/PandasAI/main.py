
import os
import logging
from pathlib import Path
import time

import pandas as pd
import pandasai as pai
from dotenv import load_dotenv
from pandasai_litellm.litellm import LiteLLM


# 1. Define project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dataset" / "city_day.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# 2. Configure error logging
logging.basicConfig(
    filename=OUTPUT_DIR / "error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)


# 3. Load Gemini API key
load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")


# 4. Load and prepare dataset
data = pd.read_csv(DATA_PATH)

# Clean column names for PandasAI
data.columns = (
    data.columns
    .str.strip()
    .str.replace(r"[^A-Za-z0-9_]", "_", regex=True)
)

# Convert Date column to datetime
data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

# Add year column for yearly analysis
data["Year"] = data["Date"].dt.year

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


# 5. Configure Gemini
llm = LiteLLM(
    model="gemini/gemini-3.8-flash",
    api_key=api_key
)

pai.config.set({"llm": llm})

# Create PandasAI DataFrame
ai_df = pai.DataFrame(data)


# 6. Define 10 natural-language queries
queries = [
    "How many records are present in this dataset?",
    "How many unique cities are present in this dataset?"
]


# 7. Execute queries with error handling
results = []

for number, query in enumerate(queries, start=1):

    print(f"\nQuery {number}: {query}")

    try:
        answer = ai_df.chat(query)

        print("Answer:", answer)

        results.append({
            "Query_Number": number,
            "Question": query,
            "Answer": str(answer),
            "Status": "Success"
        })

    except Exception as error:

        logging.exception(
            "Query %s failed: %s",
            number,
            query
        )

        print("Query failed:", error)

        results.append({
            "Query_Number": number,
            "Question": query,
            "Answer": "",
            "Status": "Failed"
        })

    # Wait before sending the next query
    if number < len(queries):
        print("Waiting 60 seconds before the next query...")
        time.sleep(60)
# 8. Save results
results_df = pd.DataFrame(results)

results_path = OUTPUT_DIR / "pandasai_results.csv"
results_df.to_csv(results_path, index=False)

print("\n--------------------------------")
print("PandasAI execution completed!")
print("Successful queries:", (results_df["Status"] == "Success").sum())
print("Failed queries:", (results_df["Status"] == "Failed").sum())
print("Results saved to:", results_path)
print("Error log:", OUTPUT_DIR / "error.log")
print("--------------------------------")
