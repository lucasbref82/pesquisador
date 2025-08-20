import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "SUA_CHAVE_AQUI"
os.environ["OPENAI_API_KEY"] = "SUA_CHAVE_OPENAI_AQUI"

search_tool = SerperDevTool()

agent = Agent(
    role="Pesquisador",
    goal="Encontrar e resumiar as ultimas notícias de IA",
    backstory="Você é um pesquisador em uma grande empresa. Você é responsável por analisar dados e fornecer insights para o negócio."
)


print("Agente criado:",agent.role)

task = Task(
    description="Encontrar e resumir as últimas notícias de IA",
    expected_output="Um resumo em lista de tópicos das 5 notícias de IA mais importantes.",
    agent=agent,
    tools=[search_tool]
)

crew = Crew(
    agents=[agent],
    tasks=[task]
)

result = crew.kickoff()
print(result)