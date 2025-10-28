from abc import ABC, abstractmethod
import re
import sqlite3
import os
from typing import Optional, List, Tuple
import interface as ctk
DB_PATH = "academia.db"
WEEKDAYS = ["segunda", "terca", "quarta", "quinta", "sexta"]

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

    def listaAlunas(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('''
            SELECT nome, apelido, cpf, dias, horario, valor, vencimento FROM alunas ORDER BY nome
            ''')
            rows = cur.fetchall()

        if not rows:
            return("Nenhuma aluna cadastrada.")
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

def verificaHorarios(dia: str, horario: str) -> bool:
    hora, minuto = map(int, horario.split(":"))
    
    if dia == "segunda" or dia == "quarta":
        if (hora >= 6 and minuto == 0) and (hora <= 9 and minuto == 0):
            return True
        elif (hora == 11 and minuto == 0) or (hora == 11 and minuto == 30):
            return True
        elif (hora >= 14 and minuto == 30) and (hora <= 19 and minuto == 30):
            return True
    elif dia == "terca" or dia == "terça" or dia == "quinta":
        if (hora >= 6 and minuto == 0) and (hora <= 9 and minuto == 0):
            return True
        elif (hora >= 15 and minuto >= 30) and (hora <= 19 and minuto == 30):
            return True
    elif dia == "sexta":
        if (hora >= 6 and minuto == 0) and (hora <= 9 and minuto == 0):
            return True
        elif (hora == 11 and minuto == 0) or (hora == 11 and minuto == 30):
            return True
        elif (hora >= 14 and minuto == 30) and (hora <= 18 and minuto == 30):
            return True
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
    ctk.entrada()

if __name__ == "__main__":
    main()