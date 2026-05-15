Estudando sobre protocolos TCP e UDP, extendi o estudo para o QUIC, mais moderno e seguro.


## Análise Técnica do Código

- Handshake Exponencial:
  Diferente do TCP, que precisaria de várias trocas de pacotes para o "aperto de mão" e depois para o TLS (criptografia), o cliente e servidor resolveram tudo isso quase instantaneamente no primeiro contato.

- UDP como Transporte:
  Por baixo dos panos, os pacotes viajaram via UDP, mas com a garantia de entrega que o aioquic implementa.

- Stream Bidirecional:
  Abriu um stream_id, enviou os dados e o servidor utilizou o mesmo ID para responder, demonstrando a capacidade de multiplexação do protocolo.


### Multiplexação por Streams: 
Note o uso de event.

            stream_id e get_next_available_stream_id()

No TCP tradicional, se você quisesse enviar duas mensagens 
isoladas, precisaria abrir duas conexões ou gerenciar um 
cabeçalho customizado. No QUIC, o próprio protocolo divide 
os canais internamente por ID, evitando o bloqueio de cabeça
de fila (HOLB).

### Abstração do UDP: 
Repare que o código não cria explicitamente um 

        socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

A biblioteca aioquic gerencia os sockets UDP por baixo dos panos
e entrega eventos de alto nível (StreamDataReceived).

### Asyncio Nativo: 
Como o QUIC é muito veloz e feito para lidar com milhares de 
fluxos concorrentes de dados (essencial no perfil de engenharia
de software moderno), frameworks que o utilizam são construídos
sobre arquiteturas não-bloqueantes (async/await).
