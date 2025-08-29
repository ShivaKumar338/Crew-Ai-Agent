from crewai import Agent

class DataFormatter(Agent):
    def __init__(self, llm=None):
        super().__init__(
            name="Data Formatter",
            role="Rearrange unified data",
            goal="Create CSV and write a news review summary.",
            backstory="I take the unified product list and present it in structured CSV format with a review.",
            llm=llm
        )
