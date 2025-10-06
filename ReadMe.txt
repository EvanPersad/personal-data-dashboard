Personal Data Dashboard for data analytics focus and practice.

A lightweight Streamlit app for quick and interactive exploration of CSV data.

Features:
- Upload a CSV and preview the first rows
- Summary statistics and downloadable summary CSV
- Choose columns in the sidebar to create:
  - Histogram
  - Line chart (with optional time aggregation if a date column exists)
  - Pie chart (category vs numeric)
- Optional correlation heatmap

To Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

I plan to deploy and this will be my first deployment ever so enjoy and thank you!