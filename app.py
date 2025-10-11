import streamlit as st
import assignment2
import pandas as pd
import datetime

SAMPLE_RATIO = st.number_input("Sample Ratio", value = 1e6)
START_DATE = st.date_input("Start Date", datetime.date(2021, 4, 1))
END_DATE = st.date_input("End Date", datetime.date(2022, 4, 30))
countries_df = pd.read_csv("a2-countries.csv")
SELECTED_COUNTRIES = st.multiselect(
    "Select Countries",
    list(countries_df["country"]),
    default=[]
)
if st.button("RUN"):
    st.write(f"Running with the following settings: Sample Ratio: {SAMPLE_RATIO} Start Date: {START_DATE} End Date: {END_DATE} Countries: {SELECTED_COUNTRIES}")
    assignment2.run(countries_csv_name="a2-countries.csv", countries=SELECTED_COUNTRIES, start_date=START_DATE, end_date=END_DATE, sample_ratio=SAMPLE_RATIO)
    st.image("a2-covid-simulation.png")