import time
import sys
import os
import Pyro5.api
import psutil  # Requer instalação prévia (pip install psutil)

def obter_memoria_atual() -> float:
    """Retorna o uso de memória do processo atual em Megabytes (MB)."""
    processo = psutil.Process(os.getpid())
    return processo.memory_info().rss / (1024 * 1024)

def executar_cliente_quatro(id_cliente="Cliente-4"):
    print(f"--- Iniciando {id_cliente} via Interpretador Python ---")
    
    # Captura métricas iniciais do sistema antes da carga
    memoria_inicial = obter_memoria_atual()
    tempo_inicio_total = time.perf_counter()
    
    try:
        # Busca o objeto remoto diretamente pelo Name Server travado no localhost
        gerador = Pyro5.api.Proxy("PYRONAME:objeto.randomico@127.0.0.1")
        
        # Rotina em loop para simular requisições contínuas
        for i in range(1, 6):
            print(f"\n[{id_cliente}] Iteração de teste {i}/5:")
            
            quantidade = i * 2
            inicio, fim = 100 * i, 200 * i
            
            # --- CRONOMETRAGEM DA CHAMADA REMOTA ---
            tempo_envio = time.perf_counter()
            
            resultados = gerador.n_inteiros_no_intervalo(quantidade, inicio, fim)
            
            tempo_resposta = time.perf_counter()
            latencia_rmi = (tempo_resposta - tempo_envio) * 1000  # Convertendo para milissegundos
            # ----------------------------------------
            
            print(f" -> Gerados {quantidade} números entre {inicio} e {fim}: {resultados}")
            print(f" ⏱️  Tempo da requisição RMI: {latencia_rmi:.2f} ms")
            
            # Delay para acompanhamento visual de concorrência
            time.sleep(1.5)
            
        print(f"\n--- {id_cliente} finalizou todos os testes com sucesso! ---")
        
    except Exception as e:
        print(f"Erro crítico no {id_cliente}: {e}")
    
    finally:
        # Captura métricas finais após a execução
        tempo_fim_total = time.perf_counter()
        memoria_final = obter_memoria_atual()
        
        tempo_total_gasto = tempo_fim_total - tempo_inicio_total
        variacao_memoria = memoria_final - memoria_inicial
        
        print("\n" + "="*50)
        print(f"📊 RELATÓRIO DE DESEMPENHO - {id_cliente}")
        print("="*50)
        print(f"⏱️  Tempo total de execução do script: {tempo_total_gasto:.2f} segundos (incluindo sleeps)")
        print(f"💾 Memória RAM Inicial: {memoria_inicial:.2f} MB")
        print(f"💾 Memória RAM Final: {memoria_final:.2f} MB")
        print(f"📈 Variação de Memória durante o teste: {variacao_memoria:+.4f} MB")
        print("="*50)

if __name__ == "__main__":
    # Captura o nome passado por argumento (ex: python Cliente_4.py Carlos)
    nome = sys.argv[1] if len(sys.argv) > 1 else "Cliente-4-Padrao"
    executar_cliente_quatro(nome)