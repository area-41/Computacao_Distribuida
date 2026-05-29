# Desafio: Sistemas de Objetos Distribuídos com Pyro5
**Disciplina:** Computação Distribuída / Computação Paralela  
**Instituição:** Universidade Tecnológica Federal do Paraná (UTFPR)  

Este repositório contém a implementação de uma aplicação distribuída utilizando o middleware **Pyro5** (Python Remote Objects). O objetivo do desafio é construir um serviço distribuído composto por um servidor que disponibiliza um objeto remoto gerador de números randômicos e múltiplos clientes que acessam esse objeto concorrentemente, utilizando **exclusivamente** um Serviço de Nomes (*Name Server*) para a localização dos componentes.


Desenvolva uma aplicação distribuída composta por um servidor, que disponibiliza um objeto remoto responsável por gerar números randômicos; e um cliente, que acessa esse objeto remoto exclusivamente por meio do Name Server.

O servidor deverá implementar os seguintes métodos remotos:

- def inteiro_aleatorio(self):
- def n_inteiros_aleatorios(self, n):
- def inteiro_no_intervalo(self, inicio, fim):
- def n_inteiros_no_intervalo(self, n, inicio, fim):
    Nos métodos de vários inteiros, como sugestão, utilize list[int].

Além de testar os métodos no cliente, faça a execução de dois ou mais clientes simultaneamente. 


---
### Arquitetura do Sistema

O sistema é baseado no modelo de comunicação de objetos distribuídos e adota uma arquitetura em três camadas lógicas para desacoplamento de localização:

1. **Name Server (Serviço de Nomes):** Atua como as "páginas amarelas" (catálogo). O servidor registra sua referência remota (URI) sob um identificador textual (`objeto.randomico`), e os clientes consultam esse catálogo para obter a referência sem conhecer previamente o IP ou a porta do servidor.
2. **Servidor (Provedor do Objeto Remoto):** Instancia a classe que gera os números aleatórios, registra-a no barramento local (`Daemon`) amarrado à interface de rede loopback e publica seu identificador no Name Server.
3. **Clientes Simultâneos:** Consultam o Name Server para obter o Proxy do objeto remoto e disparam chamadas de métodos de forma transparente, simulando chamadas locais.

### Estrutura de Arquivos

5.desafio_Servidor_Remoto/
├── Servidor.py      # Implementação do objeto remoto e inicialização do Daemon
├── Cliente.py       # Ponto de entrada do cliente com testes de métodos e concorrência
└── README.md        # Documentação do desafio e guia de execução


### Métodos Remotos Expostos pelo Servidor

* `inteiro_aleatorio()`: Retorna um único inteiro aleatório entre 0 e 100.
* `n_inteiros_aleatorios(n)`: Retorna uma lista contendo `n` inteiros aleatórios entre 0 e 100.
* `inteiro_no_intervalo(inicio, fim)`: Retorna um inteiro aleatório dentro do escopo fechado `[inicio, fim]`.
* `n_inteiros_no_intervalo(n, inicio, fim)`: Retorna uma lista de `n` inteiros aleatórios contidos no escopo fechado `[inicio, fim]`.


### Como Executar o Projeto

Como o ambiente utiliza o gerenciador de pacotes de alta performance **`uv`**, certifique-se de que a dependência do `pyro5` esteja instalada no ambiente virtual da raiz do projeto (`uv pip install pyro5`).

Siga a ordem estrita de execução abrindo terminais separados:

### Passo 1: Iniciar o Name Server (Serviço de Nomes)

Em um terminal exclusivo, inicialize o Name Server travando o nó no endereço de loopback local (`127.0.0.1`) para mitigar bloqueios de firewall do Windows ou problemas com rotas de broadcast:


        uv run pyro5-ns -n 127.0.0.1


*Mantenha este terminal ativo.*

### Passo 2: Inicializar o Servidor

Abra um segundo terminal, navegue até a pasta do desafio e execute o script do Servidor. Ele irá se conectar ao Name Server criado no passo anterior e registrar o objeto gerador:


        uv run Servidor.py


O console exibirá a confirmação de que o objeto está ativo e pronto para receber requisições de threads externas.

### Passo 3: Executar Múltiplos Clientes Simultâneos

Para validar as propriedades de concorrência do middleware e o pool de threads do Pyro5, abra múltiplos terminais concorrentes e execute os clientes passando um identificador textual por argumento:

* **Terminal Cliente 1:**

        uv run Cliente.py Alfa



* **Terminal Cliente 2:**
        
        uv run Cliente.py Beta


* **Terminal Cliente 3:**

        uv run Cliente.py Teste



### Demonstração de Saída de Teste (Logs)

Quando executado com sucesso, a saída do cliente requisitando os métodos remotos via Proxy estruturado exibe o seguinte comportamento:


        uv run Cliente.py Teste
        --- Iniciando Teste ---
        [Teste] Único aleatório: 85
        [Teste] 5 aleatórios: [42, 26, 84, 60, 9]
        [Teste] Aleatório entre 10 e 50: 21
        [Teste] 4 aleatórios entre 500 e 1000: [677, 648, 935, 663]


No console do Servidor, é possível observar as chamadas sendo processadas sob demanda à medida que os clientes realizam as requisições remotas, validando o ciclo de vida distribuído.

---

*Desafio prático desenvolvido para consolidar os conceitos de Middleware, RMI (Remote Method Invocation), Name Server Resolution e Concorrência em Sistemas Distribuídos.*