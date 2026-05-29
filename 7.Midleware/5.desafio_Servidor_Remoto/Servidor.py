import random
import Pyro5.api

#@pyro5.expose
@Pyro5.api.expose
class GeradorRandomico:
    def inteiro_aleatorio(self) -> int:
        print("Método 'inteiro_aleatorio' executado.")
        return random.randint(0, 100)

    def n_inteiros_aleatorios(self, n: int) -> list[int]:
        print(f"Método 'n_inteiros_aleatorios' executado para n={n}.")
        return [random.randint(0, 100) for _ in range(n)]

    def inteiro_no_intervalo(self, inicio: int, fim: int) -> int:
        print(f"Método 'inteiro_no_intervalo' executado para [{inicio}, {fim}].")
        return random.randint(inicio, fim)

    def n_inteiros_no_intervalo(self, n: int, inicio: int, fim: int) -> list[int]:
        print(f"Método 'n_inteiros_no_intervalo' executado para n={n} em [{inicio}, {fim}].")
        return [random.randint(inicio, fim) for _ in range(n)]

def iniciar_servidor():
    # 1. Garante que o Daemon escute no localhost
    daemon = Pyro5.api.Daemon(host="127.0.0.1")
    
    try:
        # 2. Garante que a busca pelo Name Server vá direto para o localhost
        ns = Pyro5.api.locate_ns(host="127.0.0.1")
    except Exception as e:
        print(f"Erro: Não foi possível encontrar o Name Server. Detalhes: {e}")
        return

    # 3. Registra o objeto no Daemon e vincula ao Name Server
    uri = daemon.register(GeradorRandomico)
    ns.register("objeto.randomico", uri)
    
    print("========================================")
    print(" Servidor OBJETO.RANDOMICO Ativo!")
    print(" Status: Registrado no Name Server local.")
    print(" Aguardando requisições dos clientes... ")
    print("========================================")
    
    daemon.requestLoop()

if __name__ == "__main__":
    iniciar_servidor()