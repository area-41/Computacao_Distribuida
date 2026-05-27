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
    # Inicializa o daemon do Pyro
    daemon = Pyro5.api.Daemon()
    
    # Localiza o Name Server rodando na rede
    try:
        ns = Pyro5.api.locate_ns()
    except Exception as e:
        print("Erro: Não foi possível encontrar o Name Server. Certifique-se de que ele está rodando (pyro5-ns).")
        return

    # Registra a classe no daemon
    uri = daemon.register(GeradorRandomico)
    
    # Registra o objeto no Name Server com um nome amigável
    ns.register("objeto.randomico", uri)
    
    print(f"Servidor pronto. Objeto remoto registrado com a URI:\n{uri}")
    print("Aguardando requisições...")
    
    # Inicia o loop de escuta do servidor
    daemon.requestLoop()

if __name__ == "__main__":
    iniciar_servidor()