import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("📊 Personal Data Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Read and preview data
    df = pd.read_csv(uploaded_file)
    st.write("### 🔍 Data Preview")
    st.dataframe(df.head())

    # Summary statistics
    st.write("### 📈 Summary Statistics")
    st.write(df.describe())

    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    # --- SIDEBAR CONTROLS ---
    st.sidebar.header("⚙️ Chart Controls")

    col_choice = None
    pie_col = None

    # Numeric column dropdown (main numeric selector)
    if numeric_cols:
        col_choice = st.sidebar.selectbox("Select a numeric column:", numeric_cols)

    # Category column dropdown (for pie chart)
    if cat_cols:
        pie_col = st.sidebar.selectbox("Select category column for pie chart:", cat_cols)

    # --- MAIN CONTENT VISUALS ---
    if col_choice:
        st.write(f"### 📊 Visualizations for `{col_choice}`")

        # Line Chart
        st.subheader("Line Chart")
        st.line_chart(df[col_choice])

        # Histogram / Bar Chart
        st.subheader("Histogram")
        fig_bar = px.histogram(df, x=col_choice, nbins=10, title=f"Distribution of {col_choice}")
        st.plotly_chart(fig_bar)

    # Pie Chart (if both category and numeric columns exist)
    if pie_col and col_choice:
        st.subheader("Pie Chart")
        fig_pie = px.pie(df, names=pie_col, values=col_choice, title=f"{pie_col} vs {col_choice}")
        st.plotly_chart(fig_pie)

else:
    st.info("👆 Upload a CSV file to begin analyzing your data.")
