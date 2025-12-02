from abc import ABC, abstractmethod
import re
import sqlite3
import os
from typing import Optional, List, Tuple
import hashlib
import secrets

DB_PATH = "academia.db"
WEEKDAYS = ["segunda", "terca", "quarta", "quinta", "sexta"]
DDDS_VALIDOS = [
    '11', '12', '13', '14', '15', '16', '17', '18', '19', # SP
    '21', '22', '24', # RJ
    '27', '28', # ES
    '31', '32', '33', '34', '35', '37', '38', # MG
    '41', '42', '43', '44', '45', '46', # PR
    '47', '48', '49', # SC
    '51', '53', '54', '55', # RS
    '61', # DF
    '62', '64', # GO
    '63', # TO
    '65', '66', # MT
    '67', # MS
    '68', # AC
    '69', # RO
    '71', '73', '74', '75', '77', # BA
    '79', # SE
    '81', '87', # PE
    '82', # AL
    '83', # PB
    '84', # RN
    '85', '88', # CE
    '86', '89', # PI
    '91', '93', '94', # PA
    '92', '97', # AM
    '95', # RR
    '96', # AP
    '98', '99' # MA
]

# ===== Classe Usuario (simples) =====
class Usuario:
    """
    Classe simples para representar usuário com nome e senha (armazenada como hash com salt).
    """
    def __init__(self, nome: str, pwd_hash: str = None, salt: str = None):
        self.nome = (nome or "").strip()
        self.pwd_hash = pwd_hash  # hex string
        self.salt = salt          # hex string

    def set_password(self, senha: str):
        """Gera salt curto e armazena o hash SHA256(salt + senha)."""
        if senha is None:
            raise ValueError("Senha não pode ser None")
        # salt simples suficiente para uso local; para produção use PBKDF2/etc.
        self.salt = secrets.token_hex(8)  # 8 bytes -> 16 hex chars
        self.pwd_hash = hashlib.sha256((self.salt + senha).encode('utf-8')).hexdigest()

    def check_user(self, nome: str) -> bool:
        """Verifica se o user bate com o user armazenado."""
        if not (self.nome and self.pwd_hash and self.salt):
            return False
        return self.nome
    
    def check_password(self, senha: str) -> bool:
        """Verifica se a senha bate com o hash armazenado."""
        if not (self.pwd_hash and self.salt):
            return None
        tentativa = hashlib.sha256((self.salt + (senha or "")).encode('utf-8')).hexdigest()
        return self.pwd_hash

    def to_db_tuple(self) -> tuple:
        """(nome, pwd_hash, salt) - para INSERT no DB."""
        return (self.nome, self.pwd_hash, self.salt)

    @classmethod
    def from_db_row(cls, row: tuple):
        """Cria Usuário a partir de linha (id, nome, pwd_hash, salt) ou (nome,pwd_hash,salt)."""
        if not row:
            return None
        if len(row) == 4:
            _, nome, pwd_hash, salt = row
        elif len(row) == 3:
            nome, pwd_hash, salt = row
        else:
            raise ValueError("Formato de row inválido")
        return cls(nome=nome, pwd_hash=pwd_hash, salt=salt)

# ===== Classe Aluna e Builders/Strategies =====
class Aluna:
    def __init__(self, nome, apelido, nascimento, cep, endereco, bairro,
                 celular, cpf, dias, diasSemana, horario, valor, vencimento, termo):
        self.nome = nome
        self.apelido = apelido
        self.nascimento = nascimento
        self.cep = cep
        self.endereco = endereco
        self.bairro = bairro
        self.celular = celular
        self.cpf = cpf
        self.dias = dias
        self.diasSemana = diasSemana
        self.horario = horario
        self.valor = valor
        self.vencimento = vencimento
        self.termo = termo

    def __repr__(self):
        return f"Aluna(nome={self.nome!r}, cpf={self.cpf!r})"

# A classe StrategyMensalidades define a interface para estratégias de cálculo de mensalidades.
# As subclasses consideram alunas novas com 2 ou 3 vezes por semana e alunas com desconto.
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
    
