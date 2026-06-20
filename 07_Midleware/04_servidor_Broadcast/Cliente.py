from Pyro5.api import Proxy


def mostrar_menu():
    print("\n==== Cadastro de Clientes ====")
    print("1 - Incluir cliente")
    print("2 - Consultar cliente")
    print("3 - Listar todos os clientes")
    print("0 - Sair")


def main():
    try:
        cadastro = Proxy("PYRONAME:cadastroClientes@192.168.5.175:9090")
    except Exception as e:
        print("Erro ao conectar no servidor:", e)
        return

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            codigo = input("Código: ")
            nome = input("Nome: ")
            cidade = input("Cidade: ")

            ok = cadastro.incluir(codigo, nome, cidade)
            if ok:
                print("Cliente incluído com sucesso.")
            else:
                print("Código já existente. Cliente não incluído.")

        elif opcao == "2":
            codigo = input("Código do cliente: ")
            cliente = cadastro.consultar(codigo)

            if cliente is None:
                print("Cliente não encontrado.")
            else:
                print("Cliente encontrado:")
                print("Código:", cliente["codigo"])
                print("Nome:", cliente["nome"])
                print("Cidade:", cliente["cidade"])

        elif opcao == "3":
            clientes = cadastro.listarTodos()

            if not clientes:
                print("Nenhum cliente cadastrado.")
            else:
                print("\nLista de clientes:")
                for c in clientes:
                    print(
                        "Código:", c["codigo"],
                        "| Nome:", c["nome"],
                        "| Cidade:", c["cidade"]
                    )

        elif opcao == "0":
            print("Encerrando cliente...")
            break

        else:
            print("Opção inválida.")    


if __name__ == "__main__":
    main()
