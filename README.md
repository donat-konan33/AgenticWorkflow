This is an agentic workflow making.

We’ll build an autonomous research agent workflow. The workflow involves:
We could change target as well as our needs change:

Below the different steps:
- 1 -  Accepting a research topic as input.
- 2 -  Retrieving relevant web articles using an external API.
- 3 -  Summarizing the content.
- 4 - Storing the results in a local file.


Agents need a core structure to ``Perceive, Decide and Act``.
We can think this model as ``Input, Reasoning and Output`` according this
[article](https://www.datacamp.com/tutorial/openai-o1-api).

Let's break down the different steps of this workflow!

**Step 1** : Creating the Agent Framework

Basic ``Agent`` Class
Define a reusable Agent class that all agents will inherit.

**Step 2** : Implementing ``Specialized Agents``

- Input agent: Accepts the research topic.
- Retrieval agent: Fetches articles from an API.
- Summarization agent: Summarizes the content.

**Step 3** : ``Store`` summarized data

**Step 4** : Orchestrating the ``Workflow``, we define here an MCP (Multi-Component Processing) Server like LangChain
