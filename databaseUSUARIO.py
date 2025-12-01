from abc import ABC, abstractmethod
import re
import sqlite3
import os
from typing import Optional, List, Tuple
import hashlib
import secrets

DB_PATH = "academia.db"
WEEKDAYS = ["segunda", "terca", "quarta", "quinta", "sexta"]

# ===== Classe Usuario (simples) =====
class Usuario:
    """
    Classe simples para representar usuário com nome, email e senha (armazenada como hash com salt).
    Uso: u = Usuario("Nome", "email"); u.set_password("senha"); academia.add_usuario_simples(u)
    """
    def __init__(self, nome: str, email: str, pwd_hash: str = None, salt: str = None):
        self.nome = (nome or "").strip()
        self.email = (email or "").strip().lower()
        self.pwd_hash = pwd_hash  # hex string
        self.salt = salt          # hex string

    def set_password(self, senha: str):
        """Gera salt curto e armazena o hash SHA256(salt + senha)."""
        if senha is None:
            raise ValueError("Senha não pode ser None")
        # salt simples suficiente para uso local; para produção use PBKDF2/etc.
        self.salt = secrets.token_hex(8)  # 8 bytes -> 16 hex chars
        self.pwd_hash = hashlib.sha256((self.salt + senha).encode('utf-8')).hexdigest()

    def check_password(self, senha: str) -> bool:
        """Verifica se a senha bate com o hash armazenado."""
        if not (self.pwd_hash and self.salt):
            return False
        tentativa = hashlib.sha256((self.salt + (senha or "")).encode('utf-8')).hexdigest()
        return tentativa == self.pwd_hash

    def to_db_tuple(self) -> tuple:
        """(nome, email, pwd_hash, salt) - para INSERT no DB."""
        return (self.nome, self.email, self.pwd_hash, self.salt)

    @classmethod
    def from_db_row(cls, row: tuple):
        """Cria Usuário a partir de linha (id, nome, email, pwd_hash, salt) ou (nome,email,pwd_hash,salt)."""
        if not row:
            return None
        if len(row) == 5:
            _, nome, email, pwd_hash, salt = row
        elif len(row) == 4:
            nome, email, pwd_hash, salt = row
        else:
            raise ValueError("Formato de row inválido")
        return cls(nome=nome, email=email, pwd_hash=pwd_hash, salt=salt)

# ===== Classe Aluna e Builders/Strategies (mantive sua lógica) =====
class Aluna:
    def __init__(self, nova, nome, apelido, nascimento, cep, endereco, bairro,
                 celular, cpf, dias, horario, valor, vencimento, termo):
        self.nova = nova
        self.nome = nome
        self.apelido = apelido
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

class StrategyMensalidades(ABC):
    @abstractmethod
    def valorMensalidade(self) -> float:
        pass

class AlunaNova3x(StrategyMensalidades):
    def valorMensalidade(self) -> float:
        return 230.00

class AlunaNova2x(StrategyMensalidades):
    def valorMensalidade(self) -> float:
        return 200.00

class AlunaComDesc(StrategyMensalidades):
    def valorMensalidade(self) -> float:
        return 0.00

