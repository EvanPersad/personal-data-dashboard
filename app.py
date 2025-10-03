import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Personal Data Dashboard")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of data:", df.head())

    # Example summary stats
    st.write("Summary Statistics:", df.describe())

    # Example chart
    numeric_cols = df.select_dtypes(include=['float64','int64']).columns
    if len(numeric_cols) > 0:
        st.write("Simple Line Chart:")
        st.line_chart(df[numeric_cols[0]])

    if len(numeric_cols) > 1:
    st.write("Scatter Plot:")
    fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
    st.plotly_chart(fig)
