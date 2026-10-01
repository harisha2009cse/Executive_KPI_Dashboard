import streamlit as st
import pandas as pd
import plotly.express as px
# Page settings
st.set_page_config(
    page_title="Business Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")


df = load_data()

# Create Revenue column
if "quantity" in df.columns and "unit_price" in df.columns:
    df["Revenue"] = df["quantity"] * df["unit_price"]

    if "discount_pct" in df.columns:
        df["Revenue"] = df["Revenue"] * (
            1 - df["discount_pct"].fillna(0) / 100
        )
else:
    df["Revenue"] = 0


# Convert date
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )


# Title
st.title("📊 Business Performance Dashboard")
st.write("Interactive KPI Dashboard")


# Sidebar
st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()


# Category filter
if "category" in df.columns:

    categories = df["category"].dropna().unique().tolist()

    selected_category = st.sidebar.multiselect(
        "Select Category",
        categories,
        default=categories
    )

    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_category)
    ]


# Customer segment filter
if "customer_segment" in df.columns:

    segments = df["customer_segment"].dropna().unique().tolist()

    selected_segment = st.sidebar.multiselect(
        "Select Customer Segment",
        segments,
        default=segments
    )

    filtered_df = filtered_df[
        filtered_df["customer_segment"].isin(selected_segment)
    ]


# City filter
if "city" in df.columns:

    cities = df["city"].dropna().unique().tolist()

    selected_city = st.sidebar.multiselect(
        "Select City",
        cities,
        default=cities
    )

    filtered_df = filtered_df[
        filtered_df["city"].isin(selected_city)
    ]


# KPI calculations
total_revenue = filtered_df["Revenue"].sum()

if "order_id" in filtered_df.columns:
    total_orders = filtered_df["order_id"].nunique()
else:
    total_orders = len(filtered_df)


if total_orders > 0:
    average_order_value = total_revenue / total_orders
else:
    average_order_value = 0


if "customer_segment" in filtered_df.columns:
    total_customers = filtered_df["customer_segment"].nunique()
else:
    total_customers = 0


if total_customers > 0:
    customer_acquisition_cost = (
        total_revenue / total_customers
    )
else:
    customer_acquisition_cost = 0
# Churn Rate
if "churn" in filtered_df.columns:
    churn_rate = filtered_df["churn"].mean() * 100
elif "churn_rate" in filtered_df.columns:
    churn_rate = filtered_df["churn_rate"].mean()
else:
    churn_rate = 0


# KPI Cards
st.subheader("Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "👥 Customer Acquisition Cost",
        f"₹{customer_acquisition_cost:,.2f}"
    )

with col3:
    st.metric(
        "🔄 Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col4:
    st.metric(
        "🛒 Average Order Value",
        f"₹{average_order_value:,.2f}"
    )


st.divider()


# Revenue Trend
st.subheader("📈 Revenue Trend")

if "order_date" in filtered_df.columns:

    trend_data = (
        filtered_df
        .dropna(subset=["order_date"])
        .groupby("order_date", as_index=False)["Revenue"]
        .sum()
    )

    fig = px.area(
        trend_data,
        x="order_date",
        y="Revenue",
        title="Revenue Over Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Revenue by Category
if "category" in filtered_df.columns:

    st.subheader("📦 Revenue by Category")

    category_data = (
        filtered_df
        .groupby("category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig_category = px.bar(
        category_data,
        x="category",
        y="Revenue",
        title="Category-wise Revenue"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# Revenue by City
if "city" in filtered_df.columns:

    st.subheader("🌍 Revenue by City")

    city_data = (
        filtered_df
        .groupby("city", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig_city = px.bar(
        city_data,
        x="city",
        y="Revenue",
        title="City-wise Revenue"
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True
    )


# Revenue by Customer Segment
if "customer_segment" in filtered_df.columns:

    st.subheader("👥 Customer Segment Performance")

    segment_data = (
        filtered_df
        .groupby("customer_segment", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig_segment = px.bar(
        segment_data,
        x="customer_segment",
        y="Revenue",
        title="Revenue by Customer Segment"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )


# Filtered Data
st.subheader("📋 Filtered Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# Footer
st.divider()

st.caption(
    "Interactive Business KPI Dashboard | Built using Python, Streamlit and Plotly"
)