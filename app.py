import io
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Personal Data Dashboard", layout="wide")

st.title("Personal Data Dashboard")

# ---------- File Upload ----------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

@st.cache_data(show_spinner=False)
def load_csv(file) -> pd.DataFrame:
    # Streamlit gives a file-like object; pandas can read it directly
    return pd.read_csv(file)

def safe_numeric_cols(df: pd.DataFrame):
    return df.select_dtypes(include=["float64", "int64", "float32", "int32"]).columns.tolist()

def safe_categorical_cols(df: pd.DataFrame):
    # Treat 'object' as categorical, also include categories that are strings in pandas >=2
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return cat_cols

def detect_date_cols(df: pd.DataFrame):
    # Try common date column names first; fallback to any column parseable as datetime
    common = [c for c in df.columns if c.lower() in {"date", "timestamp", "time", "day", "month"}]
    parsed_candidates = []
    for c in df.columns:
        try:
            _ = pd.to_datetime(df[c], errors="raise", infer_datetime_format=True)
            parsed_candidates.append(c)
        except Exception:
            pass
    # preserve order but unique
    out = []
    for c in common + parsed_candidates:
        if c not in out:
            out.append(c)
    return out

if not uploaded_file:
    st.info("Upload a CSV file to begin.")
    st.stop()

# ---------- Load & Preview ----------
try:
    df = load_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

if df.empty:
    st.warning("The uploaded file appears to be empty.")
    st.stop()

st.subheader("Data Preview")
st.dataframe(df.head(), use_container_width=True)

# ---------- Column Detection ----------
numeric_cols = safe_numeric_cols(df)
cat_cols = safe_categorical_cols(df)
date_cols = detect_date_cols(df)

# ---------- Sidebar Controls ----------
st.sidebar.header("Controls")

# Numeric column for main visuals
col_choice = st.sidebar.selectbox("Numeric column", numeric_cols, index=0 if numeric_cols else None)

# Category column for pie chart
pie_cat = None
if cat_cols:
    pie_cat = st.sidebar.selectbox("Category column (for pie)", cat_cols)

# Date/time configuration
date_col = None
if date_cols:
    date_col = st.sidebar.selectbox("Date column (optional)", ["(None)"] + date_cols)
    if date_col == "(None)":
        date_col = None

freq = None
if date_col:
    freq = st.sidebar.selectbox("Time aggregation", ["D - Daily", "W - Weekly", "M - Monthly", "Q - Quarterly", "Y - Yearly"], index=2)

# Correlation heatmap toggle
show_corr = st.sidebar.checkbox("Show correlation heatmap", value=False)

# ---------- Summary Statistics ----------
st.subheader("Summary Statistics")
try:
    desc = df.describe(include="all").transpose()
    st.dataframe(desc, use_container_width=True)
    # Download summary as CSV
    csv_buf = io.StringIO()
    desc.to_csv(csv_buf)
    st.download_button("Download summary (CSV)", data=csv_buf.getvalue(), file_name="summary_stats.csv", mime="text/csv")
except Exception as e:
    st.warning(f"Could not compute summary statistics: {e}")

# ---------- Visualizations ----------
if not col_choice:
    st.warning("No numeric columns detected. Please upload a CSV with at least one numeric column.")
    st.stop()

left, right = st.columns(2)

with left:
    st.subheader(f"Histogram: {col_choice}")
    try:
        fig_hist = px.histogram(df, x=col_choice, nbins=20, title=f"Distribution of {col_choice}")
        st.plotly_chart(fig_hist, use_container_width=True)
    except Exception as e:
        st.warning(f"Histogram error: {e}")

with right:
    st.subheader(f"Line Chart: {col_choice}")
    try:
        # If a date column is selected, attempt a time series view
        if date_col:
            dfx = df[[date_col, col_choice]].dropna()
            dfx[date_col] = pd.to_datetime(dfx[date_col], errors="coerce")
            dfx = dfx.dropna(subset=[date_col])

            if not dfx.empty:
                # Resample/aggregate
                code = freq.split(" - ")[0]  # e.g., "M"
                ts = dfx.set_index(date_col).resample(code).mean(numeric_only=True).reset_index()
                fig_line = px.line(ts, x=date_col, y=col_choice, title=f"{col_choice} over time ({code})")
            else:
                # fallback to index-based line
                fig_line = px.line(df, y=col_choice, title=f"{col_choice} over rows")
        else:
            fig_line = px.line(df, y=col_choice, title=f"{col_choice} over rows")

        st.plotly_chart(fig_line, use_container_width=True)
    except Exception as e:
        st.warning(f"Line chart error: {e}")

# Pie chart (requires category + numeric)
if pie_cat:
    st.subheader(f"Pie Chart: {pie_cat} vs {col_choice}")
    try:
        # If the data has multiple rows per category, aggregate the numeric column
        pie_df = df[[pie_cat, col_choice]].dropna()
        pie_df = pie_df.groupby(pie_cat, as_index=False)[col_choice].sum()
        if len(pie_df) > 30:
            st.caption("Note: Large number of categories detected; consider filtering or grouping.")
        fig_pie = px.pie(pie_df, names=pie_cat, values=col_choice, title=f"{pie_cat} share of {col_choice}")
        st.plotly_chart(fig_pie, use_container_width=True)
    except Exception as e:
        st.warning(f"Pie chart error: {e}")

# Correlation heatmap
if show_corr:
    st.subheader("Correlation Heatmap (numeric columns)")
    try:
        if len(numeric_cols) < 2:
            st.caption("Need at least two numeric columns for a correlation heatmap.")
        else:
            corr = df[numeric_cols].corr(numeric_only=True)
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
            st.plotly_chart(fig_corr, use_container_width=True)
    except Exception as e:
        st.warning(f"Correlation heatmap error: {e}")
