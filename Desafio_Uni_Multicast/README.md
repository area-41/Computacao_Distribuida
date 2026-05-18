### Exercício Desafio: 
# Unicast & Multicast

Desenvolva um modelo cliente/servidor com multicast para distribuição 
de mensagens e unicast para envio de respostas individuais.

O servidor multicast deve enviar uma pergunta de múltipla escolha a 
todos os clientes, como por exemplo:

Qual protocolo é orientado à conexão? 

A) UDP 
B) TCP 
C) ICMP)

Cada cliente deve responder via unicast com a opção escolhida.
O servidor deve contabilizar os votos e, ao final de X segundos, enviar 
o resultado (percentual de votos) via multicast a todos os participantes.

Como extensão, elabore um repositório (arquivo texto) contendo diversas 
questões, inclusive com mais alternativas, para serem enviadas pelo 
servidor. Também é possível implementar análises estatísticas dos 
resultados gerais, como porcentagem de acertos e erros. As questões 
podem ser enviadas de forma sequencial ou por meio de uma lista 
embaralhada, garantindo que nenhuma questão seja repetida durante 
a execução.


Multicast (UDP): Canal de um-para-muitos. Ideal para o servidor anunciar as perguntas
e os resultados finais para todos os clientes simultaneamente sem sobrecarregar 
a rede.

Unicast (UDP): Canal de um-para-um. Ideal para os clientes enviarem suas respostas 
individuais de volta para o IP e porta específicos do servidor, mantendo o 
anonimato entre os participantes.