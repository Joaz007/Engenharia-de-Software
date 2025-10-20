import sqlite3
import os

# Define o nome do arquivo do banco de dados
NOME_BANCO = 'inscricoes.db'

def criar_banco():
    """
    Cria o banco de dados e a tabela 'alunos' se ainda não existirem.
    """
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
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
        email TEXT,
        dias_semana TEXT,
        horario TEXT,
        valor REAL,
        uso_imagem BOOLEAN,
        instagram TEXT,
        dia_vencimento INTEGER
    )
    ''')
    print("Banco de dados e tabela 'alunos' verificados com sucesso.")
    conn.commit()
    conn.close()

def adicionar_aluno(dados_aluno):
    """
    Adiciona um novo aluno ao banco de dados.
    'dados_aluno' deve ser uma tupla na ordem correta dos campos.
    """
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    
    # SQL para inserir os dados
    sql = '''
    INSERT INTO alunos (
        nome, apelido, sexo, data_nascimento, cep, endereco, bairro, 
        celular, cpf, email, dias_semana, horario, valor, 
        uso_imagem, instagram, dia_vencimento
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    try:
        cursor.execute(sql, dados_aluno)
        conn.commit()
        # Mensagem de sucesso genérica
        print(f"Aluno '{dados_aluno[0]}' adicionado com sucesso!")
    except sqlite3.IntegrityError as e:
        # Erro comum se o CPF já existir (por causa do 'UNIQUE')
        print(f"Erro: Não foi possível adicionar o aluno. O CPF '{dados_aluno[9]}' já pode existir. {e}")
    finally:
        conn.close()

def listar_alunos():
    """
    Lista todos os alunos cadastrados no banco.
    """
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    
    # Seleciona todos os dados da tabela
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    
    if not alunos:
        print("Nenhum aluno cadastrado.")
    else:
        print("\n--- Lista de Alunos Cadastrados ---")
        for aluno in alunos:
            print(aluno)
            
    conn.close()

# --- EXEMPLO DE USO REAL ---
if __name__ == "__main__":
    
    # 1. Garante que o banco e a tabela existam
    # (Sempre rode isso antes de qualquer coisa)
    criar_banco()

    # 2. Como adicionar um aluno de verdade:
    # No seu programa real, esses dados virão dos campos de texto,
    # botões de rádio, etc., da sua interface.
    
    # A ordem DEVE ser a mesma definida no 'INSERT' da função adicionar_aluno:
    # (nome, apelido, sexo, data_nasc, cep, endereco, bairro, 
    #  celular, cpf, email, dias_semana, horario, valor, 
    #  uso_imagem (True/False), instagram, dia_vencimento)
    
    aluno_real_exemplo = (
        "Ana Clara Souza", "Ana", "Feminino", "15/03/2001",
        "86801-200", "Rua dos Pássaros, 500", "Jardim Alegre",
        "43912345678", "111.222.333-44", "ana.clara@email.com",
        "2x", "19:00-20:00", 140.00,
        True, # True para "Sim", False para "Não" (uso_imagem)
        "@anaclara.souza", 
        15 # dia_vencimento
    )

    # 3. Chame a função para adicionar
    # (Descomente a linha abaixo para adicionar a 'Ana Clara')
    #
    # adicionar_aluno(aluno_real_exemplo)

    # 4. Lista todos os alunos que já estão no banco
    # (Isso mostrará a 'Ana Clara' e qualquer outra que você já tenha)
    listar_alunos()