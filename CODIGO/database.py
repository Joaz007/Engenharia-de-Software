import sqlite3
import os

DB_NAME = "inscricoes.db"

class Aluna:
    def __init__(self, nome, apelido, sexo, nascimento, cep, endereco, bairro,
                 celular, cpf, dias, horario, valor, vencimento, termo):
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
        return f"Aluna(nome={self.nome!r}, cpf={self.cpf!r})"

class DBManager:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._ensure_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_db(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS alunas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            apelido TEXT,
            sexo TEXT,
            data_nascimento TEXT,
            cep TEXT,
            endereco TEXT,
            bairro TEXT,
            celular TEXT,
            cpf TEXT UNIQUE,
            dias_semana INTEGER,
            horario TEXT,
            valor REAL,
            dia_vencimento INTEGER,
            termo_assinado INTEGER
        )
        ''')
        conn.commit()
        conn.close()

    def adicionar_aluna(self, aluna: Aluna):
        conn = self._connect()
        cur = conn.cursor()
        sql = '''
        INSERT INTO alunas (
            nome, apelido, sexo, data_nascimento, cep, endereco, bairro,
            celular, cpf, dias_semana, horario, valor, dia_vencimento, termo_assinado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            aluna.nome, aluna.apelido, aluna.sexo, aluna.nascimento, aluna.cep,
            aluna.endereco, aluna.bairro, aluna.celular, aluna.cpf,
            aluna.dias, aluna.horario, aluna.valor, aluna.vencimento, int(aluna.termo)
        )
        try:
            cur.execute(sql, params)
            conn.commit()
            print(f"A aluna '{aluna.nome}' foi adicionada ao banco.")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao adicionar: CPF já existente ou outro problema. ({e})")
        finally:
            conn.close()

    def listar_alunas(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, apelido, cpf, dias_semana, horario, valor, dia_vencimento, termo_assinado FROM alunas")
        rows = cur.fetchall()
        conn.close()

        if not rows:
            print("Nenhuma aluna cadastrada.")
            return

        print("\n=== ALUNAS CADASTRADAS ===")
        for r in rows:
            id_, nome, apelido, cpf, dias, horario, valor, venc, termo = r
            termo_text = "Sim" if termo else "Não"
            print(f"{id_}: {nome} ({apelido}) — CPF: {cpf} — {dias}x/sem — {horario} — R${valor:.2f} — Venc.: {venc} — Termo: {termo_text}")

def InserirInfosAlunas():
    print("==== CADASTRO DE ALUNA ==== \n")

    nome = input("Insira o nome completo da aluna:\n").strip()
    apelido = input("Apelido:\n").strip()

    while True:
        sexo = input("Sexo (F/M):\n").strip().upper()
        if sexo in ("F", "M"):
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
            print("Insira um número inteiro válido.")

    horario = input("Horário das aulas:\n").strip()

    while True:
        try:
            valor = float(input("Valor da mensalidade:\n").replace(",", "."))
            break
        except ValueError:
            print("Insira um valor numérico (ex: 200.00).")

    while True:
        try:
            vencimento = int(input("Data de vencimento da mensalidade (dia do mês):\n"))
            break
        except ValueError:
            print("Insira um número válido (1-31).")

    while True:
        termo_input = input("O termo de responsabilidade foi assinado? (S/N):\n").strip().upper()
        if termo_input in ("S", "N"):
            termo = (termo_input == "S")
            break
        print("Resposta inválida. Use S ou N.")

    if not termo:
        print("\nO termo não foi assinado. O cadastro não pôde ser concluído.\n")
        return None

    return Aluna(nome, apelido, sexo, nascimento, cep, endereco, bairro, celular, cpf, dias, horario, valor, vencimento, termo)

def main():
    db = DBManager()

    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar aluna")
        print("2 - Listar alunas cadastradas")
        print("3 - Sair")

        opcao = input("\nO que deseja fazer?\n").strip()

        if opcao == "1":
            aluna = InserirInfosAlunas()
            if aluna:
                db.adicionar_aluna(aluna)
        elif opcao == "2":
            db.listar_alunas()
        elif opcao == "3":
            print("Saindo do sistema!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
