# Projeto de Redes: Chat Multi-Servidor com Relay TCP

[![Demonstração do Chat](https://img.youtube.com/vi/vndaYX5fkVg/0.jpg)](https://youtu.be/vndaYX5fkVg)
*Clique na imagem acima para assistir ao vídeo do projeto em funcionamento.*

Vídeo do Chat: https://youtu.be/vndaYX5fkVg

Olá! Este projeto foi desenvolvido para demonstrar como funciona a comunicação entre múltiplos clientes e servidores usando Sockets TCP e Threads em Python. 

A ideia principal aqui é o conceito de **Relay (Ponte)**: um cliente se conecta a um servidor, que por sua vez repassa a mensagem para outro servidor central.

## Como a arquitetura funciona?

O sistema é composto por quatro partes que se conectam em "cascata":

1.  **Cliente 01**: Conecta-se ao Servidor 01 (Porta 50000).
2.  **Servidor 01 (O Relay)**: Recebe do Cliente 01 e repassa para o Servidor 02. Ele também "ouve" o Servidor 02 para trazer novidades de volta.
3.  **Servidor 02 (O Hub Central)**: É o coração do chat. Ele recebe mensagens de todo mundo (Servidor 01 e Cliente 02) e faz um **Broadcast** (espalha a mensagem para todos os conectados).
4.  **Cliente 02**: Conecta-se diretamente ao Servidor 02 (Porta 50001).

### O Caminho da Mensagem
Quando o **Cliente 01** envia um "Oi":
`Cliente 01` ➡️ `Servidor 01` ➡️ `Servidor 02` ➡️ `Broadcast para todos (incluindo Cliente 02)`

---

## Tecnologias Utilizadas

* **Python 3**
* **Socket**: Para a comunicação de baixo nível (TCP).
* **Threading**: Para permitir que o servidor faça várias coisas ao mesmo tempo (ouvir e falar com vários clientes).
* **Tkinter**: Para a interface gráfica (GUI) bonitinha dos clientes.

---

## Como rodar o projeto?

Para que tudo funcione sem erros de conexão, você deve seguir esta ordem exata no seu terminal ou IDE (como PyCharm/VS Code):

1.  **Ligue o Servidor 02**: `python Servidor_02.py`
    * *Ele ficará aguardando na porta 50001.*
2.  **Ligue o Servidor 01**: `python Servidor_01.py`
    * *Ele vai se conectar ao S2 e ficar aguardando clientes na porta 50000.*
3.  **Abra o Cliente 02**: Conecte na porta **50001**.
4.  **Abra o Cliente 01**: Conecte na porta **50000**.

---

## O que eu aprendi fazendo isso?

* **Portas e Endereços**: Aprendi que cada serviço precisa de sua porta exclusiva (50000 e 50001) para não haver conflito.
* **Threads são vida!**: Sem elas, o servidor travaria na primeira mensagem e não conseguiria ouvir mais ninguém.
* **O problema do Bloqueio**: Entendi que o `recv()` "tranca" o código, por isso precisamos de threads dedicadas apenas para escuta em tempo real.
* **Broadcast**: É muito legal ver uma mensagem enviada por um computador aparecer em todos os outros ao mesmo tempo!

---
*Projeto desenvolvido para fins de estudo sobre Sistemas Distribuídos e Redes de Computadores.*