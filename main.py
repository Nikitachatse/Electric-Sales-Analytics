# Importing the libraries
import pandas as pd
import numpy as np
import preprocessor
import streamlit as st

# changing the layout of streamlit
st.set_page_config(layout="wide")

df = pd.read_csv("data.csv")

# Creating the date features
df = preprocessor.fetch_time_features(df)
# sidebar
st.sidebar.title("Filters")
# year filter
years = preprocessor.multiselect("Select Year", df["Financial_Year"].unique().tolist())
# Retailer filter
retailers = preprocessor.multiselect("Select Retailer", df["Retailer"].unique().tolist())
# Company filter
companies = preprocessor.multiselect("Select Companies", df["Company"].unique().tolist())
# Month filter
months = preprocessor.multiselect("Select Month", df["Financial_Month"].unique().tolist())

# Global filtering
filtered_df = df[(df["Financial_Year"].isin(years)) & (df["Retailer"].isin(retailers)) & (df["Company"].isin(companies)) & (df["Financial_Month"].isin(months))]


# Main dashboard
st.title("Sales Analytics Dashbord")

# Creating columns and key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label = "Total sales", value = int(filtered_df["Amount"].sum()))
with col2:
    st.metric(label = "Total margin", value = int(filtered_df["Margin"].sum()))
with col3:
    st.metric(label = "Total transactions", value = len(filtered_df["Margin"]))
with col4:
    st.metric(label = "Margin percentage (in %)", value = int(filtered_df["Margin"].sum()*100/filtered_df["Amount"].sum()))

# yearly sales month on month basis
yearly_sales = filtered_df[["Financial_Year","Financial_Month","Amount"]].groupby(["Financial_Year","Financial_Month"]).sum().reset_index()
pivoted_yearly_sales = yearly_sales.pivot(index = "Financial_Month", columns = "Financial_Year", values = "Amount")
pivoted_yearly_sales.reset_index(inplace = True)
pivoted_yearly_sales.set_index("Financial_Month", inplace = True)
st.line_chart(pivoted_yearly_sales,x_label = "Financial Month", y_label = "Total sales")

# Partition
col5, col6 = st.columns(2)
with col5:
    st.title("Retailer count by Revenue")
    retailer_count = preprocessor.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index("revenue_percentages", inplace = True)
    st.bar_chart(retailer_count, x_label = "Revenue percentage",y_label = "Retailer count")
with col6:
    st.title("Companies count by Revenue")
    company_count = preprocessor.fetch_top_revenue_companies(filtered_df)
    company_count.set_index("company_percentages", inplace = True)
    st.bar_chart(company_count,x_label = "Revenue percentage", y_label = "Companies count")