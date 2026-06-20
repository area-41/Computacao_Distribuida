import requests

def obter_regiao(nome_estado):
    # URL da API de localidades do IBGE
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

    try:
        # Faz a requisição HTTP
        resposta = requests.get(url)
        # gera um erro se falhar a conexão
        resposta.raise_for_status()  

        # Converte o resultado em uma lista de dicionários
        estados = resposta.json()

        # Percorre todos os estados retornados pela API
        for estado in estados:            
            if estado["nome"].lower() == nome_estado.lower():            
                return estado["regiao"]["nome"]
            
        # não obter regiao
        return None

    except requests.RequestException as e:
        print(f"Erro ao consultar IBGE: {e}")
        return None