import time
import sys
import Pyro5.api

def executar_cliente(id_cliente="Cliente-1"):
    print(f"--- Iniciando {id_cliente} ---")
    
    try:
        # Busca o objeto remoto exclusivamente pelo Name Server
        gerador = Pyro5.api.Proxy("PYRONAME:objeto.randomico@127.0.0.1")
        
        # Testando método: inteiro_aleatorio
        res1 = gerador.inteiro_aleatorio()
        print(f"[{id_cliente}] Único aleatório: {res1}")
        time.sleep(1)
        
        # Testando método: n_inteiros_aleatorios
        res2 = gerador.n_inteiros_aleatorios(5)
        print(f"[{id_cliente}] 5 aleatórios: {res2}")
        time.sleep(1)
        
        # Testando método: inteiro_no_intervalo
        res3 = gerador.inteiro_no_intervalo(10, 50)
        print(f"[{id_cliente}] Aleatório entre 10 e 50: {res3}")
        time.sleep(1)
        
        # Testando método: n_inteiros_no_intervalo
        res4 = gerador.n_inteiros_no_intervalo(4, 500, 1000)
        print(f"[{id_cliente}] 4 aleatórios entre 500 e 1000: {res4}")
        
    except Exception as e:
        print(f"Erro no {id_cliente}: {e}")

if __name__ == "__main__":
    # Permite passar o nome do cliente por argumento de linha de comando (ex: python client.py Alfa)
    nome = sys.argv[1] if len(sys.argv) > 1 else "Cliente-Padrao"
    executar_cliente(nome)