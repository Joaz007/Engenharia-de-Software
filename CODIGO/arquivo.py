import re

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

#criando classe academia para poder usar o singleton 
class Academia: 
    _instance = None #p deixar a instancia unica (SINGLETON)

    def __new__(cls):
        if cls._instance is None: 
            cls._instance = super(Academia, cls).__new__(cls)
            cls._instance.alunas = []
            cls._instance.horarios = {}
        return cls._instance
    
    def limiteHorario(self, horario):
        hora, minuto = map(int, horario.split(":"))
        if 6 <= hora < 12: #turno da manha 
            return 10
        elif (hora == 14 and minuto >= 30) or (15 <= hora < 18) or (hora == 18 and minuto <= 30):
            return 7
        elif (hora == 18 and minuto > 30) or (19 <= hora <= 21):
            return 10 
        else: 
            return 0
    
    def addAlunas(self, aluna):
        horario = aluna.horario
        limite = self.limiteHorario(horario)

        if limite == 0:
            print(f"o horario {horario} não é válido.")
            return
        
        if horario not in self.horarios:
            self.horarios[horario] = []

        if len(self.horarios[horario]) >= limite:
            print(f"O horario {horario} ja atingiu o limite de {limite} alunas.")
            return

        self.alunas.append(aluna)
        print(f"A aluna {aluna.nome} foi cadastrada com sucesso.")

    def listaAlunas(self):
        print("\n=== ALUNAS ===")
        if not self.alunas:
            print("nenhuma aluna cadastrada.")
            return
        for i, aluna in enumerate(self.alunas, start = 1):
            print(f"{i}. {aluna.nome} ({aluna.horario})")

    def mostraVagas(self):
        print("\n === VAGAS POR HORARIO ===")
        if not self.horarios: 
            print("nenhum horário registrado ainda.")
            return
        
        for h, alunas in sorted(self.horarios.items()):
            limite = self.limiteHorario(h)
            vagasRestantes = limite - len(alunas)
            print(f"{h}: {len(alunas)}/{limite} alunas ({vagasRestantes} vagas disponiveis)")

def InserirInfosAlunas():
    print("==== CADASTRO DE ALUNA ==== \n")

    nome = input("Insira o nome completo da aluna:\n").strip()
    apelido = input("Apelido:\n").strip()

    while True:
        sexo = input("Sexo (F/M):\n").strip()
        if sexo in ["F", "M", "f", "m"]:
            break
        print("Por favor, insira uma resposta válida (F ou M).")

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

    while True: 
        horario = input("Horário da aula: (exemplo: 06:00)\n").strip()
        if re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", horario):
            break
        print("por favor, insira um horário no formato HH:MM.")

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

    while True: 
        termo_input = input("O termo de responsabilidade foi assinado? (S/N):\n").strip()
        if termo_input in ["S", "N", "s", "n"]:
            termo = termo_input.upper() == "S"
            break 
        print("Por favor, insira uma resposta válida (S ou N)")

    if not termo:
        print("\nO termo não foi assinado. O cadastro não pôde ser concluído.\n")
        return None

    nova_aluna = Aluna(
        nome, apelido, sexo, nascimento, cep, endereco, bairro,
        celular, cpf, dias, horario, valor, vencimento, termo
    )

    print("\nCadastro realizado com sucesso!\n")
    return nova_aluna

def main():
    academia = Academia()

    while True:
        print("\n=== MENU ===\n")
        print("1 - Cadastrar aluna")
        print("2 - Listar alunas cadastradas")
        print("3 - Sair")

        opcao = input("\nO que deseja fazer?\n").strip()

        if opcao == "1": 
            aluna = InserirInfosAlunas()
            if aluna:
                academia.addAlunas(aluna)
        elif opcao == "2": 
            academia.listaAlunas()
        elif opcao == "3":
            print("Saindo do sistema!")
            break
        else: 
            print("Opcao invalida.")

if __name__ == "__main__":
    main()