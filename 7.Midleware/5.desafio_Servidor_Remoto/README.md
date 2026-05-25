# Desafio 

Desenvolva uma aplicação distribuída composta por um servidor, que disponibiliza um objeto remoto responsável por gerar números randômicos; e um cliente, que acessa esse objeto remoto exclusivamente por meio do Name Server.

O servidor deverá implementar os seguintes métodos remotos:

- def inteiro_aleatorio(self):
- def n_inteiros_aleatorios(self, n):
- def inteiro_no_intervalo(self, inicio, fim):
- def n_inteiros_no_intervalo(self, n, inicio, fim):
    Nos métodos de vários inteiros, como sugestão, utilize list[int].

Além de testar os métodos no cliente, faça a execução de dois ou mais clientes simultaneamente. 