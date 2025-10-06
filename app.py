import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Personal Data Dashboard")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 🔍 Data Preview")
    st.dataframe(df.head())

    # Summary Statistics
    st.write("### 📈 Summary Statistics")
    st.write(df.describe())

    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Dropdowns for user selection
    if numeric_cols:
        st.write("### 📊 Choose a Column to Visualize")
        col_choice = st.sidebar.selectbox("Select a numeric column:", numeric_cols)


        # Line Chart
        st.write("#### Line Chart")
        st.line_chart(df[col_choice])

        # Histogram / Bar Chart
        st.write("#### Histogram")
        fig_bar = px.histogram(df, x=col_choice, nbins=10, title=f"Distribution of {col_choice}")
        st.plotly_chart(fig_bar)

    # Pie Chart (only if you have at least 1 categorical + 1 numeric column)
    if cat_cols and numeric_cols:
        st.write("#### Pie Chart")
        pie_col = st.sidebar.selectbox("Select a numeric column:", numeric_cols)
        fig_pie = px.pie(df, names=pie_col, values=col_choice, title=f"{pie_col} vs {col_choice}")
        st.plotly_chart(fig_pie)
