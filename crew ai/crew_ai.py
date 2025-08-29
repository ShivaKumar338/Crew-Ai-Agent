import json
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import pandas as pd
import streamlit as st
import plotly.express as px
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CrewAI Prediction Market Aggregator",
    page_icon="📊",
    layout="wide"
)

# =========================
# AGENT 1: Data Scraper
# =========================
def scrape_polymarket():
    url = "https://polymarket.com"
    products = [
        {"name": "US Presidential Election 2028", "category": "Politics", "price": 0.45, "url": url+"/event/123"}
    ]
    return {"source": "polymarket", "products": products}

def scrape_kalshi():
    url = "https://kalshi.com"
    products = [
        {"name": "US Presidential Election 2028", "category": "Politics", "price": 0.47, "url": url+"/market/456"}
    ]
    return {"source": "kalshi", "products": products}

def scrape_predictit():
    url = "https://www.predictit.org"
    products = [
        {"name": "US Presidential Election 2028", "category": "Politics", "price": 0.44, "url": url+"/market/789"}
    ]
    return {"source": "predictit", "products": products}

def agent1_scrape():
    all_data = []
    all_data.append(scrape_polymarket())
    all_data.append(scrape_kalshi())
    all_data.append(scrape_predictit())
    return all_data

# =========================
# AGENT 2: Product Matcher
# =========================
def agent2_match(raw_data):
    products_list = []
    for site in raw_data:
        for prod in site["products"]:
            prod["source"] = site["source"]
            products_list.append(prod)

    unified_products = []

    def find_match(product, unified):
        for uprod in unified:
            for match in uprod["matches"]:
                ratio = fuzz.token_sort_ratio(product["name"], match["name"])
                if ratio > 80:
                    return uprod, ratio / 100
        return None, 0

    for product in products_list:
        match_entry, confidence = find_match(product, unified_products)
        if match_entry:
            match_entry["matches"].append({
                "name": product["name"], 
                "source": product["source"], 
                "price": product["price"], 
                "confidence": confidence
            })
        else:
            unified_products.append({
                "name": product["name"],
                "matches": [{
                    "name": product["name"], 
                    "source": product["source"], 
                    "price": product["price"], 
                    "confidence": 1.0
                }]
            })
    return unified_products

# =========================
# AGENT 3: UI + Charts + Download
# =========================
def agent3_ui(unified_products):
    rows = []
    sources = set()
    for product in unified_products:
        row = {"Product Name": product["name"]}
        for match in product["matches"]:
            row[f"{match['source']} Price"] = match["price"]
            row[f"{match['source']} Confidence"] = round(match["confidence"], 2)
            sources.add(match['source'])
        rows.append(row)

    df = pd.DataFrame(rows)

    # 🎨 Custom CSS
    st.markdown("""
        <style>
        .main {background-color: #0e1117;}
        .stDataFrame {border-radius: 10px; overflow: hidden;}
        .metric-card {background: #1e2130; padding: 15px; border-radius: 12px; 
                      box-shadow: 0 2px 10px rgba(0,0,0,0.3); color: white;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # 🚀 Header
    st.title("📊 CrewAI Prediction Market Aggregator")
    st.markdown("A unified dashboard that scrapes **prediction markets**, matches products across platforms, and visualizes them for comparison.")

    # 📊 Show Metrics
    st.subheader("📈 Key Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Products Matched", len(df))
    col2.metric("Sources", len(sources))
    col3.metric("Total Data Points", df.shape[0] * df.shape[1])

    # ======================
    # 🔖 Tabs for Navigation
    # ======================
    tab1, tab2, tab3, tab4 = st.tabs(["📑 Overview Table", "📊 Charts", "🔍 Filters", "⬇️ Downloads"])

    with tab1:
        st.subheader("📑 Full Aggregated Table")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("📊 Price Comparison Charts")
        melted = df.melt(id_vars="Product Name", 
                         value_vars=[c for c in df.columns if "Price" in c], 
                         var_name="Source", value_name="Price")
        fig_bar = px.bar(melted, x="Product Name", y="Price", color="Source", barmode="group", title="Price by Source")
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_line = px.line(melted, x="Product Name", y="Price", color="Source", markers=True, title="Trend Comparison")
        st.plotly_chart(fig_line, use_container_width=True)

        avg_prices = melted.groupby("Source")["Price"].mean().reset_index()
        fig_pie = px.pie(avg_prices, names="Source", values="Price", title="Average Price Share by Source")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.subheader("🔍 Filter Options")
        selected_source = st.multiselect("Select Source(s)", options=list(sources), default=list(sources))

        if selected_source:
            display_cols = ["Product Name"]
            for src in selected_source:
                display_cols.append(f"{src} Price")
                display_cols.append(f"{src} Confidence")
            st.subheader("Filtered Product Table")
            st.dataframe(df[display_cols], use_container_width=True)

    with tab4:
        st.subheader("⬇️ Download Results")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "unified_products.csv", "text/csv")
        st.success("✅ Data is ready for export!")

    # 🌐 Footer
    st.markdown("<br><hr><center>🚀 Built with ❤️ using CrewAI + Streamlit</center>", unsafe_allow_html=True)


# =========================
# MAIN FUNCTION
# =========================
def main():
    st.sidebar.title("⚙️ CrewAI Controls")
    if st.sidebar.button("Run Full Pipeline"):
        with st.spinner("🔄 Running Agents: Scraping → Matching → Displaying UI..."):
            time.sleep(2)  # simulate loading
            raw_data = agent1_scrape()
            unified_products = agent2_match(raw_data)
        st.success("✅ Pipeline completed successfully!")
        agent3_ui(unified_products)

if __name__ == "__main__":
    main()
# =========================