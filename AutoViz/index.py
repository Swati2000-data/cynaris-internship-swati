
from pathlib import Path
import html

OUTPUT_DIR = Path("outputs")

html_files = [
    file for file in OUTPUT_DIR.rglob("*.html")
    if file.name not in ("autoviz_index.html", "sweetviz_report.html")
]

print("AutoViz HTML files found:", len(html_files))

content = """
<html>
<head>
    <title>AutoViz Report</title>
</head>
<body>
    <h1>Hotel Booking - AutoViz Report</h1>
    <h2>Generated Visualizations</h2>
    <ul>
"""

for file in html_files:
    relative_path = file.relative_to(OUTPUT_DIR).as_posix()
    content += (
        f'<li><a href="{html.escape(relative_path)}">'
        f'{html.escape(file.name)}</a></li>\n'
    )

content += """
    </ul>
</body>
</html>
"""

index_path = OUTPUT_DIR / "autoviz_index.html"
index_path.write_text(content, encoding="utf-8")

print("Index generated successfully:", index_path.resolve())
