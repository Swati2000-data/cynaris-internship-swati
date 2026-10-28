# Power BI Fundamentals — Week 3 Day 1

## Dataset
Online Retail transactional dataset (invoice line items), covering 1 Dec 2010 to 9 Dec 2011.
The uploaded source had 541,909 rows and 8 columns.

## Prepared file
`online_retail_cleaned.csv` is prepared for positive-sales analysis:
- Excludes cancellation invoices (invoice numbers beginning with `C`).
- Excludes rows with quantity <= 0 or unit price <= 0.
- Parses invoice dates and exports them in ISO date-time format.
- Fills missing product descriptions with `Unknown product description`.
- Preserves unknown CustomerID as blank rather than inventing customer identities.
- Adds `Revenue = Quantity * UnitPrice`.

This is an analysis-ready view for positive sales, not a replacement for a returns/cancellations analysis. The source includes cancellations/negative transactions; if your assignment needs return analysis, use the original dataset separately.

## Import into Power BI Desktop
1. Home → Get data → Text/CSV.
2. Select `online_retail_cleaned.csv`.
3. In the preview, choose Transform Data if you need to verify data types; otherwise Load.
4. Set `InvoiceDate` to Date/Time, `Quantity` to Whole number, `UnitPrice` and `Revenue` to Decimal number, and IDs/codes to Text.
5. Save the report as `powerbi_fundamentals_week3_day1.pbix`.

## Suggested three-page report

### Page 1 — Sales Overview
KPI cards: Total Sales, Total Orders, Units Sold, Unique Customers.
Visuals:
- Line chart: Revenue by month.
- Bar chart: Sales by country (Top 10).
- Bar chart: Sales by product description (Top 10).
Slicers: Invoice Date, Country (use as Region because dataset has Country, not Region), and product category is not present in this dataset. Use Description or StockCode as a product filter, and note the dataset has no product-category field.

### Page 2 — Drill-down
Create a hierarchy using Country → InvoiceNo → StockCode (this is a navigation hierarchy, not a business product category hierarchy).
Visuals:
- Bar chart: Sales by Country.
- Matrix: Country > InvoiceNo > Description, with Total Sales and Units Sold.
Enable drill-down on the hierarchy chart and use drill-through to a detail page if desired.

### Page 3 — KPI Summary
Cards: Total Sales, Average Order Value, Average Selling Price, Products Sold, Countries Served.
Visuals:
- Monthly sales trend.
- Sales by country table.
- Sales and units by product.
Use conditional formatting sparingly to highlight high/low values.

## Slicers and field mapping
- Date slicer → InvoiceDate (or date-only column if using a calendar table).
- Region slicer → Country (the dataset does not contain a Region column).
- Category slicer → Description or StockCode as a substitute. The dataset does not contain a product Category field; do not label this as a true category unless you create a documented category mapping.

## DAX
Use `DAX_measures.txt` for starter measures. Create measures individually via Modeling → New measure. The optional Calendar table and date-only column notes are included in that file. If creating a Calendar table, relate Calendar[Date] to the date-only column, not the date-time field.

## Publish and share
1. Save the PBIX.
2. In Power BI Desktop, Home → Publish, and choose a workspace available to your account.
3. Open https://app.powerbi.com and confirm the report appears in that workspace.
4. Use Share only if your license and organization settings permit it. A normal Power BI Service link is not automatically public and recipients may need permissions/licensing.
5. If sharing is blocked, use the PBIX and screenshots in GitHub and ask your mentor whether that is acceptable. Do not use Publish to web for private or internship-confidential data.

## GitHub
Suggested deliverables:
- `powerbi_fundamentals_week3_day1.pbix`
- `online_retail_cleaned.csv` (only if repository size/licensing rules permit)
- screenshots of each report page
- this README and `DAX_measures.txt`

Commit message:
`feat: powerbi-fundamentals week-3-day-1 complete`
