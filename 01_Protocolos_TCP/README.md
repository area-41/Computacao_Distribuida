# Especialização em Python Avançado - UTFPR
## Disciplina: Python para a Computação Distribuída
**Professor:** Rogério Pozza

### Unidade 2: Protocolos TCP

Este repositório contém a progressão de estudos práticos realizados para a disciplina de **Python para a Computação Distribuída**. O objetivo central é compreender e aplicar os principais conceitos e métodos de protocolos e middleware para redes de computadores no desenvolvimento de aplicações distribuídas utilizando a biblioteca `socket` do Python.

---

## Objetivos do Projeto

O projeto demonstra a evolução técnica de um sistema Cliente-Servidor, explorando a camada de transporte e a implementação de protocolos de aplicação para:
* Estabelecer comunicação robusta via TCP/IP.
* Gerenciar sessões e estados de conexão.
* Implementar concorrência para múltiplos acessos.
* Garantir a rastreabilidade através de logs de auditoria.

---

## Estrutura do Projeto

O projeto está organizado em módulos que representam diferentes níveis de complexidade técnica:

### 01. Echo Simples (`01_echo_simples`)
* **Conceito:** Comunicação básica via sockets TCP/IP.
* **Foco:** Entender o fluxo de *handshake* inicial e a abertura/fechamento de primitivas de rede.
* **Funcionamento:** O servidor processa uma única requisição e encerra a conexão.

### 02. Loop Persistente (`02_loop_persistente`)
* **Conceito:** Gerenciamento de Sessão de Comunicação.
* **Foco:** Manter o canal de comunicação ativo para múltiplas trocas de dados sem a necessidade de novos handshakes.
* **Funcionamento:** Uso de laços de repetição e sinalizações de controle (comando "sair").

### 03. Servidor com Menu (`03_servidor_menu`)
* **Conceito:** Desenvolvimento de Protocolos de Aplicação.
* **Foco:** Criação de uma interface de serviços sobre o TCP, definindo regras de sintaxe e semântica para as mensagens.
* **Funcionamento:** Processamento de comandos específicos e retorno de respostas dinâmicas estruturadas.

### 04. Multithreading (`04_multithreading`)
* **Conceito:** Paralelismo e Concorrência em Sistemas Distribuídos.
* **Foco:** Permitir a escalabilidade do servidor para atender múltiplos clientes de forma não bloqueante.
* **Funcionamento:** Utilização da biblioteca `threading` para isolar cada conexão em um fluxo de execução independente.

### 05. Logger do Servidor (`05_logger_servidor`)
* **Conceito:** Auditoria, Persistência e Monitoramento.
* **Foco:** Aplicar métodos de registro de estado e eventos em sistemas distribuídos.
* **Funcionamento:** Registro em tempo real de IPs, timestamps e operações em arquivo físico (`log_atividades.txt`), essencial para depuração de middleware.

---

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/Computacao_Distribuida.git](https://github.com/seu-usuario/Computacao_Distribuida.git)
    ```

2.  **Inicie o Servidor:**
    Navegue até a pasta do módulo desejado e execute:
    ```bash
    python Servidor_nome_do_arquivo.py
    ```

3.  **Inicie o Cliente:**
    Em um novo terminal (ou múltiplos terminais para o caso de Multithreading), execute:
    ```bash
    python Cliente_nome_do_arquivo.py
    ```

---

## Tecnologias e Métodos
* **Python 3.x**
* **Socket API**: Comunicação em baixo nível (Camada de Transporte).
* **Threading**: Gerenciamento de concorrência.
* **I/O Handling**: Persistência de logs para auditoria de rede.

---
*Este material compõe as atividades práticas da Especialização em Python Avançado da UTFPR.*