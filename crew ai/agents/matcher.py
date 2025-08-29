from crewai import Agent

class ProductMatcher(Agent):
    def __init__(self, llm=None):
        super().__init__(
            name="Product Matcher",
            role="Identify similar products",
            goal="Match same products across different websites.",
            backstory="I compare product names and descriptions to unify the product list.",
            llm=llm
        )
