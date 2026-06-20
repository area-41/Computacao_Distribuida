import time
import sys
import Pyro5.api

def executar_cliente_secundario(id_cliente="Cliente-Beta"):
    print(f"--- Iniciando {id_cliente} (Carga em Loop) ---")
    
    try:
        # Busca o objeto remoto diretamente pelo Name Server travado no localhost
        gerador = Pyro5.api.Proxy("PYRONAME:objeto.randomico@127.0.0.1")
        
        # Rotina diferenciada: Loop para simular requisições contínuas
        for i in range(1, 6):
            print(f"\n[{id_cliente}] Iteração de teste {i}/5:")
            
            # Requisitando múltiplos inteiros em um intervalo customizado
            quantidade = i * 2
            inicio, fim = 100 * i, 200 * i
            
            resultados = gerador.n_inteiros_no_intervalo(quantidade, inicio, fim)
            print(f" -> Gerados {quantidade} números entre {inicio} e {fim}: {resultados}")
            
            # Pequeno delay para podermos acompanhar a concorrência no terminal do servidor
            time.sleep(1.5)
            
        print(f"\n--- {id_cliente} finalizou todos os testes com sucesso! ---")
        
    except Exception as e:
        print(f"Erro crítico no {id_cliente}: {e}")

if __name__ == "__main__":
    nome = sys.argv[1] if len(sys.argv) > 1 else "Beta-Default"
    executar_cliente_secundario(nome)