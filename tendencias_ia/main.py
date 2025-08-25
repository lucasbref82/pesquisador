import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

# Configurar chaves de API
open_api_key = os.environ["OPENAI_API_KEY"]
serper_api_key = os.environ["SERPER_API_KEY"]

# Ferramenta de busca
search_tool = SerperDevTool()

# Criar agente
agent = Agent(
    role="Pesquisador",
    goal="Encontrar e resumir as últimas notícias de IA",
    backstory="Você é um pesquisador experiente que busca informações relevantes.",
)

# Criar tarefa
task = Task(
    description="Pesquise e resuma as últimas 3 notícias sobre IA",
    expected_output="Um resumo em tópicos das 3 principais notícias de IA.",
    agent=agent,
    tools=[search_tool],
)

# Criar crew e rodar
crew = Crew(agents=[agent], tasks=[task])
resultado = crew.kickoff()

print("Resultado da pesquisa:\n", resultado)