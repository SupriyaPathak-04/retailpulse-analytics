import streamlit as st
import pandas as pd
import plotly.express as px
#writing the heading 
# RetailPulse Analytics — original dashboard implementation

st.set_page_config(
    page_title="RetailPulse Analytics",
    layout="wide"
)

st.title("RetailPulse Analytics")
st.caption("Online retail performance • Product insights • Customer behavior")

st.sidebar.header("Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload the UCI Online Retail Excel file",
    type=["xlsx", "xls"]
)

@st.cache_data
def read_and_prepare(file_bytes):
    from io import BytesIO
    raw = pd.read_excel(BytesIO(file_bytes))
    required = {
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country"
    }
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")

    raw["InvoiceDate"] = pd.to_datetime(raw["InvoiceDate"], errors="coerce")
    raw["InvoiceNo"] = raw["InvoiceNo"].astype(str)
    raw["Revenue"] = pd.to_numeric(raw["Quantity"], errors="coerce") * pd.to_numeric(raw["UnitPrice"], errors="coerce")
    raw["Quantity"] = pd.to_numeric(raw["Quantity"], errors="coerce")
    raw["UnitPrice"] = pd.to_numeric(raw["UnitPrice"], errors="coerce")
    raw["Description"] = raw["Description"].fillna("Unknown product").astype(str)
    raw["Country"] = raw["Country"].fillna("Unknown").astype(str)

# Explicit sales-analysis rule: exclude cancellation invoices and non-positive sales rows.
    sales = raw[
        raw["InvoiceDate"].notna()
        & ~raw["InvoiceNo"].str.startswith("C")
        & (raw["Quantity"] > 0)
        & (raw["UnitPrice"] > 0)
    ].copy()
    sales = sales.dropna(subset=["Revenue"])
    return raw, sales

if uploaded_file is None:
    st.info("Upload the original UCI Online Retail Excel file using the sidebar to open the dashboard.")
    st.markdown(
        "The app expects the original transaction-level dataset with invoice, product, "
        "quantity, date, price, customer and country columns."
    )
    st.stop()

try:
    raw_df, sales_df = read_and_prepare(uploaded_file.getvalue())
except Exception as error:
    st.error(f"Could not prepare the dataset: {error}")
    st.stop()

st.sidebar.header("Filters")
date_min = sales_df["InvoiceDate"].min().date()
date_max = sales_df["InvoiceDate"].max().date()
selected_dates = st.sidebar.date_input(
    "Transaction dates",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)
all_countries = sorted(sales_df["Country"].unique())
default_countries = ["United Kingdom"] if "United Kingdom" in all_countries else all_countries
selected_countries = st.sidebar.multiselect(
    "Country",
    options=all_countries,
    default=default_countries
)

view = sales_df.copy()
if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start, end = selected_dates
    view = view[
        view["InvoiceDate"].dt.date.between(start, end)
    ]
if selected_countries:
    view = view[view["Country"].isin(selected_countries)]
else:
    view = view.iloc[0:0]

if view.empty:
    st.warning("No sales match these filters. Select a wider date range or another country.")
    st.stop()

# Overview metrics
revenue = view["Revenue"].sum()
orders = view["InvoiceNo"].nunique()
identified_customers = view["CustomerID"].nunique()
units = view["Quantity"].sum()
aov = revenue / orders if orders else 0

st.subheader("Business overview")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Revenue", f"£{revenue:,.0f}")
m2.metric("Distinct orders", f"{orders:,}")
m3.metric("Identified customers", f"{identified_customers:,}")
m4.metric("Units sold", f"{units:,.0f}")
m5.metric("Average order value", f"£{aov:,.2f}")
st.caption(
    "Revenue = Quantity × UnitPrice. Sales analysis excludes invoice numbers beginning with C "
    "and rows with non-positive quantity or unit price. Customer counts exclude missing CustomerID values."
)

