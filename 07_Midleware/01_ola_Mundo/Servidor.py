import Pyro5.api


@Pyro5.api.expose
class OlaMundo:
    def olaMundo(self):
        return "Ola Mundo dos Objetos Remotos"


def main():
    servidor_nomes = Pyro5.api.locate_ns()

    thread_daemon = Pyro5.api.Daemon()
    objeto_ola = OlaMundo()
    endereco = thread_daemon.register(objeto_ola)         

    servidor_nomes.register("olaMundo", endereco)

    print("Aguardando conexões...")    
    print("URI:", endereco)

    thread_daemon.requestLoop()


if __name__ == "__main__":
    main()
