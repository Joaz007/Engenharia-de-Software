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
        return f"<Aluna {self.nome} ({self.horario})>"
    
    def converteDic(self):
        return self.__dict__
    
    def instanciaDic(data):
        return Aluna(**data)


class Academia:
    _instance = None
    ARQUIVO = "academia.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Academia, cls).__new__(cls)
            cls._instance.alunas = []
            cls._instance.horarios = {dia: {} for dia in ["segunda", "terca", "quarta", "quinta", "sexta"]}
            cls._instance.carregaDados()
        return cls._instance

    def limiteHorario(self, horario):
        hora, minuto = map(int, horario.split(":"))
        if 6 <= hora < 12:
            return 10  # manhã
        elif (hora == 14 and minuto >= 30) or (15 <= hora < 18) or (hora == 18 and minuto <= 30):
            return 7   # tarde
        elif (hora == 18 and minuto > 30) or (19 <= hora <= 21):
            return 10  # noite
        return 0

    def salvaDados(self):
        dados = {
            "alunas": [a.converteDic() for a in self.alunas],
            "horarios": {
                dia: {h: [a.cpf for a in lista] for h, lista in horarios.items()}
                for dia, horarios in self.horarios.items()
            }
        }
        with open(self.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregaDados(self):
        if not os.path.exists(self.ARQUIVO):
            return
        with open(self.ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        self.alunas = [Aluna.instanciaDic(d) for d in dados.get("alunas", [])]
        cpfAluna = {a.cpf: a for a in self.alunas}
        self.horarios = {dia: {} for dia in ["segunda", "terca", "quarta", "quinta", "sexta"]}
        for dia, horarios in dados.get("horarios", {}).items():
            for h, cpfs in horarios.items():
                self.horarios[dia][h] = [cpfAluna[c] for c in cpfs if c in cpfAluna]

    def addAlunas(self, aluna, dia, horario):
        dia = dia.lower()
        if dia not in self.horarios:
            print("Dia inválido.")
            return
        limite = self.limiteHorario(horario)
        if limite == 0:
            print(f"Horário {horario} inválido.")
            return

        if horario not in self.horarios[dia]:
            self.horarios[dia][horario] = []

        # verifica duplicata
        if any(a.cpf == aluna.cpf for a in self.horarios[dia][horario]):
            print(f"{aluna.nome} já está cadastrada em {dia} às {horario}.")
            return

        if len(self.horarios[dia][horario]) >= limite:
            print(f"O horário {horario} de {dia} já está cheio ({limite} alunas).")
            return

        # adiciona
        self.alunas.append(aluna)
        self.horarios[dia][horario].append(aluna)
        self.salvaDados()
        print(f"{aluna.nome} cadastrada em {dia} às {horario}.")

    def listaAlunas(self):
        print("\n=== ALUNAS ===")
        if not self.alunas:
            print("Nenhuma aluna cadastrada.")
            return
        for i, a in enumerate(self.alunas, 1):
            print(f"{i}. {a.nome} ({a.horario})")

    def mostraVagas(self):
        print("\n=== VAGAS ===")
        for dia, horarios in self.horarios.items():
            print(f"\n{dia.capitalize()}:")
            if not horarios:
                print("  Nenhum horário ainda.")
                continue
            for h, alunas in sorted(horarios.items()):
                limite = self.limiteHorario(h)
                vagas = limite - len(alunas)
                print(f"  {h}: {len(alunas)}/{limite} ({vagas} vagas)")


def InserirInfosAlunas():
    print("==== CADASTRO DE ALUNA ====\n")

    nome = input("Nome completo:\n").strip()
    apelido = input("Apelido:\n").strip()

    while True:
        sexo = input("Sexo (F/M):\n").strip().upper()
        if sexo in ["F", "M"]:
            break
        print("Por favor, insira F ou M.")

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
            print("Insira um número válido.")

    horariosSemana = []
    for i in range(dias):
        print(f"\n=== Aula {i+1} de {dias} ===")
        while True:
            dia = input("Dia (segunda a sexta):\n").strip().lower()
            if dia in ["segunda", "terca", "terça", "quarta", "quinta", "sexta"]:
                dia = dia.replace("terça", "terca")
                break
            print("Dia inválido.")
        while True:
            horario = input("Horário (HH:MM):\n").strip()
            if re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", horario):
                break
            print("Formato inválido. Ex: 06:00.")
        horariosSemana.append((dia, horario))

    while True:
        try:
            valor = float(input("Valor da mensalidade:\n"))
            break
        except ValueError:
            print("Número inválido.")

    while True:
        try:
            vencimento = int(input("Dia de vencimento:\n"))
            break
        except ValueError:
            print("Número inválido.")

    while True:
        termo_input = input("Termo assinado? (S/N):\n").strip().upper()
        if termo_input in ["S", "N"]:
            termo = termo_input == "S"
            break
        print("Digite S ou N.")

    if not termo:
        print("Termo não assinado. Cadastro cancelado.")
        return None, None

    primeiroHorario = horariosSemana[0][1]

    nova_aluna = Aluna(
        nome, apelido, sexo, nascimento, cep, endereco, bairro,
        celular, cpf, dias, primeiroHorario, valor, vencimento, termo
    )

    return nova_aluna, horariosSemana


def main():
    academia = Academia()

    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar aluna")
        print("2 - Listar alunas")
        print("3 - Ver vagas")
        print("4 - Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            aluna, horarios = InserirInfosAlunas()
            if aluna:
                for dia, horario in horarios:
                    academia.addAlunas(aluna, dia, horario)
        elif opcao == "2":
            academia.listaAlunas()
        elif opcao == "3":
            academia.mostraVagas()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