# Sales trends
st.subheader("1 · Sales performance")
monthly = (
    view.assign(Month=view["InvoiceDate"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)
    .agg(Revenue=("Revenue", "sum"), Orders=("InvoiceNo", "nunique"))
)
monthly_fig = px.line(
    monthly, x="Month", y="Revenue", markers=True,
    hover_data=["Orders"], title="Monthly revenue"
)
monthly_fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (£)")
st.plotly_chart(monthly_fig, use_container_width=True)

market_col, weekday_col = st.columns(2)
with market_col:
    market = view.groupby("Country", as_index=False)["Revenue"].sum().nlargest(10, "Revenue").sort_values("Revenue")
    market_fig = px.bar(market, x="Revenue", y="Country", orientation="h", title="Top countries by revenue")
    market_fig.update_layout(xaxis_title="Revenue (£)", yaxis_title="")
    st.plotly_chart(market_fig, use_container_width=True)
with weekday_col:
    order_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_day = view.assign(Weekday=view["InvoiceDate"].dt.day_name()).groupby("Weekday", as_index=False)["Revenue"].sum()
    by_day["Weekday"] = pd.Categorical(by_day["Weekday"], categories=order_days, ordered=True)
    by_day = by_day.sort_values("Weekday")
    day_fig = px.bar(by_day, x="Weekday", y="Revenue", title="Revenue by day of week")
    day_fig.update_layout(xaxis_title="", yaxis_title="Revenue (£)")
    st.plotly_chart(day_fig, use_container_width=True)

# Product insights
st.subheader("2 · Product intelligence")
qty_col, revenue_col = st.columns(2)
with qty_col:
    product_units = view.groupby("Description", as_index=False)["Quantity"].sum().nlargest(10, "Quantity").sort_values("Quantity")
    units_fig = px.bar(product_units, x="Quantity", y="Description", orientation="h", title="Top products by units sold")
    units_fig.update_layout(xaxis_title="Units sold", yaxis_title="")
    st.plotly_chart(units_fig, use_container_width=True)
with revenue_col:
    product_revenue = view.groupby("Description", as_index=False)["Revenue"].sum().nlargest(10, "Revenue").sort_values("Revenue")
    product_fig = px.bar(product_revenue, x="Revenue", y="Description", orientation="h", title="Top products by revenue")
    product_fig.update_layout(xaxis_title="Revenue (£)", yaxis_title="")
    st.plotly_chart(product_fig, use_container_width=True)

st.caption(
    "Business interpretation: unit volume measures popularity, while revenue measures sales value. "
    "Neither alone proves profitability because product costs and margins are not included."
)

# Customer behavior
st.subheader("3 · Customer behavior")
known = view.dropna(subset=["CustomerID"]).copy()
if known.empty:
    st.info("No customer IDs are available for the current filters.")
else:
    customer_orders = known.groupby("CustomerID")["InvoiceNo"].nunique().rename("Orders").reset_index()
    repeat_rate = (customer_orders["Orders"] > 1).mean() * 100
    c1, c2 = st.columns(2)
    with c1:
        freq_fig = px.histogram(
            customer_orders, x="Orders", nbins=30,
            title="Order frequency per identified customer"
        )
        freq_fig.update_layout(xaxis_title="Distinct orders per customer", yaxis_title="Number of customers")
        st.plotly_chart(freq_fig, use_container_width=True)
    with c2:
        customer_revenue = known.groupby("CustomerID", as_index=False)["Revenue"].sum().nlargest(10, "Revenue").sort_values("Revenue")
#     spend_fig = px.bar(
#          customer_revenue,
#             x="Revenue",
#              y="CustomerID",
#     orientation="h",
#     title="Top 10 customers by revenue",
#     text="Revenue"
# )

# spend_fig.update_traces(
#     texttemplate="£%{x:,.0f}",
#     textposition="outside"
# )

# spend_fig.update_layout(
#     yaxis={"type": "category", "autorange": "reversed"},
#     xaxis_title="Revenue (£)",
#     yaxis_title="Customer ID",
#     showlegend=False
# ) 
    spend_fig = px.bar(
    customer_revenue,
    x="Revenue",
    y="CustomerID",
    orientation="h",
    title="Top 10 customers by revenue"
)

spend_fig.update_layout(
    yaxis={"type": "category", "autorange": "reversed"},
    xaxis_title="Revenue (£)",
    yaxis_title="Customer ID",
    showlegend=False
)

st.plotly_chart(spend_fig, use_container_width=True)

st.metric("Repeat-customer share in selected data", f"{repeat_rate:.1f}%")
st.caption("A repeat customer is defined here as an identified customer with more than one distinct invoice in the selected period.")

# Evidence-based takeaways
st.subheader("4 · Business takeaways")
country_totals = view.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
product_totals = view.groupby("Description")["Revenue"].sum().sort_values(ascending=False)
unit_totals = view.groupby("Description")["Quantity"].sum().sort_values(ascending=False)

if not country_totals.empty and not product_totals.empty:
    leading_country = country_totals.index[0]
    leading_revenue_product = product_totals.index[0]
    leading_units_product = unit_totals.index[0]
    st.markdown(
        f"- **Market signal:** {leading_country} has the highest revenue under the current filters "
        f"(£{country_totals.iloc[0]:,.2f}). Review customer concentration before expanding investment."
    )
    st.markdown(
        f"- **Revenue-leading product:** {leading_revenue_product} generated £{product_totals.iloc[0]:,.2f} "
        "in recorded revenue. Check margins and stock availability before prioritizing it."
    )
    st.markdown(
        f"- **Volume-leading product:** {leading_units_product} has the highest total units sold "
        f"({unit_totals.iloc[0]:,.0f}). Compare it with the revenue ranking to distinguish volume from value."
    )
if not known.empty:
    st.markdown(
        f"- **Retention opportunity:** {repeat_rate:.1f}% of identified customers in the current selection "
        "placed more than one order. Consider testing a re-engagement message for one-time buyers and measure the result."
    )
st.caption("These takeaways describe patterns in historical data. They do not establish causation or guarantee future outcomes.")

with st.expander("Inspect filtered transaction sample"):
    # st.dataframe(view.head(1000), use_container_width=True, hide_index=True)
    display_view = view.head(1000).copy()
    display_view["StockCode"] = display_view["StockCode"].astype(str)
    st.dataframe(display_view, use_container_width=True, hide_index=True)
    st.caption(f"Showing up to 1,000 of {len(view):,} filtered transaction rows.")

st.divider()
st.caption("RetailPulse Analytics · Python, Pandas, Streamlit and Plotly · Dataset: UCI Online Retail")
