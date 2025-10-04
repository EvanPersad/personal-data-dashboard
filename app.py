import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Personal Data Dashboard")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file: #if a file is uploaded
    df = pd.read_csv(uploaded_file) #dataframe is set to be the csv file being read by panda
    st.write("Preview of data:", df.head()) #Sanity check for user to see if file loaded correctly

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

    # Identify categorical (non-numeric) columns
    cat_cols = df.select_dtypes(include=['object']).columns

    if len(cat_cols) > 0 and len(numeric_cols) > 0:
        st.write("Pie Chart:")

    # Use first categorical column + first numeric column
        fig = px.pie(df, names=cat_cols[0], values=numeric_cols[0], title="Distribution")
        st.plotly_chart(fig)
