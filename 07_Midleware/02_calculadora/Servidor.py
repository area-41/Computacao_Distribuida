import Pyro5.api


@Pyro5.api.expose
class Calculadora:
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return a / b


def main():
    servidor_nomes = Pyro5.api.locate_ns()

    thread_daemon = Pyro5.api.Daemon()
    objeto_calc = Calculadora()                 
    endereco = thread_daemon.register(objeto_calc)         

    servidor_nomes.register("calc", endereco)

    print("Aguardando requisições...")
    print("URI:", endereco)

    thread_daemon.requestLoop()


if __name__ == "__main__":
    main()
