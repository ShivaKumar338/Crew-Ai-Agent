from crewai import Agent

class DataCollector(Agent):
    def __init__(self, llm=None):
        super().__init__(
            name="Data Collector",
            role="Scrape gambling/prediction sites",
            goal="Collect product prices from Polymarket, Kalshi, etc.",
            backstory="I gather market data from multiple prediction/gambling sites for analysis.",
            llm=llm  # 👈 pass the LLM here
        )
