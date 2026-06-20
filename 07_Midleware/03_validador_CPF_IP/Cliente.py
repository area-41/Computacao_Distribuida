from Pyro5.api import Proxy


def main():
    objeto_cpf = Proxy("PYRONAME:validarCPF")
    
    cpf_gerado = objeto_cpf.gerarCPF()
    print("CPF gerado pelo servidor:", cpf_gerado)
    
    valido = objeto_cpf.validarCPF(cpf_gerado)
    print("CPF gerado é válido?", valido)
    
    cpf_invalido = "11111111111"
    valido = objeto_cpf.validarCPF(cpf_invalido)
    print("CPF", cpf_invalido, "é válido?", valido)


if __name__ == "__main__":
    main()
