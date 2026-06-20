import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, QuicEvent


class ClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resposta_recebida = asyncio.Event()

    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, StreamDataReceived):
            print(f"\n[Resposta do Servidor]: {event.data.decode('utf-8')}")
            self.resposta_recebida.set()


async def main():
    configura_quic = QuicConfiguration(is_client=True)
    configura_quic.verify_mode = False

    print("[*] Conectando ao servidor local via QUIC...")

    async with connect("127.0.0.1", 4433, configuration=configura_quic, create_protocol=ClientProtocol) as cliente:
        stream_id = cliente._quic.get_next_available_stream_id()
        mensagem = b"Mensagem vinda do cliente QUIC no Codespaces!"

        cliente._quic.send_stream_data(stream_id, mensagem, end_stream=True)
        cliente.transmit()

        await cliente.resposta_recebida.wait()


if __name__ == "__main__":
    asyncio.run(main())