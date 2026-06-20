import Pyro5.api


@Pyro5.api.expose
class CadastroClientes:
    def __init__(self):
        self.clientes = {}

    def incluir(self, codigo, nome, cidade):
        codigo = str(codigo).strip()

        if codigo in self.clientes:
            return False

        self.clientes[codigo] = {
            "codigo": codigo,
            "nome": str(nome).strip(),
            "cidade": str(cidade).strip()
        }
        return True

    def consultar(self, codigo):
        codigo = str(codigo).strip()
        return self.clientes.get(codigo)

    def listarTodos(self):
        return list(self.clientes.values())


def main():
    # servidor_nomes = Pyro5.api.locate_ns()
    servidor_nomes = Pyro5.api.locate_ns(host="192.168.5.175", port=9090)

    # thread_daemon = Pyro5.api.Daemon()
    thread_daemon = Pyro5.api.Daemon(host="192.168.5.149")

    objeto = CadastroClientes()
    endereco = thread_daemon.register(objeto)

    servidor_nomes.register("cadastroClientes", endereco)

    print("Aguardando conexões...")
    print("URI:", endereco)

    thread_daemon.requestLoop()


if __name__ == "__main__":
    main()