class AlunaBuilder:
    def __init__(self):
        self._data = {
            "nova": None,
            "nome": None,
            "apelido": None,
            "nascimento": None,
            "cep": None,
            "endereco": None,
            "bairro": None,
            "celular": None,
            "cpf": None,
            "dias": None,
            "horario": None,
            "valor": None,
            "vencimento": None,
            "termo": None
        }

    # métodos 
    def nova(self, v): self._data["nova"] = bool(v); return self
    def nome(self, v): self._data["nome"] = v.strip() if v is not None else None; return self
    def apelido(self, v): self._data["apelido"] = v.strip() if v is not None else None; return self
    def nascimento(self, v): self._data["nascimento"] = v.strip() if v is not None else None; return self
    def cep(self, v): self._data["cep"] = v.strip() if v is not None else None; return self
    def endereco(self, v): self._data["endereco"] = v.strip() if v is not None else None; return self
    def bairro(self, v): self._data["bairro"] = v.strip() if v is not None else None; return self
    def celular(self, v): self._data["celular"] = v.strip() if v is not None else None; return self
    def cpf(self, v): self._data["cpf"] = v.strip() if v is not None else None; return self
    def dias(self, v):
        try:
            self._data["dias"] = int(v)
        except Exception:
            self._data["dias"] = None
        return self
    def horario(self, v): self._data["horario"] = v.strip() if v is not None else None; return self
    def valor(self, v):
        try:
            if not self._data["nova"]:
                self._data["valor"] = AlunaComDesc().valorMensalidade()
            elif  self._data["dias"] == 2:
                self._data["valor"] = AlunaNova2x().valorMensalidade()
            elif self._data["dias"] == 3:
                self._data["valor"] = AlunaNova3x().valorMensalidade()
        except Exception:
            self._data["valor"] = None
        return self
    def vencimento(self, v):
        try:
            self._data["vencimento"] = int(v)
        except Exception:
            self._data["vencimento"] = None
        return self
    def termo(self, v): self._data["termo"] = bool(v); return self

    def _validate(self):
        required = ["nome", "cpf", "dias", "horario", "valor", "vencimento", "termo"]
        for k in required:
            if self._data.get(k) is None:
                raise ValueError("Campo obrigatório faltando: {}".format(k))

        cpf_raw = ''.join(ch for ch in self._data["cpf"] if ch.isdigit())
        if len(cpf_raw) != 11:
            raise ValueError("CPF inválido: deve conter 11 dígitos.")
        self._data["cpf"] = cpf_raw

        if not re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", self._data["horario"]):
            raise ValueError("Formato de horário inválido. Use HH:MM")

        if not (isinstance(self._data["dias"], int) and self._data["dias"] > 0):
            raise ValueError("Dias deve ser inteiro > 0")

        if not (isinstance(self._data["valor"], float) or isinstance(self._data["valor"], int)):
            raise ValueError("Valor inválido")

        if not (1 <= int(self._data["vencimento"]) <= 31):
            raise ValueError("Vencimento deve ser 1-31")

    def build(self):
        self._validate()
        return Aluna(
            self._data["nova"],
            self._data["nome"],
            self._data["apelido"],
            self._data["nascimento"],
            self._data["cep"],
            self._data["endereco"],
            self._data["bairro"],
            self._data["celular"],
            self._data["cpf"],
            self._data["dias"],
            self._data["horario"],
            self._data["valor"],
            self._data["vencimento"],
            self._data["termo"]
        )

    def from_dict(cls, d):
        b = AlunaBuilder()
        for k, v in d.items():
            if k in b._data:
                b._data[k] = v
        return b

