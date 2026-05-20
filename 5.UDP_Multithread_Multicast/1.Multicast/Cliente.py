import socket
import struct # utilizado para indicar o endereco multicast e o IP local

GRUPO = '224.1.1.7' # endereco multicast
PORTA = 50000  

conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# setsockopt permite configurar parâmetros, como SO_REUSEADDR, que permite o bind de vários processos
# com o mesmo endereco/porta. Evita o erro Address already in use
conexao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# o '' porque o grupo multicast não é um IP local, mas sim um IP virtual de grupo.
# Assim ele aceita pacotes para qq IP local.
conexao.bind(('', PORTA))

# 4s4s representa o endereco multicast (4 bytes - socket.inet_aton(GRUPO)) 
# e um endereco local (0.0.0.0)
multicast = struct.pack('4s4s', socket.inet_aton(GRUPO), socket.inet_aton('0.0.0.0'))

# o item multicast indica o IP multicast e o IP da interface que recebe os pacotes
# portanto, setsockopt configura esses endereços
conexao.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast)

print(f"Cliente aguardando valores em {GRUPO}:{PORTA}")
while True:
    dados, _ = conexao.recvfrom(1024)
    print("recebe: ", dados.decode('utf-8', errors='ignore'))
