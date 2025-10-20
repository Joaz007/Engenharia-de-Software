class Aluna:
    def __init__(self, nome, apelido, sexo, nascimento, cep, endereco, bairro, celular, cpf, dias, horario, valor, vencimento, termo):
        self.nome = nome
        self.apelido = apelido
        self.sexo = sexo
        self.nascimento = nascimento
        self.cep = cep
        self.endereco = endereco
        self.bairro = bairro
        self.celular = celular
        self.cpf = cpf
        self.dias = dias
        self.horario = horario
        self.valor = valor
        self.vencimento = vencimento
        self.termo = termo

        print(
            nome + "\n" + apelido + "\n" + sexo + "\n" + nascimento + "\n" + cep + "\n" +
            endereco + "\n" + bairro + "\n" + celular + "\n" + cpf + "\n" +
            str(dias) + "\n" + horario + "\n" + str(valor) + "\n" + str(vencimento) + "\n" + str(termo)
        )


newAluna = Aluna("Maria Eduarda", "Duda", "F", "21/10/2005", "86800-014", "Rua Munhoz da Rocha, 1527", "Centro", "43998710567", "11734664959", 2, "19:30", "200.00", 10, 1)

def InserirInfosAlunas():
    print("==== CADASTRO DE ALUNA ==== \n")

    nome = input("Insira o nome completo da aluna:\n").strip()
    apelido = input("Apelido:\n").strip()
    sexo = input("Sexo (F/M):\n").strip()
    nascimento = input("Data de nascimento (dd/mm/aaaa):\n").strip()
    cep = input("CEP:\n").strip()
    endereco = input("Endereço:\n").strip()
    bairro = input("Bairro:\n").strip()
    celular = input("Celular:\n").strip()
    cpf = input("CPF:\n").strip()

    while True:
        try:
            dias = int(input("Quantas vezes por semana?\n"))
            break
        except ValueError:
            print("Insira um valor válido.")

    horario = input("Horário das aulas:\n").strip()

    while True:
        try:
            valor = float(input("Valor da mensalidade:\n"))
            break
        except ValueError:
            print("Insira um valor válido.")

    while True:
        try:
            vencimento = int(input("Data de vencimento da mensalidade:\n"))
            break
        except ValueError:
            print("Insira um valor numérico.")

    termo_input = input("O termo de responsabilidade foi assinado? (S/N):\n").strip().upper()
    termo = termo_input == "S"  # converte para booleano

    if not termo:
        print("\nO termo não foi assinado. O cadastro não pôde ser concluído.\n")
        return None

    # ordem correta dos parâmetros:
    nova_aluna = Aluna(
        nome, apelido, sexo, nascimento, cep, endereco, bairro,
        celular, cpf, dias, horario, valor, vencimento, termo
    )

    print("\nCadastro realizado com sucesso!\n")
    return nova_aluna

def main():

    aluna = InserirInfosAlunas()
    if aluna:
        print("Aluna cadastrada com sucesso.")
    else: 
        print("Nenhuma aluna cadastrada.")

if __name__ == "__main__":
    main()