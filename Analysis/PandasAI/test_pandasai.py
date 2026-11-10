
import os
from pathlib import Path

import pandas as pd
import pandasai as pai
from dotenv import load_dotenv
from pandasai_litellm.litellm import LiteLLM

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dataset" / "city_day.csv"

# Load API key
load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

# Load dataset using Pandas
data = pd.read_csv(DATA_PATH)

# Clean column names for PandasAI
data.columns = (
    data.columns
    .str.strip()
    .str.replace(r"[^A-Za-z0-9_]", "_", regex=True)
)

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)
print("Cleaned columns:", data.columns.tolist())

# Configure LLM
llm = LiteLLM(
   model="gemini/gemini-3.8-flash",
    api_key=api_key
)
# Create PandasAI DataFrame
# Register Gemini LLM globally with PandasAI
pai.config.set({
    "llm": llm
})

# Create PandasAI DataFrame
df = pai.DataFrame(data)

# Test natural-language query
question = "How many rows are present in this dataset?"

print("\nQuestion:", question)

answer = df.chat(question)

print("PandasAI Answer:", answer)
