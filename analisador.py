import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

load_dotenv()

open_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

llm = ChatOpenAI(api_key=open_api_key, model="gpt-4o")

search_tool = SerperDevTool(api_key=serper_api_key)


analista_fundamentalista = Agent(
    role='Analista Financeiro Fundamentalista',
    goal='Analisar os fundamentos financeiros de BBAS3',
    backstory="""Você é um analista financeiro Sênior especializado em analise fundamentalista.
    Seu trabalho é avaliar o valor intrínseco das empresas com base em seus balanços, demonstrações de resultados e outros indicadores financeiros.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool]
)

analista_tecnico = Agent(
    role='Analista Técnico de Ações',
    goal='Analisar os padrões gráficos e indicadores técnicos de BBAS3',
    backstory="""Você é um analista tecnico Sênior especializado em análise de gráficos de ações.
    Seu trabalho é identificar padrões de preço e volume, além de utilizar indicadores técnicos para prever moviemntos futuros das ações.""",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools=[search_tool]
)

tarefa_fundamendalista = Task(
    description="""Conduza uma análise fundamentalista completa da ação BBAS3.
    Avalie os balanços financeiros, demonstrações de resultados, fluxo de caixa, indicadores de rentabilidade, liquidez e endividamento""",
    expected_output='Relatório completo com avaliação dos fundamentos financeiros da BBAS3',
    agent=analista_fundamentalista
)

tarefa_tecnica = Task(
    description= """Conduza uma análise técnica completa da ação BBAS3.
    Avalie os padrões gráficos indicadores técnicos (como médias móveis, RSI, MACD) e identifique possíveis pontos de entrada e saída.""",
    expected_output='Relatório completo com avaliação técnica da BBAS3',
    agent=analista_tecnico
)

equipe = Crew(
    agents=[analista_fundamentalista, analista_tecnico],
    tasks=[tarefa_fundamendalista, tarefa_tecnica],
    verbose=True,
    process=Process.sequential
)

resultado = equipe.kickoff(inputs={"input" : "BBAS3"})

print("#########################")
print(resultado)