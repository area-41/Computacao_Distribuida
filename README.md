# Projetos de Computação Distribuída

Este repositório contém uma coleção de implementações práticas e laboratórios desenvolvidos para o estudo de **Sistemas Distribuídos**, cobrindo desde a comunicação básica via Sockets de transporte até protocolos modernos da camada de aplicação e arquiteturas híbridas de mensageria.

---

### Estrutura do Repositório

O repositório está organizado em módulos progressivos para facilitar o entendimento do fluxo de dados e dos paradigmas de rede os quais foram estudados ao longo do curso, somados ao QUIC e desafios sugeridos, assim como um estudo utilizando Redis e gerenciador UV para verificação de velocidade manutenção de pacotes:

| Módulo / Pasta | Descrição Teórica & Prática | Tecnologias Utilizadas |
| :--- | :--- | :--- |
| **`1.Protocolos_TCP`** | Implementação de canais de comunicação orientados à conexão estáveis. Desenvolvimento de um sistema de chat básico para validação de fluxo síncrono. | Python (`socket` TCP) |
| **`2.TCP_Multithread`** | Evolução do servidor TCP utilizando concorrência para gerenciar múltiplos clientes simultâneos sem bloqueio de chamadas (*I/O Blocking*). | Python `threading` |
| **`3.Mensageria_Distribuda`** | Estudos e laboratórios voltados à arquitetura baseada em eventos e filas de mensagens. | Protocolos de Mensageria / Broker |
| **`4.Protocolo_UDP`** | Comunicação rápida não-orientada à conexão. Experimentos com fluxos contínuos de dados e geradores de conteúdo sob demanda. | Python (`socket` UDP) |
| **`5.UDP_Multithread_Multicast`** | Distribuição de dados em larga escala (*um-para-muitos*) via canais lógicos multicast combinada com execução concorrente. | Multicast IP (`224.0.0.1`) |
| **`6.QUIC`** | Implementação de comunicação utilizando o protocolo moderno **QUIC** (base do HTTP/3), explorando multiplexação por streams e TLS nativo sobre UDP. | `aioquic`, `asyncio`, OpenSSL |
| **`Conectado_Redis_UV`** | Integração de sistemas distribuídos com bancos de dados em memória de alta performance para gerenciamento de cache e estados globais. | Redis, Python |
| **`Desafio_Uni_Multicast`** | **Projeto Integrador:** Sistema de Quiz dinâmico com arquitetura de rede híbrida. Envio global de perguntas e resultados (Multicast/Local Loopback) e votação privada (Unicast UDP). | Sockets UDP Híbridos, JSON |


#### Como Executar os Laboratórios Principais

### O Desafio Híbrido (Quiz Unicast/Multicast Local)
Este projeto simula uma infraestrutura de rede onde uma entidade centralizada distribui dados globais e computa métricas individuais de forma privada.

1. Navegue até a pasta do desafio:
   
       cd Desafio_Uni_Multicast

2. Inicie o servidor central que gerencia o banco de questões (`questoes.json`), embaralha os dados e calcula as porcentagens de acertos:

       python servidor.py

3. Abra novas abas de terminal (no PyCharm ou terminal do sistema) para simular quantos participantes desejar e inicialize os clientes:

        python cliente.py


### O Protocolo QUIC (Módulo 6)
Demonstração prática de streams não bloqueantes usando programação assíncrona.

> 💡 **Nota de Ambiente:** Este módulo possui suporte nativo para **GitHub Codespaces** através da configuração integrada na pasta `.devcontainer`.

1. Certifique-se de que a biblioteca está instalada e os certificados TLS foram gerados via OpenSSL:

        pip install aioquic
        openssl req -newkey rsa:2048 -nodes -keyout chave.pem -x509 -days 365 -out certificado.pem -subj "/CN=localhost"

2. Execute o servidor assíncrono:

        python quic_server.py

3. Em outro terminal, execute o cliente para disparar payloads concorrentes:

        python quic_client.py

### Requisitos de Sistema

* **Linguagem:** Python 3.9 ou superior
* **Ambiente Recomendado:** PyCharm IDE ou VS Code (com suporte a Dev Containers / GitHub Codespaces)
* **Dependências Principais:** `aioquic` (para o Módulo 6), bibliotecas nativas `socket`, `threading` e `asyncio`.

---
 *Repositório desenvolvido para fins acadêmicos na Universidade Tecnológica Federal do Paraná (UTFPR).*
