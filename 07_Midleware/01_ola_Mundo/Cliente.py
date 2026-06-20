from Pyro5.api import Proxy


def main():
    objeto_ola = Proxy("PYRONAME:olaMundo")
    print("Resposta do Servidor: ", objeto_ola.olaMundo())


if __name__ == "__main__":
    main()
