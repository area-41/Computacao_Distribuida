import requests

def obter_piada(nome_estado):
    # URL da API de localidades do IBGE
    url = "piadas.json"

    try:
        # Faz a requisição HTTP
        resposta = requests.get(url)
        # gera um erro se falhar a conexão
        resposta.raise_for_status()  

        # Converte o resultado em uma lista de dicionários
        piadas = resposta.json()

        print(piadas)
        # Percorre todos as piadas retornados pela API
        # for piada in piadas:
        #     if piada["nome"].lower() == nome_estado.lower():
        #         return piada["regiao"]["nome"]
            
        # não obter regiao
        return None

    except requests.RequestException as e:
        print(f"Erro na piada: {e}")
        return None