# ===== Classe Academia (Singleton) com integração de usuarios =====
class Academia:
    _instance = None

    def __new__(cls, db_path: str = DB_PATH):
        if cls._instance is None:
            cls._instance = super(Academia, cls).__new__(cls)
            cls._instance.db_path = db_path
            cls._instance._ensure_db()
        return cls._instance

    def _connect(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _ensure_db(self):
        # cria tabelas se não existirem
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS alunas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                apelido TEXT,
                nascimento TEXT,
                cep TEXT,
                endereco TEXT,
                bairro TEXT,
                celular TEXT,
                cpf TEXT UNIQUE,
                dias INTEGER,
                horario TEXT,
                valor REAL,
                vencimento INTEGER,
                termo INTEGER
            )
            ''')
            cur.execute('''
            CREATE TABLE IF NOT EXISTS horarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia TEXT NOT NULL,
                horario TEXT NOT NULL,
                aluna_cpf TEXT NOT NULL,
                FOREIGN KEY(aluna_cpf) REFERENCES alunas(cpf) ON DELETE CASCADE
            )
            ''')
            # tabela simples de usuarios (para login)
            cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                pwd_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
            ''')
            conn.commit()

    def limiteHorario(self, horario: str) -> int:
        hora, minuto = map(int, horario.split(":"))
        if 6 <= hora < 12:
            return 10
        elif (hora == 14 and minuto >= 30) or (15 <= hora < 18) or (hora == 18 and minuto <= 30):
            return 7
        elif (hora == 18 and minuto > 30) or (19 <= hora <= 21):
            return 10
        return 0

    def addAlunas(self, aluna: Aluna, dia: str, horario: str):
        dia = dia.lower()
        if dia not in WEEKDAYS:
            print("Dia inválido.")
            return

        limite = self.limiteHorario(horario)
        if limite == 0:
            print(f"Horário {horario} inválido.")
            return

        with self._connect() as conn:
            cur = conn.cursor()
            # insere aluna se não existir (cpf UNIQUE evita duplicata)
            try:
                cur.execute('''
                INSERT INTO alunas (
                    nome, apelido, nascimento, cep, endereco, bairro,
                    celular, cpf, dias, horario, valor, vencimento, termo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    aluna.nome, aluna.apelido, aluna.nascimento,
                    aluna.cep, aluna.endereco, aluna.bairro, aluna.celular,
                    aluna.cpf, aluna.dias, aluna.horario, aluna.valor,
                    aluna.vencimento, int(aluna.termo)
                ))
                conn.commit()
            except sqlite3.IntegrityError:
                # já existe aluna com esse CPF; continuamos (pode ser apenas hora extra)
                pass

            cur.execute('''
            SELECT 1 FROM horarios WHERE dia = ? AND horario = ? AND aluna_cpf = ?
            ''', (dia, horario, aluna.cpf))
            if cur.fetchone():
                print(f"{aluna.nome} já está cadastrada em {dia} às {horario}.")
                return

            cur.execute('''
            SELECT COUNT(*) FROM horarios WHERE dia = ? AND horario = ?
            ''', (dia, horario))
            count = cur.fetchone()[0]
            if count >= limite:
                print(f"O horário {horario} de {dia} já está cheio ({limite} alunas).")
                return

            cur.execute('''
            INSERT INTO horarios (dia, horario, aluna_cpf) VALUES (?, ?, ?)
            ''', (dia, horario, aluna.cpf))
            conn.commit()

            print(f"{aluna.nome} cadastrada em {dia} às {horario}.")

    def listaAlunas(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('''
            SELECT nome, apelido, cpf, dias, horario, valor, vencimento, termo FROM alunas ORDER BY nome
            ''')
            rows = cur.fetchall()

        if not rows:
            print("Nenhuma aluna cadastrada.")
            return

        print("\n=== ALUNAS ===")
        for i, r in enumerate(rows, start=1):
            nome, apelido, cpf, dias, horario, valor, vencimento, termo = r
            termo_text = "Sim" if termo else "Não"
            print(f"{i}. {nome} ({apelido}) — CPF: {cpf} — {dias}x/sem — {horario} — R${valor:.2f} — Venc.: {vencimento} — Termo: {termo_text}")

    def mostraVagas(self):
        with self._connect() as conn:
            cur = conn.cursor()
            print("\n=== VAGAS ===")
            for dia in WEEKDAYS:
                print(f"\n{dia.capitalize()}:")
                cur.execute('''SELECT DISTINCT horario FROM horarios WHERE dia = ?''', (dia,))
                horarios = [row[0] for row in cur.fetchall()]
                if not horarios:
                    print("  Todos os horários estão disponíveis.")
                    continue

                for h in sorted(horarios):
                    cur.execute('SELECT COUNT(*) FROM horarios WHERE dia = ? AND horario = ?', (dia, h))
                    ocupado = cur.fetchone()[0]
                    limite = self.limiteHorario(h)
                    vagas = max(limite - ocupado, 0)
                    print(f"  {h}: {ocupado}/{limite} ({vagas} vagas)")

    # ===== Métodos simples de gerenciamento de usuários =====
    def add_usuario_simples(self, usuario: Usuario) -> bool:
        """
        Tenta inserir usuário. Retorna True se inseriu com sucesso, False se email já existe.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            try:
                cur.execute('''
                    INSERT INTO usuarios (nome, email, pwd_hash, salt) VALUES (?, ?, ?, ?)
                ''', usuario.to_db_tuple())
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def autenticar_usuario_simples(self, email: str, senha: str) -> Optional[Usuario]:
        """
        Retorna Usuario se autenticação OK, senão None.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT nome, email, pwd_hash, salt FROM usuarios WHERE email = ?', (email.lower(),))
            row = cur.fetchone()
            if not row:
                return None
            user = Usuario.from_db_row(row)
            if user and user.check_password(senha):
                return user
            return None

    def listaUsuarios(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, nome, email FROM usuarios ORDER BY nome')
            rows = cur.fetchall()
        if not rows:
            print("Nenhum usuário cadastrado.")
            return
        print("\n=== USUÁRIOS ===")
        for r in rows:
            uid, nome, email = r
            print(f"{uid}. {nome} — {email}")

# ===== Validação CPF e interface de inserção de alunas =====
def validar_cpf(cpf: str):
    cpf_digits = ''.join(ch for ch in cpf if ch.isdigit())
    if len(cpf_digits) != 11:
        return False
    if cpf_digits == cpf_digits[0] * 11:
        return False
    nums = [int(c) for c in cpf_digits]
    s = sum(nums[i] * (10 - i) for i in range(9))
    r = s % 11
    dv1 = 0 if r < 2 else 11 - r
    if dv1 != nums[9]:
        return False
    s2 = sum(nums[i] * (11 - i) for i in range(10))
    r2 = s2 % 11
    dv2 = 0 if r2 < 2 else 11 - r2
    if dv2 != nums[10]:
        return False
    return cpf_digits

def InserirInfosAlunas() -> Optional[Tuple[Aluna, List[Tuple[str, str]]]]:
    print("==== CADASTRO DE ALUNA ====")

    nome = input("Nome completo:\n").strip()
    apelido = input("Apelido:\n").strip()
    nova = bool(input("Aluna sem desconto? (S/N):\n").strip().upper() == "S")
    
    while True:
        nascimento = input("Data de nascimento (dd/mm/aaaa):\n").strip()
        if re.match(r"^\d{2}/\d{2}/\d{4}$", nascimento):
            break
        print("Data inválida. Formato: dd/mm/aaaa")

    while True:
        cep = input("CEP (00000-000):\n").strip()
        if re.match(r"^\d{5}-\d{3}$", cep):
            break   
        print("CEP inválido. Formato: 00000-000")
        
    endereco = input("Endereço:\n").strip()
    bairro = input("Bairro:\n").strip()
    celular = input("Celular:\n").strip()

    while True:
        cpf_input = input("CPF:\n").strip()
        cpf_valid = validar_cpf(cpf_input)
        if cpf_valid:
            cpf = cpf_valid
            break
        print("CPF inválido. Digite novamente.")

    while True:
        try:
            dias = int(input("Quantas vezes por semana?\n"))
            break
        except ValueError:
            print("Insira um número válido.")

    horariosSemana: List[Tuple[str, str]] = []
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
                pass
            else:
                print("Formato inválido. Ex: 06:00.")
                continue
            hora, minuto = map(int, horario.split(":"))

            if dia == "segunda" or dia == "quarta":
                if (hora >= 6 and minuto == 0) and (hora <= 9 and minuto == 0):
                    break
                elif (hora == 11 and minuto == 0) or (hora == 11 and minuto == 30):
                    break
                elif (hora >= 14 and minuto == 30) and (hora <= 19 and minuto == 30):
                    break
            elif dia == "terca" or dia == "quinta":
                if (hora >= 6 and minuto == 0) and (hora <= 9 and minuto == 0):
                    break
                elif (hora >= 15 and minuto >= 30) and (hora <= 19 and minuto == 30):
                    break
            elif dia == "sexta":
                if (hora >= 6 and minuto == 0) and (hora <= 9 and minuto == 0):
                    break
                elif (hora == 11 and minuto == 0) or (hora == 11 and minuto == 30):
                    break
                elif (hora >= 14 and minuto == 30) and (hora <= 18 and minuto == 30):
                    break
            print("Horário indisponível para o dia escolhido.")
        horariosSemana.append((dia, horario))

    while True:
        try:
            if not nova:
                valor = float(input("Valor da mensalidade:\n").replace(",", "."))
            elif dias == 2:
                valor = AlunaNova2x().valorMensalidade()
            elif dias == 3:
                valor = AlunaNova3x().valorMensalidade()
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
        return None

    primeiroHorario = horariosSemana[0][1]

    # Usa o AlunaBuilder para criar a instância 
    try:
        builder = AlunaBuilder() \
            .nova(nova) \
            .nome(nome) \
            .apelido(apelido) \
            .nascimento(nascimento) \
            .cep(cep) \
            .endereco(endereco) \
            .bairro(bairro) \
            .celular(celular) \
            .cpf(cpf) \
            .dias(dias) \
            .horario(primeiroHorario) \
            .valor(valor) \
            .vencimento(vencimento) \
            .termo(termo)

        nova_aluna = builder.build()
    except ValueError as e:
        print("Erro no cadastro:", e)
        return None

    return nova_aluna, horariosSemana

# ===== Helpers CLI para usuário =====
def register_user_cli(academia: Academia):
    print("=== Registrar usuário ===")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()
    if not nome or not email or not senha:
        print("Preencha todos os campos.")
        return
    u = Usuario(nome, email)
    try:
        u.set_password(senha)
    except ValueError as e:
        print("Erro:", e); return
    if academia.add_usuario_simples(u):
        print("Usuário criado:", u.email)
    else:
        print("E-mail já cadastrado.")

def login_cli(academia: Academia) -> Optional[Usuario]:
    print("=== Login ===")
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()
    user = academia.autenticar_usuario_simples(email, senha)
    if user:
        print(f"Logado como: {user.nome} ({user.email})")
        return user
    else:
        print("E-mail ou senha incorretos.")
        return None

# ===== Main (menu) =====
def main():
    academia = Academia()
    logged_user: Optional[Usuario] = None

    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar aluna")
        print("2 - Listar alunas")
        print("3 - Ver vagas")
        print("4 - Registrar usuário")
        print("5 - Login usuário")
        print("6 - Listar usuários")
        print("7 - Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            # exigir login opcional? por enquanto não exige; se quiser, peça login
            result = InserirInfosAlunas()
            if result:
                aluna, horarios = result
                for dia, horario in horarios:
                    academia.addAlunas(aluna, dia, horario)
        elif opcao == "2":
            academia.listaAlunas()
        elif opcao == "3":
            academia.mostraVagas()
        elif opcao == "4":
            register_user_cli(academia)
        elif opcao == "5":
            logged_user = login_cli(academia)
        elif opcao == "6":
            academia.listaUsuarios()
        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
