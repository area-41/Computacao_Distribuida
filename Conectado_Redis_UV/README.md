# Computação Distribuída: Comunicação com Docker & Redis

Esta pasta contém uma implementação prática de um sistema de mensageria distribuída utilizando a arquitetura **Publish/Subscribe (Pub/Sub)** do **Redis** rodando em um container **Docker**, integrado a uma interface gráfica desenvolvida em **Python (Tkinter)** com suporte a concorrência via **Threads**.

Teste desenvolvido como parte das atividades práticas do curso da **UTFPR** (Universidade Tecnológica Federal do Paraná).

---

### Arquitetura do Sistema

O Redis atua como um **Message Broker** (Intermediário de Mensagens) de alta performance rodando inteiramente em memória RAM. Em vez de estabelecer conexões de rede diretas (`socket.bind` / `connect`) e gerenciar IPs e portas para cada nó da rede, os clientes e servidores comunicam-se de forma desacoplada através de um canal centralizado.

* **Publisher (Emissor/Cliente):** Publica mensagens em um canal específico do Redis (`chat_distribuido`).
* **Subscriber (Receptor/Servidor):** Inscreve-se no mesmo canal e processa as mensagens recebidas em tempo real.
* **Interface Gráfica (Tkinter):** Utiliza uma `Thread` em segundo plano dedicada estritamente para escutar o Redis (`pubsub.listen()`), impedindo o congelamento (`freeze`) do loop principal da interface gráfica (`root.mainloop()`).


### Estrutura de Arquivos da Pasta


Conectado_Redis_UV/
├── .venv/               # Ambiente virtual isolado gerenciado pelo UV
├── app_grafica.py       # Aplicação completa com Interface Gráfica Tkinter e Threads
├── cliente.py           # Script alternativo em modo texto (Console) para envio de mensagens
├── servidor.py          # Script alternativo em modo texto (Console) para recepção de mensagens
└── README.md            # Documentação do projeto (este arquivo)



### Tecnologias Utilizadas

* **Python 3.12** (Instalado de forma otimizada via **uv**)
* **Redis 8.0** (Rodando em ambiente de micro-infraestrutura isolada via **Docker**)
* **Tkinter & TTK** (Interface nativa para renderização da janela)
* **Threading** (Para concorrência assíncrona do receptor de eventos)



### Pré-requisitos e Como Executar

### 1. Iniciar a Infraestrutura do Redis (Docker)

Certifique-se de que o Docker Desktop está aberto e inicialize o seu container do Redis utilizando o terminal:


        docker start redis



### 2. Ativar o Ambiente Virtual (`.venv`)

No VS Code, abra o terminal embutido (`Ctrl + '`) dentro da pasta do projeto. O ambiente virtual gerenciado pelo `uv` deve se ativar automaticamente, exibindo o prefixo `(.Computacao_Distribuida)`.


        source .venv/Scripts/activate



### 3. Executar a Aplicação

#### Cenário A: Executando a Interface Gráfica Integrada

Abra quantas instâncias da interface gráfica desejar para simular nós independentes da rede distribuída:


        python app_grafica.py



*Tudo o que for digitado em uma janela será transmitido via Docker/Redis e exibido nas demais janelas em tempo real.*

#### Cenário B: Executando via Linha de Comando (Terminal)

Caso queira testar a infraestrutura de forma puramente textual:

1. Em um terminal, execute o receptor:


        python servidor.py




2. Em outro terminal, execute o emissor:


        python cliente.py



### Aprendizados e Conceitos Chave 🧠

1. **Bancos de Dados Em Memória (In-Memory):** Entendimento prático de como o Redis elimina gargalos de I/O de disco gravando dados estritamente na memória RAM (reduzindo latências de milissegundos para microssegundos).
2. **Desacoplamento de Redes:** Migração de arquiteturas baseadas em Sockets IP/Porta fixos para arquiteturas orientadas a eventos (Event-Driven) usando filas/canais de Pub/Sub.
3. **Gerenciamento de Threads em Interfaces Gráficas:** Aplicação do conceito de Threads de segundo plano (`daemon=True`) para escuta de barramentos de rede bloqueantes sem interrupção do desenho da interface (Main Thread).
4. **Gerenciamento Moderno com UV:** Substituição de gerenciadores pesados (Conda/Pip globais) por um fluxo de trabalho ultra-rápido escrito em Rust, garantindo reprodutibilidade local por meio da pasta `.venv`.
"""