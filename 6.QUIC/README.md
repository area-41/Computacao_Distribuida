## Análise Técnica do Código

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