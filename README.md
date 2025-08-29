
# 📊 CrewAI Prediction Market Aggregator

This project is an **AI-powered multi-agent system** that scrapes **prediction/gambling markets** (like Polymarket, Kalshi, PredictIt), matches products across platforms, and formats them into structured CSV files and visual summaries.  

It uses **CrewAI agents** powered by **Gemini LLM** + a **Streamlit dashboard** for visualization.

---

## ✨ Features
- 🤖 **Multi-Agent Pipeline**
  - **Data Collector** – scrapes market data (prices, events).  
  - **Product Matcher** – compares & unifies similar products across sites.  
  - **Data Formatter** – structures results into CSV + summary text.  

- 📑 **Unified Product Dataset** across multiple sources.  
- 📊 **Interactive Dashboard** (Streamlit) with:
  - Overview tables  
  - Bar, line & pie charts  
  - Filter & download options  

- 🔐 **.env Integration** – Gemini API key securely stored.  

---

## ⚙️ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
