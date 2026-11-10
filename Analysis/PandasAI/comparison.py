import os
import time
import logging
from pathlib import Path

import pandas as pd
import pandasai as pai
from dotenv import load_dotenv
from pandasai_litellm.litellm import LiteLLM


# 1. Define project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dataset" / "city_day.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# 2. Configure logging
logging.basicConfig(
    filename=OUTPUT_DIR / "comparison_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

# 3. Load Gemini API key
load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing.")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

# 4. Load dataset
data = pd.read_csv(DATA_PATH)

data.columns = (
    data.columns.str.strip()
    .str.replace(r"[^A-Za-z0-9_]", "_", regex=True)
)

# 5. Calculate manual Pandas answers
manual_answers = {
    "Total records": len(data),

    "Overall average AQI": round(
        data["AQI"].mean(), 2
    ),

    "Most frequent AQI category": (
        data["AQI_Bucket"].mode(dropna=True).iloc[0]
    )
}

# 6. Configure PandasAI
llm = LiteLLM(
    model="gemini/gemini-3.8-flash",
    api_key=api_key
)

pai.config.set({"llm": llm})

ai_df = pai.DataFrame(data)

# 7. Define the same three questions
comparison_queries = [
    {
        "question": "How many records are present in this dataset?",
        "manual_answer": manual_answers["Total records"]
    },
    {
        "question": "What is the overall average AQI, excluding missing values?",
        "manual_answer": manual_answers["Overall average AQI"]
    },
    {
        "question": "Which AQI_Bucket category occurs most frequently, excluding missing values?",
        "manual_answer": manual_answers["Most frequent AQI category"]
    }
]

# 8. Execute and compare
comparison_results = []

for number, item in enumerate(comparison_queries, start=1):

    question = item["question"]
    manual_answer = item["manual_answer"]

    print(f"\nComparison {number}: {question}")
    print("Manual Pandas answer:", manual_answer)

    try:
        ai_answer = ai_df.chat(question)

        print("PandasAI answer:", ai_answer)

        comparison_results.append({
            "Question": question,
            "PandasAI_Answer": str(ai_answer),
            "Manual_Pandas_Answer": str(manual_answer),
            "Status": "Success"
        })

    except Exception as error:

        logging.exception(
            "Comparison query %s failed: %s",
            number,
            question
        )

        print("PandasAI query failed:", error)

        comparison_results.append({
            "Question": question,
            "PandasAI_Answer": "",
            "Manual_Pandas_Answer": str(manual_answer),
            "Status": "Failed"
        })

    if number < len(comparison_queries):
        print("Waiting 60 seconds before next comparison...")
        time.sleep(60)

# 9. Save comparison results
comparison_df = pd.DataFrame(comparison_results)

comparison_path = OUTPUT_DIR / "comparison_results.csv"

comparison_df.to_csv(comparison_path, index=False)

print("\n--------------------------------")
print("Comparison completed!")
print("Successful:", (comparison_df["Status"] == "Success").sum())
print("Failed:", (comparison_df["Status"] == "Failed").sum())
print("Saved to:", comparison_path)
print("--------------------------------")