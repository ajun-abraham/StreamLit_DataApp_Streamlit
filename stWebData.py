import streamlit as st
import pandas as pd

# --- Config ---
dataURL = "https://raw.githubusercontent.com/Sven-Bo/datasets/master/store_sales_2022-2023.csv"
YEAR = 2023

# --- Page Setup ---

st.set_page_config(page_title="Sale Dash")
st.title("Sale Dashboard")

# --- HIDE STREAMLIT BRANDING ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -- load data ---
@st.cache_data
def loadData(url):
    data = pd.read_csv(url)
    
    data = data.assign(
        date_of_sale = lambda x: pd.to_datetime(x.date_of_sale),
        month=  lambda x: x.date_of_sale.dt.month,
        year=  lambda x: x.date_of_sale.dt.year )
    return data

data = loadData(dataURL)
CITY = data.city.unique().tolist()

revenue = data.groupby(["city","year"])["sales_amount"].sum().unstack().assign(change = lambda x: x.pct_change(axis=1)[YEAR]*100)

# --- Metric ---

cols= st.columns(3)

for idx,col in enumerate(cols):
    with col:
        st.metric(
            label=CITY[idx],
            value=f"{revenue.loc[CITY[idx],YEAR]:.2f}",
            delta=f"{revenue.loc[CITY[idx],'change']:.2f}% vs. last year"
            
        )
        

selCity = st.selectbox(
    "Select a city", CITY
)

show_previous_year = st.toggle("Show Previous Year")

if show_previous_year:
    selYear = YEAR - 1
else:
    selYear = YEAR
    
st.write(f"**Sales for {selYear}**")

tab_month,tab_category = st.tabs(["Monthly Analysis", "Category Analysis"])

with tab_month:
    filData = data.query("year == @selYear & city == @selCity").groupby("month",dropna=False,as_index=False)["sales_amount"].sum()

    st.bar_chart(
        data = filData.set_index("month")
    )
with tab_category:
    filData = data.query("year == @selYear & city == @selCity").groupby("product_category",dropna=False,as_index=False)["sales_amount"].sum()

    st.bar_chart(
        data = filData.set_index("product_category")
    )





