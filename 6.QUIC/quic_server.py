"""
O servidor herda de QuicConnectionProtocol. Quando um cliente abre um canal de dados (stream),
o servidor recebe os dados, processa e responde de volta naquele mesmo stream.
"""
import asyncio
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, QuicEvent


class ServerProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, StreamDataReceived):
            dados_recebidos = event.data.decode("utf-8")
            print(f"[*] Recebido no Stream {event.stream_id}: {dados_recebidos}")

            resposta = f"Olá! QUIC funcionando no Codespaces. Recebi: '{dados_recebidos}'".encode("utf-8")
            self._quic.send_stream_data(event.stream_id, resposta, end_stream=True)
            self.transmit()


async def main():
    configura_quic = QuicConfiguration(is_client=False)
    configura_quic.load_cert_chain("certificado.pem", "chave.pem")

    print("[*] Servidor QUIC aguardando conexões na porta 4433 (UDP)...")

    # Mudamos para '0.0.0.0' para aceitar conexões internas do container
    server = await serve(
        host="0.0.0.0",
        port=4433,
        configuration=configura_quic,
        create_protocol=ServerProtocol,
    )
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())