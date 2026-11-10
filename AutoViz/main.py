
import os
import html
import pandas as pd
import sweetviz as sv

from pathlib import Path
from autoviz.AutoViz_Class import AutoViz_Class

# -----------------------------------
# 1. Define project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "hotel_bookings.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
AUTOVIZ_DIR = OUTPUT_DIR / "autoviz"

OUTPUT_DIR.mkdir(exist_ok=True)
AUTOVIZ_DIR.mkdir(exist_ok=True)

# -----------------------------------
# 2. Load dataset
# -----------------------------------

print("Loading hotel booking dataset...")

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")
print("Dataset shape:", df.shape)
print("Total missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

# -----------------------------------
# 3. Run AutoViz
# -----------------------------------

print("\nGenerating AutoViz report...")

AV = AutoViz_Class()

AV.AutoViz(
    filename="",
    sep=",",
    depVar="",
    dfte=df,
    header=0,
    verbose=1,
    lowess=False,
    chart_format="html",
    max_rows_analyzed=150000,
    max_cols_analyzed=32,
    save_plot_dir=str(AUTOVIZ_DIR)
)

print("AutoViz analysis completed!")

# Create an HTML index for generated charts
html_files = sorted(AUTOVIZ_DIR.glob("*.html"))

index_content = """
<html>
<head>
<title>AutoViz Report Index</title>
</head>
<body>
<h1>Hotel Booking - AutoViz Report</h1>
<h2>Generated visualizations</h2>
<ul>
"""

for file in html_files:
    index_content += (
        f'<li><a href="autoviz/{html.escape(file.name)}">'
        f'{html.escape(file.name)}</a></li>'
    )

index_content += """
</ul>
</body>
</html>
"""

index_path = OUTPUT_DIR / "autoviz_index.html"
index_path.write_text(index_content, encoding="utf-8")

print("AutoViz HTML index saved:", index_path)

# -----------------------------------
# 4. Run SweetViz
# -----------------------------------

print("\nGenerating SweetViz report...")

report = sv.analyze(df)

sweetviz_path = OUTPUT_DIR / "sweetviz_report.html"

report.show_html(
    filepath=str(sweetviz_path),
    open_browser=False
)

print("SweetViz report saved:", sweetviz_path)

# -----------------------------------
# 5. Identify three business insights
# -----------------------------------

print("\n========== BUSINESS INSIGHTS ==========")

# Insight 1: Cancellation rate by hotel
cancellation = (
    df.groupby("hotel")["is_canceled"].mean() * 100
)

print("\n1. Cancellation rate by hotel:")
print(cancellation.round(2))

# Insight 2: Average daily rate by hotel
adr = df.groupby("hotel")["adr"].mean()

print("\n2. Average Daily Rate by hotel:")
print(adr.round(2))

# Insight 3: Most popular arrival month
monthly_bookings = df["arrival_date_month"].value_counts()

print("\n3. Most popular arrival month:")
print(monthly_bookings.head(1))

print("\nAll tasks completed!")
