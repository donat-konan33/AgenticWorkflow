import requests
import openai
import deepseek
import os

openai_api_key = os.environ["OPENAI_API_KEY"]
web_api_key = os.environ.get("WEB_API_KEY")

client = openai.OpenAI(api_key=openai_api_key,
                       #project='weather-2025'
                       )

class Agent:
    def __init__(self, name):
        self.name = name

    def perceive(self, input_data):
        """Receive input from the environment."""
        raise NotImplementedError("Perceive method must be implemented.")

    def decide(self):
        """Make decisions based on perceived input."""
        raise NotImplementedError("Decide method must be implemented.")

    def act(self):
        """Perform an action based on the decision."""
        raise NotImplementedError("Act method must be implemented.")


class InputAgent(Agent):
    """This agent takes a research topic as input."""
    def perceive(self, input_data):
        self.topic = input_data

    def decide(self):
        return f"Proceeding with research on: {self.topic}"

    def act(self):
        print(self.decide())
        return self.topic


class RetrievalAgent(Agent):
    """This agent uses an external API (such as a mock news API) to fetch articles."""
    def __init__(self, name, api_url):
        super().__init__(name)
        self.api_url = api_url

    def perceive(self, topic):
        self.topic = topic

    def decide(self):
        query_params = {"q": self.topic, "apiKey": web_api_key}
        return requests.get(self.api_url, params=query_params)

    def act(self):
        response = self.decide()
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            print(f"Retrieved {len(articles)} articles.")
            return articles
        else:
            print("Failed to retrieve articles.")
            return []

class SummarizationAgent(Agent):
    """This agent uses OpenAI’s API to summarize the content."""
    def perceive(self, articles):
        self.articles = articles

    def decide(self):
        summaries = []
        for article in self.articles:
            prompt = f"Summarize the following article:\n\n{article['content']}"
            response = client.completions.create(
                model="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=100
            )
            summaries.append(response.choices[0].text.strip())
        return summaries

    def act(self):
        summaries = self.decide()
        for idx, summary in enumerate(summaries):
            print(f"Summary {idx + 1}: {summary}")
        return summaries


class FileStorageAgent(Agent):
    """Adding file storage: Save the summarized content to a text file."""
    def perceive(self, summaries):
        self.summaries = summaries

    def decide(self):
        return "Summaries saved to research_summaries.txt."

    def act(self):
        with open("research_summaries.txt", "w") as file:
            for summary in self.summaries:
                file.write(summary + "\n\n")
        print(self.decide())


class Workflow:
    """integrate the agents into an orchestrated workflow."""
    def __init__(self, agents):
        self.agents = agents

    def run(self, input_data):
        current_data = input_data
        for agent in self.agents:
            agent.perceive(current_data)
            current_data = agent.act()
        print("Workflow completed.")

if __name__ == "__main__":
    # Define the API URL for article retrieval
    api_url = "https://newsapi.org/v2/everything"
    try:
        # Create agents
        input_agent = InputAgent(name="InputAgent")
        retrieval_agent = RetrievalAgent(name="RetrievalAgent", api_url=api_url)
        summarization_agent = SummarizationAgent(name="SummarizationAgent")
        file_storage_agent = FileStorageAgent(name="FileStorageAgent")

        # Orchestrate workflow
        agents = [input_agent, retrieval_agent, summarization_agent, file_storage_agent]
        research_workflow = Workflow(agents)

        # Run the workflow
        topic = "AI in Healthcare"
        research_workflow.run(topic)
    except Exception as e:
        print(f"Something was wrong, it may be due to {e}")
