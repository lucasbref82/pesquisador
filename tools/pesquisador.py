import json
import os
import requests
from langchain.tools import tool


class SearchTool:
    """Ferramenta de busca personalizada usando Serper.dev"""

    @tool("Procurar na internet")
    def search_google(query):
        """Usado para buscar informações na web e resultados relevantes."""
        print("Buscando na web...")
        numero_resultados_retornados = 5
        url = "https://google.serper.dev/search"
        payload = json.dumps(
            {"q": query, "num": numero_resultados_retornados, "tbm": "nws"}
        )
        headers = {
            "X-API-KEY": os.environ.get("SERPER_API_KEY"),
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if "organic" not in response.json():
            return "Desculpe, não consegui encontrar nada."
        else:
            resultados = response.json()["organic"]
            string = []
            print("Resultados:", resultados[:numero_resultados_retornados])
            for resultado in resultados[:numero_resultados_retornados]:
                try:
                    date = resultado.get("date", "Data não disponível")
                    string.append(
                        (
                            "\n".join(
                                [
                                    f"Titulo: {resultado.get('title', 'Título não disponível')}",
                                    f"Link: {resultado.get('link', 'Link não disponível')}",
                                    f"Data: {date}",
                                    f"Trecho: {resultado.get('snippet', 'Trecho não disponível')}",
                                ]
                            )
                        )
                    )
                except KeyError:
                    continue
        return "\n".join(string)
