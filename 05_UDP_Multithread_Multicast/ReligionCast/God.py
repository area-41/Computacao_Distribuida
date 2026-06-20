import socket
import struct
import time
import threading
import os


class MulticastServer:
    def __init__(self, ip='224.1.1.1', port=5000):
        self.ip = ip
        self.port = port
        self.running = False

    def transmitir(self, arquivo_path):
        if not os.path.exists(arquivo_path):
            print(f"\n[Erro] Arquivo {arquivo_path} não encontrado.")
            return

        self.running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        print(f"\n>>> Transmitindo conteúdo de: {arquivo_path}\n")

        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    if not self.running: break

                    texto = linha.strip()
                    if texto:
                        sock.sendto(texto.encode('utf-8'), (self.ip, self.port))
                        # print(f"[Enviado]: {texto[:80]}")
                        print(f"\n{texto[:80]}\n")
                        time.sleep(5)  # Intervalo para leitura
        except Exception as e:
            print(f"Erro na transmissão: {e}")
        finally:
            sock.close()
            self.running = False
            print("\n>>> Transmissão finalizada. Pressione Enter para voltar ao menu.")


def exibir_menu():
    print("\n" + "=" * 30)
    print("SISTEMA DE TRANSMISSÃO RELIGIOSA")
    print("=" * 30)
    print("1. Bíblia")
    print("2. Alcorão")
    print("3. Bhagavad Gita (Indu)")
    print("4. O Livro dos Espíritos (Espírita)")
    print("5. Budista")
    print("6. Taoista")
    print("7. Nordica")
    print("0. Sair")
    return input("\nEscolha uma opção: ")


def main():
    server = MulticastServer()
    opcoes = {
        '1': 'biblia.txt',
        '2': 'alcorao.txt',
        '3': 'indu.txt',
        '4': 'espirita.txt',
        '5': 'budista.txt',
        '6': 'taoista.txt',
        '7': 'nordica.txt'
    }

    while True:
        escolha = exibir_menu()

        if escolha == '0':
            print("Encerrando...")
            break

        if escolha in opcoes:
            if server.running:
                print("\nAguarde a transmissão atual terminar ou reinicie o programa.")
                continue

            # Dispara a transmissão em uma thread separada
            t = threading.Thread(target=server.transmitir, args=(opcoes[escolha],))
            t.daemon = True
            t.start()
        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    main()