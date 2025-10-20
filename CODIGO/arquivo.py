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

        print(nome + "\n" + apelido + "\n" + sexo + "\n" + nascimento + "\n" + cep + "\n" + endereco + "\n" + bairro + "\n" + celular + "\n" + cpf + "\n" + str(dias) + "\n" + horario + "\n" + valor + "\n" + str(vencimento) + "\n" + str(termo))


newAluna = Aluna("Maria Eduarda", "Duda", "F", "21/10/2005", "86800-014", "Rua Munhoz da Rocha, 1527", "Centro", "43998710567", "11734664959", 2, "19:30", "200.00", 10, 1)