import re
import json 
import os

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

    def __repr__(self):
        return f"<Aluna {self.nome} {self.horario}>"
    
    def converteDic(self):
        return self.__dict__
    
    def instanciaDic(data):
        return Aluna(**data)

# Singleton Academia
class Academia:
    _instance = None
    ARQUIVO = "academia.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Academia, cls).__new__(cls)
            cls._instance.alunas = []
            cls._instance.horarios = {
                "segunda": {}, "terca": {}, "quarta": {}, "quinta": {}, "sexta": {}
            }
        return cls._instance

    def limiteHorario(self, horario):
        hora, minuto = map(int, horario.split(":"))
        # manhã 06:00 - 11:59
        if 6 <= hora < 12:
            return 10
        # tarde 14:30 - 18:30
        elif (hora == 14 and minuto >= 30) or (15 <= hora < 18) or (hora == 18 and minuto <= 30):
            return 7
        # noite 18:31 - 21:00
        elif (hora == 18 and minuto > 30) or (19 <= hora <= 21):
            return 10
        else:
            return 0
        
    def salvaDados(self):
        dados = {"alunas": [a.converteDic() for a in self.alunas], 
                 "horarios": {dia: {h: [aluna.cpf for aluna in lista] for h, lista in horarios.items()} for dia, horarios in self.horarios.items()}}
        
        with open(self.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii = False, indent = 4)

    def carregaDados(self):
        if not os.path.exists(self.ARQUIVO):
            return
        
        with open(self.ARQUIVO, "r", encoding = "utf-8") as f:
            dados = json.load(f)

        self.alunas = [Aluna.instanciaDic(d) for d in dados.get("alunas", [])]

        cpfAluna = {a.cpf: a for a in self.alunas}
        self.horarios = {dia: {} for dia in ["segunda", "terca", "quarta", "quinta", "sexta"]}

        for dia, horarios in dados.get("horarios", {}).items():
            for h, cpfs in horarios.items():
                self.horarios[dia][h] = [cpfAluna[c] for c in cpfs if c in cpfAluna]

    def addAlunas(self, aluna, dia):
        dia = dia.lower()
        horario = aluna.horario

        if dia not in self.horarios:
            print("Dia inválido. Insira segunda, terca, quarta, quinta ou sexta.")
            return

        limite = self.limiteHorario(horario)
        if limite == 0:
            print(f"O horário {horario} não é válido (cadastros permitidos entre 06:00 e 21:00).")
            return

        # cria a lista do horário no dia se ainda não existir
        if horario not in self.horarios[dia]:
            self.horarios[dia][horario] = []

        if len(self.horarios[dia][horario]) >= limite:
            print(f"O horário {horario} de {dia} já atingiu o limite de {limite} alunas.")
            return

        # adiciona à lista geral e à lista do dia/horário
        self.alunas.append(aluna)
        self.horarios[dia][horario].append(aluna)
        self.salvaDados()

        print(f"A aluna {aluna.nome} foi cadastrada em {dia} às {horario} com sucesso.")

    def listaAlunas(self):
        print("\n=== ALUNAS ===")
        if not self.alunas:
            print("Nenhuma aluna cadastrada.")
            return
        for i, aluna in enumerate(self.alunas, start=1):
            print(f"{i}. {aluna.nome} ({aluna.horario})")

    def mostraVagas(self):
        print("\n=== VAGAS POR HORÁRIO ===")
        for dia, horarios in self.horarios.items():
            print(f"\n{dia.capitalize()}:")
            if not horarios:
                print("  Nenhum horário cadastrado ainda.")
                continue
            # ordenar pelas chaves (horário)
            for h, alunas in sorted(horarios.items(), key=lambda x: x[0]):
                limite = self.limiteHorario(h)
                vagasRestantes = limite - len(alunas)
                print(f"  {h}: {len(alunas)}/{limite} alunas ({vagasRestantes} vagas disponíveis)")

def InserirInfosAlunas():
    print("==== CADASTRO DE ALUNA ==== \n")

    nome = input("Insira o nome completo da aluna:\n").strip()
    apelido = input("Apelido:\n").strip()

    while True:
        sexo = input("Sexo (F/M):\n").strip().upper()
        if sexo in ["F", "M"]:
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

    # captura e normaliza o dia antes de validar
    while True:
        dia_raw = input("Dia da aula (segunda a sexta):\n").strip().lower()
        
        dia = dia_raw.replace("ç", "c").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        if dia in ["segunda", "terca", "quarta", "quinta", "sexta"]:
            break
        print("Por favor, insira um dia válido (segunda, terca, quarta, quinta, sexta).")

    # horário no formato HH:MM
    while True:
        horario = input("Horário da aula (exemplo: 06:00):\n").strip()
        if re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", horario):
            break
        print("Por favor, insira um horário no formato HH:MM.")

    while True:
        try:
            valor = float(input("Valor da mensalidade (ex: 200.00):\n"))
            break
        except ValueError:
            print("Insira um valor válido (ex: 200.00).")

    while True:
        try:
            vencimento = int(input("Dia do vencimento (número):\n"))
            break
        except ValueError:
            print("Insira um número válido.")

    while True:
        termo_input = input("O termo de responsabilidade foi assinado? (S/N):\n").strip().upper()
        if termo_input in ["S", "N"]:
            termo = termo_input == "S"
            break
        print("Por favor, insira uma resposta válida (S ou N).")

    if not termo:
        print("\nO termo não foi assinado. O cadastro não pôde ser concluído.\n")
        return None, None

    nova_aluna = Aluna(
        nome, apelido, sexo, nascimento, cep, endereco, bairro,
        celular, cpf, dias, horario, valor, vencimento, termo
    )

    print("\nCadastro realizado com sucesso!\n")
    return nova_aluna, dia

def main():
    academia = Academia()

    while True:
        print("\n=== MENU ===\n")
        print("1 - Cadastrar aluna")
        print("2 - Listar alunas cadastradas")
        print("3 - Ver vagas por dia/horario")
        print("4 - Sair")

        opcao = input("\nO que deseja fazer?\n").strip()

        if opcao == "1":
            aluna, dia = InserirInfosAlunas()
            
            if aluna is not None:
                academia.addAlunas(aluna, dia)
        elif opcao == "2":
            academia.listaAlunas()
        elif opcao == "3":
            academia.mostraVagas()
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    main()
