import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Superstore Retail Profitability",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data():
    df = pd.read_csv("superstore_cleaned.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Profit Margin"] = (df["Profit"] / df["Sales"]) * 100
    return df


df = load_data()

st.title("E-Commerce Retail Performance & Profitability Dashboard")
st.caption("Executive Overview & Profit Leakage Diagnostic")

# Sidebar Filters
st.sidebar.header("Filter Analytics")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique(),
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique(),
)

filtered_df = df[
    (df["Region"].isin(selected_region))
    & (df["Category"].isin(selected_category))
]

# Top KPI Metrics
col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
overall_margin = (
    (total_profit / total_sales * 100) if total_sales != 0 else 0
)
avg_discount = filtered_df["Discount"].mean() * 100

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Avg Profit Margin", f"{overall_margin:.1f}%")
col4.metric("Avg Discount Rate", f"{avg_discount:.1f}%")

st.divider()

# Visualization Row
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Profit Leakage by Sub-Category")
    subcat_summary = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .reset_index()
        .sort_values(by="Profit")
    )
    fig_subcat = px.bar(
        subcat_summary,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        color_continuous_scale="RdYlGn",
        title="Total Profit / Loss by Sub-Category",
    )
    st.plotly_chart(fig_subcat, width="stretch")

with col_right:
    st.subheader("2. Impact of Discounts on Profit Margin")
    fig_scatter = px.scatter(
        filtered_df,
        x="Discount",
        y="Profit Margin",
        color="Category",
        hover_data=["Sub-Category", "Sales", "Profit"],
        title="Discount Rate vs. Profit Margin %",
    )
    st.plotly_chart(fig_scatter, width="stretch")