# O AlunaBuilder constrói objetos Aluna passo a passo. Use o builder quando
# houver muitos campos opcionais ou quando quiser centralizar validações.
class AlunaBuilder:
    def __init__(self):
        self._data = {
            "nome": None,
            "apelido": None,
            "nascimento": None,
            "cep": None,
            "endereco": None,
            "bairro": None,
            "celular": None,
            "cpf": None,
            "dias": None,
            "diasSemana": None,
            "horario": None,
            "valor": None,
            "vencimento": None,
            "termo": None
        }

    # métodos 
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
    def diasSemana(self, v):self._data["diasSemana"] = v.split(",") if v is not None else None; return self
    def horario(self, v): self._data["horario"] = v.split(",") if v is not None else None; return self
    def valor(self, v): self._data["valor"] = float(v) if v is not None else None; return self
    def vencimento(self, v):
        try:
            self._data["vencimento"] = int(v)
        except Exception:
            self._data["vencimento"] = None
        return self
    def termo(self, v): self._data["termo"] = bool(v); return self

    def _validate(self):
        required = ["nome", "cpf", "dias", "valor", "vencimento", "termo"]
        for k in required:
            if self._data.get(k) is None:
                raise ValueError("Campo obrigatório faltando: {}".format(k))

        cpf_raw = ''.join(ch for ch in self._data["cpf"] if ch.isdigit())
        if len(cpf_raw) != 11:
            raise ValueError("CPF inválido: deve conter 11 dígitos.")
        self._data["cpf"] = cpf_raw

        if not (isinstance(self._data["dias"], int) and self._data["dias"] > 0):
            raise ValueError("Dias deve ser inteiro > 0")

        if not (isinstance(self._data["valor"], float) or isinstance(self._data["valor"], int)):
            raise ValueError("Valor inválido")

        if not (1 <= int(self._data["vencimento"]) <= 31):
            raise ValueError("Vencimento deve ser 1-31")

    def build(self):
        self._validate()
        return Aluna(
            self._data["nome"],
            self._data["apelido"],
            self._data["nascimento"],
            self._data["cep"],
            self._data["endereco"],
            self._data["bairro"],
            self._data["celular"],
            self._data["cpf"],
            self._data["dias"],
            self._data["diasSemana"],
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
# A classe Academia implementa Singleton: o atributo _instance e o método __new__
# asseguram que apenas UMA instância da classe exista durante a execução.
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
            cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
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

    def addAlunas(self, aluna: Aluna):
        aluna.diasSemana = [d.strip().lower() for d in aluna.diasSemana]
        aluna.horario = [h.strip() for h in aluna.horario]
        
        for dia, horario in zip(aluna.diasSemana, aluna.horario):
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
                        aluna.cpf, aluna.dias, horario, aluna.valor,
                        aluna.vencimento, int(aluna.termo)
                    ))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass

                cur.execute('''
                SELECT 1 FROM horarios WHERE dia = ? AND horario = ? AND aluna_cpf = ?
                ''', (dia, horario, aluna.cpf))
                if cur.fetchone():
                    return(f"{aluna.nome} já está cadastrada em {dia} às {horario}.")
                    
                cur.execute('''
                SELECT COUNT(*) FROM horarios WHERE dia = ? AND horario = ?
                ''', (dia, horario))
                count = cur.fetchone()[0]
                if count >= self.limiteHorario(horario):
                    return(f"O horário {horario} de {dia} já está cheio ({self.limiteHorario(horario)} alunas).")

                cur.execute('''
                INSERT INTO horarios (dia, horario, aluna_cpf) VALUES (?, ?, ?)
                ''', (dia, horario, aluna.cpf))
                conn.commit()

        return(f"{aluna.nome} cadastrada nos horários com sucesso.")

    def listaAlunas(self, cpf) -> List[Tuple]:
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('''
            SELECT * FROM alunas WHERE cpf = ?''', (cpf_limpo,))
            rows = cur.fetchall()

        if not rows:
            return None
        else:
            return rows
    
    def mostraVagas(self, dia: str) -> List[Tuple[int, int, int, int, int]]:
        lista_de_vagas: List[Tuple[int, int, int, int, int]] = []
    
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('''SELECT DISTINCT horario FROM horarios WHERE dia = ?''', (dia,))
            horarios = [row[0] for row in cur.fetchall()]
            
            if not horarios:
                return []
            else:
                for h in sorted(horarios):
                    cur.execute('SELECT COUNT(*) FROM horarios WHERE dia = ? AND horario = ?', (dia, h))
                    ocupado = cur.fetchone()[0]
                    limite = self.limiteHorario(h)
                    
                    if limite == 0:
                        continue 
                    vagas = max(limite - ocupado, 0)
                    vaga_atual = (h, ocupado, limite, vagas)
                    lista_de_vagas.append(vaga_atual)
                    
                return lista_de_vagas
            
    def excluirAluna(self, cpf: str):
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        with self._connect() as conn:
            cur = conn.cursor()
            #verificando se a aluna existe
            cur.execute("SELECT cpf FROM alunas WHERE cpf = ?", (cpf_limpo,))
            row = cur.fetchone()

            if not row:
                return False
            
            #excluindooo
            cur.execute("DELETE FROM alunas WHERE cpf = ?", (cpf_limpo,))
            conn.commit()

        return True
    
    def editarAluna(self, cpf: str, **novos_dados):
        cpf_limpo = ''.join(filter(str.isdigit, cpf))

        with self._connect() as conn: 
            cur = conn.cursor()

            cur.execute("SELECT * FROM alunas WHERE cpf = ?", (cpf_limpo,))
            row = cur.fetchone()

            if not row:
                return "Aluna não encontrada."
            
            #atualizando a tabela de alunas 
            campos_validos = {"nome", "apelido", "nascimento", "cep", "endereco", "bairro",
                              "celular", "dias", "valor", "vencimento", "termo"}
            
            updates = []
            valores = []

            for campo, valor in novos_dados.items():
                if campo in campos_validos:
                    updates.append(f"{campo} = ?")
                    valores.append(valor)

            if updates:
                sql = f"UPDATE alunas SET {', '.join(updates)} WHERE cpf = ?"
                valores.append(cpf_limpo)
                cur.execute(sql, valores)
                conn.commit()
            
            #atualizando os dias e horarios 
            diasSemana = novos_dados.get("diasSemana")
            horarios = novos_dados.get("horario")

            if diasSemana and horarios: 
                diasSemana = [d.strip().lower() for d in diasSemana]
                horarios = [h.strip() for h in horarios]

                if len(diasSemana) != len(horarios):
                    return "Quantidade de dias e horarios nao coincide."
                
                cur.execute("SELECT dia, horario FROM horarios WHERE aluna_cpf = ?", (cpf_limpo,))
                horarios_antigos = cur.fetchall()

                #apagando os horarios atuais
                cur.execute("DELETE FROM horarios WHERE aluna_cpf = ?", (cpf_limpo,))
                conn.commit()

                for d, h in zip(diasSemana, horarios):
                    cur.execute("SELECT COUNT(*) FROM horarios WHERE dia = ? AND horario = ?", (d, h))
                    ocupados = cur.fetchone()[0]

                    limite = self.limiteHorario(h)

                    if ocupados >= limite:
                        #volta os horarios antigos se der ruim
                        for da, ho in horarios_antigos:
                            cur.execute("INSERT INTO horarios (dia, horario, aluna_cpf) VALUES (?, ?, ?)", (da, ho, cpf_limpo))
                            conn.commit()
                            return f"O horário {h} de {d} ja esta cheio ({limite} alunas)."

                for d, h in zip(diasSemana, horarios):
                    cur.execute("INSERT INTO horarios (dia, horario, aluna_cpf) VALUES (?, ?, ?)", (d, h, cpf_limpo))
                    conn.commit()        
        
        return "Dados da aluna atualizados com sucesso."
    
    def buscarPorNome_ou_Cpf(self, info_parcial: str):
        info_parcial = f"%{info_parcial.lower()}%"
            
        with self._connect() as conn:
            cur = conn.cursor()
            if info_parcial.replace("%", "").isdigit():
                cur.execute(""" SELECT nome, cpf, nascimento, valor, vencimento FROM alunas WHERE LOWER(cpf) LIKE ? ORDER BY nome """, (info_parcial,))
            else:
                cur.execute(""" SELECT nome, cpf, nascimento, valor, vencimento FROM alunas WHERE LOWER(nome) LIKE ? ORDER BY nome """, (info_parcial,))
            alunas = cur.fetchall()

            if not alunas:
                return None
            
        return alunas
    
    def aniversariantesMes(self, mes: int):        
        mes_str = f"{mes:02d}" #eh pra 01, 02 etc ser valido tb

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(""" SELECT nome, nascimento FROM alunas WHERE substr(nascimento, 4, 2) = ? ORDER BY nascimento """, (mes_str,))
            rows = cur.fetchall()

            if not rows:
                return None
            
        return rows
    
    # ===== Métodos simples de gerenciamento de usuários =====
    def add_usuario_simples(self, usuario: Usuario) -> bool:
        """
        Tenta inserir usuário. Retorna True se inseriu com sucesso, False se nome já existe.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            try:
                cur.execute('''
                    INSERT INTO usuarios (nome, pwd_hash, salt) VALUES (?, ?, ?)
                ''', usuario.to_db_tuple())
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def autenticar_usuario_simples(self, nome: str, senha: str) -> Optional[Usuario]:
        """
        Retorna Usuario se autenticação OK, senão None.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT nome, pwd_hash, salt FROM usuarios WHERE nome = ?', (nome,))
            row = cur.fetchone()
            if not row:
                return False
            user = Usuario.from_db_row(row)
            if user and user.check_password(senha):
                return True
            return False
        
    def listaUsuarios(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, nome FROM usuarios ORDER BY nome')
            rows = cur.fetchall()
        if not rows:
            print("Nenhum usuário cadastrado.")
            return
        print("\n=== USUÁRIOS ===")
        for r in rows:
            uid, nome = r
            print(f"{uid} - {nome}")
            
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
    return True

def validar_data(data: str):
    pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
    if not re.match(pattern, data):
        return False

    dia, mes, ano = map(int, data.split('/'))
    if mes == 2:
        if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
            if dia > 29:
                return False
        else:
            if dia > 28:
                return False
    elif mes in {4, 6, 9, 11}:
        if dia > 30:
            return False
        return True
    else:
        if dia > 31:
            return False
        return True                      

def validar_telefone(telefone: str):
    telefone = ''.join(ch for ch in telefone if ch.isdigit())
    if len(telefone) != 11:
        return False
    
    ddd = telefone[:2]
    if ddd not in DDDS_VALIDOS:
        return False

    padrao_celular = re.compile(r'^\d{2}9\d{8}$')
    if padrao_celular.match(telefone):
        return True
    else:
        return False
    
def InserirInfosAlunas(nome, apelido, nascimento, cep, endereco, bairro, celular, cpf, quantdias, dias, horario, valor, vencimento, termo):
    # Usa o AlunaBuilder para criar a instância 
    try:
        builder = AlunaBuilder() \
            .nome(nome) \
            .apelido(apelido) \
            .nascimento(nascimento) \
            .cep(cep) \
            .endereco(endereco) \
            .bairro(bairro) \
            .celular(celular) \
            .cpf(cpf) \
            .dias(quantdias) \
            .diasSemana(dias) \
            .horario(horario) \
            .valor(valor) \
            .vencimento(vencimento) \
            .termo(termo) \

        nova_aluna = builder.build()
    except ValueError as e:
        print("Erro no cadastro:", e)
        return None
    
    return nova_aluna

def main():
    academia = Academia()
    novaAluna = AlunaBuilder()
    #tirei a função de exibir a interface pra vc codar no terminal tá

if __name__ == "__main__":
    main()
    