import Pyro5.api
import random


@Pyro5.api.expose
class ValidarCPF:

    def validarCPF(self, cpf):        
        cpf = cpf.replace(".", "").replace("-", "")
        
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        digito1 = (soma * 10) % 11
        if digito1 == 10:
            digito1 = 0
        
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        digito2 = (soma * 10) % 11
        if digito2 == 10:
            digito2 = 0

        return cpf[9] == str(digito1) and cpf[10] == str(digito2)

    def gerarCPF(self):        
        cpf = [random.randint(0, 9) for _ in range(9)]
        
        soma = sum(cpf[i] * (10 - i) for i in range(9))
        digito1 = (soma * 10) % 11
        if digito1 == 10:
            digito1 = 0
        cpf.append(digito1)
        
        soma = sum(cpf[i] * (11 - i) for i in range(10))
        digito2 = (soma * 10) % 11
        if digito2 == 10:
            digito2 = 0
        cpf.append(digito2)

        return "".join(str(d) for d in cpf)

def main():
    servidor_nomes = Pyro5.api.locate_ns()

    # daemon = Pyro5.api.Daemon()
    daemon = Pyro5.api.Daemon(host="192.168.5.149")

    objeto_cpf = ValidarCPF()
    uri = daemon.register(objeto_cpf)
    

    servidor_nomes.register("validarCPF", uri)

    print("Aguardando conexões...")
    print("URI:", uri)

    daemon.requestLoop()


if __name__ == "__main__":
    main()
