import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Verify key is loaded
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Please set it in .env or environment variables.")

print("✅ Gemini key loaded successfully")


from crewai import Crew, Flow, Task
from agents.collector import DataCollector
from agents.matcher import ProductMatcher
from agents.formatter import DataFormatter
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Define agents with Gemini LLM
    collector = DataCollector(llm="gemini/gemini-1.5-flash")
    matcher = ProductMatcher(llm="gemini/gemini-1.5-flash")
    formatter = DataFormatter(llm="gemini/gemini-1.5-flash")

    # Define tasks with expected_output 👇
    task_collect = Task(
        description="Scrape prediction/gambling sites and collect product prices.",
        expected_output="A raw dataset of product names and prices scraped from Polymarket, Kalshi, etc.",
        agent=collector
    )

    task_match = Task(
        description="Match products across different sites by comparing names and descriptions.",
        expected_output="A unified dataset where the same products across platforms are matched.",
        agent=matcher
    )

    task_format = Task(
        description="Format the unified product list into a CSV and create a summary review.",
        expected_output="A CSV file saved to output/results.csv and a short summary saved to output/review.txt.",
        agent=formatter
    )

    # Define the flow with agents + tasks
    crew = Crew(
        agents=[collector, matcher, formatter],
        tasks=[task_collect, task_match, task_format]
    )

    result = crew.kickoff()

    print("\n✅ Unified product data pipeline completed.")
    print("CSV saved to output/results.csv")
    print("News review saved to output/review.txt")

if __name__ == "__main__":
    main()
