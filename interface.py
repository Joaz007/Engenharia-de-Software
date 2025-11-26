import re #importe a biblioteca de Expressões Regulares
from tkinter import * #importa o tkinter - interface gráfica
import customtkinter as ctk #importa o customtkinter - interface gráfica personalizada
from PIL import Image #importa a biblioteca Pillow para manipulação de imagens
import requests #importa a biblioteca requests para fazer requisições HTTP
import database as db #importa o arquivo database.py para manipulação do banco de dados

#cadastro - ok
#fazer comprovante
#verificar disponibilidade de horário - ok
#exibir a lista de alunas - ok
#exibir a lista de alunas por turma
#remover aluna
#editar aluna
#aniversariantes do mês
#alunas com mensalidades atrasadas
#criar um banco de dados - ok
imageAdd_ctk = ctk.CTkImage(dark_image= Image.open("imagens/add.png"), size=(30, 30))
imageAlunas_ctk = ctk.CTkImage(dark_image= Image.open("imagens/alunas.png"), size=(35, 35))
imageHome_ctk = ctk.CTkImage(dark_image= Image.open("imagens/home.png"), size=(30, 30))
imageFit_ctk = ctk.CTkImage(dark_image= Image.open("imagens/fit.png"), size=(30, 30))
imageNiver_ctk = ctk.CTkImage(dark_image= Image.open("imagens/niver.png"), size=(30, 30))
imagePay_ctk = ctk.CTkImage(dark_image= Image.open("imagens/pay.png"), size=(30, 30))
imageRemove_ctk = ctk.CTkImage(dark_image= Image.open("imagens/remove.png"), size=(30, 30))
imageVenc_ctk = ctk.CTkImage(dark_image= Image.open("imagens/venc.png"), size=(30, 30))
imageVoltar_ctk = ctk.CTkImage(dark_image= Image.open("imagens/voltar.png"), size=(30, 30))
imageVagas_ctk = ctk.CTkImage(dark_image= Image.open("imagens/vagas.png"), size=(30, 30))
imageInput_ctk = ctk.CTkImage(dark_image= Image.open("imagens/input.png"), size=(30, 30))

def formatar_telefone(event):
    if event.keysym not in ('BackSpace', 'Delete') and not event.char:
        return

    entry = event.widget
    
    #Pega o texto atual e a posição do cursor
    texto_atual = entry.get()
    
    #Limpa o texto, mantendo apenas os dígitos
    numeros = re.sub(r'\D', '', texto_atual)
    
    #Limita a 11 dígitos (tamanho máximo de um celular com DDD)
    numeros = numeros[:11]
    
    novo_texto = ""
    if len(numeros) > 0:
        novo_texto = "(" + numeros[:2] # Adiciona (
    
    if len(numeros) >= 3:
        novo_texto += ") " + numeros[2:7] # Adiciona ) e o primeiro bloco de 5 números
        
    if len(numeros) >= 8:
        # Formato final com os últimos 4 dígitos
        novo_texto = f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}" 
        
    #Atualiza o texto no Entry
    entry.delete(0, ctk.END)
    entry.insert(0, novo_texto)

def formatar_data(event):
    if event.keysym not in ('BackSpace', 'Delete') and not event.char:
        return

    entry = event.widget
    
    #Pega o texto atual e a posição do cursor
    texto_atual = entry.get()
    
    #Limpa o texto, mantendo apenas os dígitos
    numeros = re.sub(r'\D', '', texto_atual)

    #Limita a 8 dígitos (tamanho máximo de uma data)
    numeros = numeros[:8]
    
    novo_texto = ""
    if len(numeros) > 0:
        novo_texto = numeros[:2] # Adiciona os primeiros 2 números
    if len(numeros) >= 3:
        novo_texto += "/" + numeros[2:4] # Adiciona / e o primeiro bloco de 2 números

    if len(numeros) >= 5:
        # Formato final com os últimos 4 dígitos
        novo_texto = f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:]}" 

    #Atualiza o texto no Entry
    entry.delete(0, ctk.END)
    entry.insert(0, novo_texto)
    
def formatar_cpf(event):
    if event.keysym not in ('BackSpace', 'Delete') and not event.char:
        return

    entry = event.widget
    texto_atual = entry.get()
    numeros = re.sub(r'\D', '', texto_atual)
    numeros = numeros[:11]

    novo_texto = ""
    if len(numeros) > 0:
        novo_texto = numeros[:3] # Adiciona os primeiros 3 números
    if len(numeros) >= 4:
        novo_texto += "." + numeros[3:6] # Adiciona . e o segundo bloco de 3 números
    if len(numeros) >= 7:
        novo_texto += "." + numeros[6:9] # Adiciona . e o terceiro bloco de 3 números
    if len(numeros) >= 10:
        novo_texto += "-" + numeros[9:] # Adiciona - e os últimos 2 dígitos

    entry.delete(0, ctk.END)
    entry.insert(0, novo_texto)
    
def valor(dias):
    if dias == 2:
        return db.AlunaNova2x().valorMensalidade()
    elif dias == 3:
        return db.AlunaNova3x().valorMensalidade()
    else:
        return db.AlunaComDesc().valorMensalidade()

def verificar_cep(cep):    
    if len(cep) != 8:
        return None, "CEP inválido"
    
    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url, timeout=5)
        data = response.json()
        if "erro" in data:
            return None, "CEP não encontrado."
        else:
            return data
    except requests.exceptions.RequestException as e:
        return None, f"Erro de conexão: {e}"
    
def cadastro(janela):
    novaAluna = db.AlunaBuilder()
    
    frameCadastro = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    frameCadastro.place(relx=0.5, rely=0.23, anchor=N)
    widgetCadastro = ctk.CTkFrame(frameCadastro, fg_color= "transparent", width=1450, height=750)
    widgetCadastro.place(relx= 0.5, anchor=N)
    widgetTermo = ctk.CTkFrame(frameCadastro, fg_color= "transparent", width=700, height=150)
    widgetTermo.place(relx= 0.5, rely=0.33, anchor=N)
    
    labelCadastro = ctk.CTkLabel(widgetCadastro, text="Cadastro", font=("Segoe UI Black",28))
    labelCadastro.grid(row=0, column=0, columnspan=9, pady= 30)
    
    #linha 1 - Nome, Apelido, Data de Nascimento
    labelNome = ctk.CTkLabel(widgetCadastro, text="Nome:", font=("Arial", 15))
    labelNome.grid(row=1, column=0, pady=10, sticky=E)
    entryNome = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryNome.grid(row=1, column=1, columnspan=3, pady=10, padx=10, sticky=EW)

    labelApelido = ctk.CTkLabel(widgetCadastro, text="Apelido:", font=("Arial", 15))
    labelApelido.grid(row=1, column=4, pady=10, sticky=E)
    entryApelido = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryApelido.grid(row=1, column=5, pady=10, padx=5, sticky=W)

    labelData = ctk.CTkLabel(widgetCadastro, text="Data de Nascimento:", font=("Arial", 15))
    labelData.grid(row=1, column=7, pady=10, sticky=E)
    entryData = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryData.grid(row=1, column=8, pady=10, padx= 10, sticky=W)
    entryData.bind("<KeyRelease>", formatar_data)

    #linha 2 - CEP, Endereço, Bairro, Celular
    labelCEP = ctk.CTkLabel(widgetCadastro, text="CEP:", font=("Arial", 15))
    labelCEP.grid(row=2, column=0, pady=10, sticky=E)
    entryCEP = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryCEP.grid(row=2, column=1, pady=10, padx= 10, sticky=W)
    botaoBuscarCEP = ctk.CTkButton(widgetCadastro, text="Buscar CEP", width= 50, command= lambda: buscar_cep())
    botaoBuscarCEP.grid(row=2, column=2, pady=10, padx=10, sticky=W)
    
    labelEndereco = ctk.CTkLabel(widgetCadastro, text="Endereço:", font=("Arial", 15))
    labelEndereco.grid(row=2, column=3, pady=10, sticky=E)
    entryEndereco = ctk.CTkEntry(widgetCadastro, font=("Arial", 15), width=250)
    entryEndereco.grid(row=2, column=4, pady=10, padx= 10, sticky=W)

    labelBairro = ctk.CTkLabel(widgetCadastro, text="Bairro:", font=("Arial", 15))
    labelBairro.grid(row=2, column=5, pady=10, sticky=E)
    entryBairro = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryBairro.grid(row=2, column=6, pady=10, padx= 10, sticky=W)

    labelNumero = ctk.CTkLabel(widgetCadastro, text="Celular:", font=("Arial", 15))
    labelNumero.grid(row=2, column=7, pady=10, sticky=E)
    entryNumero = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryNumero.grid(row=2, column=8, pady=10, padx= 10, sticky=W)
    entryNumero.bind("<KeyRelease>", formatar_telefone)
    
    #linha 3 - CPF, Quantidade de Dias, Valor da Mensalidade, Vencimento
    labelCPF = ctk.CTkLabel(widgetCadastro, text="CPF:", font=("Arial", 15))
    labelCPF.grid(row=3, column=0, pady=10, sticky=E)
    entryCPF = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryCPF.grid(row=3, column=1, pady=10, padx= 10, sticky=W)
    entryCPF.bind("<KeyRelease>", formatar_cpf)

    def defineDia(entrada):
        if entrada == 2:
            entryMensalidade.delete(0, ctk.END)
            entryMensalidade.insert(0, valor(dia_semana.get()))
            entryDiasSemana3.grid_forget()
            entryHorario3.grid_forget()
        elif entrada == 3:
            entryMensalidade.delete(0, ctk.END)
            entryMensalidade.insert(0, valor(dia_semana.get()))
            entryDiasSemana3.grid(row=3, column=4, pady= 30)
            entryHorario3.grid(row=3, column=5, pady= 30)
            
    dia_semana = IntVar()
    labelQuantDias = ctk.CTkLabel(widgetCadastro, text="Quantidade de Dias:", font=("Arial", 15))
    labelQuantDias.grid(row=3, column=3, pady=10, padx= 10, sticky=E)
    entry2 = ctk.CTkRadioButton(widgetCadastro, text="2x", font=("Arial", 15), variable=dia_semana, value=2, command=lambda: defineDia(2))
    entry2.grid(row=3, column=4, pady=10, sticky=W)
    entry3 = ctk.CTkRadioButton(widgetCadastro, text="3x", font=("Arial", 15), variable=dia_semana, value=3, command=lambda: defineDia(3))
    entry3.grid(row=3, column=5, pady=10, padx= 5, sticky=W)
        
    labelMensalidade = ctk.CTkLabel(widgetCadastro, text="Valor da Mensalidade:", font=("Arial", 15))
    labelMensalidade.grid(row=3, column=6, pady=10, sticky=E)
    entryMensalidade = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryMensalidade.grid(row=3, column=7, pady=10, padx= 10, sticky=W)
    entryMensalidade.insert(0, valor(dia_semana.get()))
    
    #linhas 4-9 - Vencimento
    vencimento_var = IntVar()
    labelVencimento = ctk.CTkLabel(widgetCadastro, text="Vencimento:", font=("Arial", 15))
    labelVencimento.grid(row=4, column=0, pady=10, padx= 5, sticky=E)
    entryVenc5 = ctk.CTkRadioButton(widgetCadastro, text="5", font=("Arial", 15), variable=vencimento_var, value=5)
    entryVenc5.grid(row=4, column=1, pady=10, padx= 5, sticky=W)
    entryVenc10 = ctk.CTkRadioButton(widgetCadastro, text="10", font=("Arial", 15), variable=vencimento_var, value=10)
    entryVenc10.grid(row=5, column=1, pady=10, padx= 5, sticky=W)
    entryVenc15 = ctk.CTkRadioButton(widgetCadastro, text="15", font=("Arial", 15), variable=vencimento_var, value=15)
    entryVenc15.grid(row=6, column=1, pady=10, padx= 5, sticky=W)
    entryVenc20 = ctk.CTkRadioButton(widgetCadastro, text="20", font=("Arial", 15), variable=vencimento_var, value=20)
    entryVenc20.grid(row=7, column=1, pady=10, padx= 5, sticky=W)
    entryVenc25 = ctk.CTkRadioButton(widgetCadastro, text="25", font=("Arial", 15), variable=vencimento_var, value=25)
    entryVenc25.grid(row=8, column=1, pady=10, padx= 5, sticky=W)
    entryVenc30 = ctk.CTkRadioButton(widgetCadastro, text="30", font=("Arial", 15), variable=vencimento_var, value=30)
    entryVenc30.grid(row=9, column=1, pady=10, padx= 5, sticky=W)

    labelTermo = ctk.CTkLabel(widgetTermo, text="Termo de Responsabilidade para Prática de Atividade Física", font=("Arial", 20))
    labelTermo.pack(pady=20)
    labelContrato = ctk.CTkLabel(widgetTermo, text="Estou ciente de que é recomendável conversar com um médico antes de aumentar meu nível atual de atividade física, tenho pleno conhecimento da minha atual condição de saúde. Sei também que a realização de atividades físicas pode acarretar algum risco, caso existam problemas clínicos que a contraindiquem total ou parcialmente. Assumo plena responsabilidade por qualquer atividade física praticada sem o atendimento a essa recomendação e DECLARO que aceito as responsabilidades inerentes à participação no treino, bem como isento de qualquer responsabilidade a \"Lu Mafra Personal Trainer\".\n\nConcorda com o Termo de Responsabilidade para Prática de Atividade Física?", font=("Arial", 18), wraplength=950, justify= "left")
    labelContrato.pack(pady=10)
    
    checkTermo = ctk.CTkCheckBox(widgetTermo, text="Concordo", font=("Arial", 15))
    checkTermo.pack(pady=10, anchor=W)
    
    def continuar():
        # Validação simples
        entryNome.configure(border_color="gray")
        entryCPF.configure(border_color="gray")
        entryData.configure(border_color="gray")
        entryNumero.configure(border_color="gray")
        labelQuantDias.configure(text_color="white")
        labelVencimento.configure(text_color="white")
        checkTermo.configure(border_color="gray")
        if (not entryNome.get().strip()):
            entryNome.configure(border_color="red")
            return
        if not entryCPF.get().strip() or not db.validar_cpf(entryCPF.get()):
            entryCPF.configure(border_color="red")
            return
        if (not entryData.get().strip()):
            entryData.configure(border_color="red")
            return
        if (not entryNumero.get().strip()):
            entryNumero.configure(border_color="red")
            return
        if (not dia_semana.get()):
            labelQuantDias.configure(text_color="red")
            return
        if (not vencimento_var.get()):
            labelVencimento.configure(text_color="red")
            return
        if not checkTermo.get():
            checkTermo.configure(border_color="red")
            return
            
        widgetCadastro.place_forget()
        widgetTermo.place_forget()

        # Mostra a nova tela (tabview e botões)
        frameHorarios.place(relx=0.5, rely=0.22, anchor=N)
        frame_botoes.place(relx=0.5, rely=0.88, anchor=N)
        
    labelContinuar = ctk.CTkButton(widgetCadastro, text="Continuar", font=("Arial", 15), command= lambda: continuar())
    labelContinuar.grid(row = 9, column = 8, pady=10, padx= 10, sticky=E)
    
    #novo frame para os horários
    frameHorarios = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)

    labelHorario = ctk.CTkLabel(frameHorarios, text="Horários Disponíveis", font=("Segoe UI Black", 28))
    labelHorario.grid(row=0, column=0, columnspan=9, pady= 30)

    labelDias = ctk.CTkLabel(frameHorarios, text="Selecione os dias da semana:   ", font=("Arial", 15))
    labelDias.grid(row=1, column=3, pady= 30)

    entryDiasSemana1 = ctk.CTkComboBox(frameHorarios, values=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], font=("Arial", 15))
    entryDiasSemana2 = ctk.CTkComboBox(frameHorarios, values=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], font=("Arial", 15))
    entryDiasSemana3 = ctk.CTkComboBox(frameHorarios, values=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], font=("Arial", 15))

    if dia_semana.get() == 2:
        entryDiasSemana1.grid(row=1, column=4, pady= 30)
        entryDiasSemana2.grid(row=2, column=4, pady= 30)
    elif dia_semana.get() == 3:
        entryDiasSemana1.grid(row=1, column=4, pady= 30)
        entryDiasSemana2.grid(row=2, column=4, pady= 30)
        entryDiasSemana3.grid(row=3, column=4, pady= 30)
        
    entryHorario1 = ctk.CTkComboBox(frameHorarios, font=("Arial", 15))
    entryHorario2 = ctk.CTkComboBox(frameHorarios, font=("Arial", 15))
    entryHorario3 = ctk.CTkComboBox(frameHorarios, font=("Arial", 15))

    if dia_semana.get() == 2:
        entryHorario1.grid(row=1, column=5, pady= 30)
        entryHorario2.grid(row=2, column=5, pady= 30)
    elif dia_semana.get() == 3:
        entryHorario1.grid(row=1, column=5, pady= 30)
        entryHorario2.grid(row=2, column=5, pady= 30)
        entryHorario3.grid(row=3, column=5, pady= 30)
        
    labelverificacao = ctk.CTkLabel(frameHorarios, text="", font=("Arial", 15))
    labelverificacao.grid(row=4, column=4, columnspan=2, pady=30)
    
    # frame para os botões Voltar/Enviar
    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent", height=100, width=1450)
    botao_voltar = ctk.CTkButton(frame_botoes, text="Voltar", font=("Arial", 15), command=lambda: voltar())
    botao_voltar.pack(side="left", padx=20, pady=15)
    botao_enviar = ctk.CTkButton(frame_botoes, text="Enviar", font=("Arial", 15), command=lambda: enviar_dados())
    botao_enviar.pack(side="right", padx=20, pady=15)
    
    def buscar_cep():
        cep = re.sub(r'\D', '', entryCEP.get())
        resultado = verificar_cep(cep)

        if isinstance(resultado, dict):
            entryEndereco.insert(0, resultado.get('logradouro', ''))
            entryBairro.insert(0, resultado.get('bairro', ''))
        elif isinstance(resultado, tuple): # Erro
            erro_msg = resultado[1]
            labelResp = ctk.CTkLabel(widgetCadastro, text="", font=("Arial", 15))
            labelResp.grid(row=2, column=2, pady=10, sticky=W)
            labelResp.configure(text=erro_msg)
            labelResp.after(3000, lambda: labelResp.destroy())
            
    def verificar_horarios():
        if dia_semana.get() == 2:
            if not db.verificaHorarios(entryDiasSemana1.get().lower(), entryHorario1.get()):
                labelverificacao.configure(text=f"Horário {entryHorario1.get()} indisponível para o dia {entryDiasSemana1.get().lower()}", text_color="red")
            if not db.verificaHorarios(entryDiasSemana2.get().lower(), entryHorario2.get()):
                labelverificacao.configure(text=f"Horário {entryHorario2.get()} indisponível para o dia {entryDiasSemana2.get().lower()}", text_color="red")
        elif dia_semana.get() == 3:
            if not db.verificaHorarios(entryDiasSemana1.get().lower(), entryHorario1.get()):
                labelverificacao.configure(text=f"Horário {entryHorario1.get()} indisponível para o dia {entryDiasSemana1.get().lower()}", text_color="red")
            if not db.verificaHorarios(entryDiasSemana2.get().lower(), entryHorario2.get()):
                labelverificacao.configure(text=f"Horário {entryHorario2.get()} indisponível para o dia {entryDiasSemana2.get().lower()}", text_color="red")
            if not db.verificaHorarios(entryDiasSemana3.get().lower(), entryHorario3.get()):
                labelverificacao.configure(text=f"Horário {entryHorario3.get()} indisponível para o dia {entryDiasSemana3.get().lower()}", text_color="red")
    
    def limpaInfo():
        #reseta valores padrão
        entryNome.delete(0, ctk.END)
        entryApelido.delete(0, ctk.END)
        entryData.delete(0, ctk.END)
        entryCEP.delete(0, ctk.END)
        entryEndereco.delete(0, ctk.END)
        entryBairro.delete(0, ctk.END)
        entryNumero.delete(0, ctk.END)
        entryCPF.delete(0, ctk.END)
        entryMensalidade.delete(0, ctk.END)
        
        dia_semana.set(0)       
        vencimento_var.set(0)   
        checkTermo.deselect()  
        
        entryDiasSemana1.set("")
        entryHorario1.delete(0, ctk.END)
        entryDiasSemana2.set("")
        entryHorario2.delete(0, ctk.END)
        entryDiasSemana3.set("")
        entryHorario3.delete(0, ctk.END)
        
        entryNome.configure(border_color="gray")
        entryCPF.configure(border_color="gray")
        entryData.configure(border_color="gray")
        entryNumero.configure(border_color="gray")
        labelVencimento.configure(text_color="gray")
        checkTermo.configure(border_color="gray")
        
    def enviar_dados():
        labelverificacao.configure(text="")  # Limpa a mensagem de verificação
        verificar_horarios()
        if labelverificacao.cget("text") != "":
            return
        # Coleta os dados dos campos
        nome = entryNome.get().strip()
        apelido = entryApelido.get().strip()
        nascimento = entryData.get().strip()
        cep = re.sub(r'\D', '', entryCEP.get())
        endereco = entryEndereco.get().strip()
        bairro = entryBairro.get().strip()
        celular = re.sub(r'\D', '', entryNumero.get())
        cpf = re.sub(r'\D', '', entryCPF.get())
        quantdias = dia_semana.get()
        if quantdias == 2:
            dias = f"{entryDiasSemana1.get().lower()}, {entryDiasSemana2.get().lower()}"
            horario = f"{entryHorario1.get()}, {entryHorario2.get()}"
        elif quantdias == 3:
            dias = f"{entryDiasSemana1.get().lower()}, {entryDiasSemana2.get().lower()}, {entryDiasSemana3.get().lower()}"
            horario = f"{entryHorario1.get()}, {entryHorario2.get()}, {entryHorario3.get()}"
        valor_mensalidade = entryMensalidade.get().strip()
        vencimento = vencimento_var.get()
        termo = checkTermo.get()
        
        # Insere os dados no banco de dados
        nova_aluna = db.InserirInfosAlunas(nome, apelido, nascimento, cep, endereco, bairro, celular, cpf, quantdias, dias, horario, valor_mensalidade, vencimento, termo)
        if nova_aluna:
            text = db.Academia().addAlunas(nova_aluna)
            label = ctk.CTkLabel(frameHorarios, text="", font=("Arial", 15))
            label.grid(row=5, column=4, columnspan=2, pady=30)
            label.configure(text=text, text_color="green")
            label.after(3000, lambda: (label.destroy(), voltar(), limpaInfo()))
        else:
            print("Erro ao enviar os dados.")

    def voltar():
        # Esconde a tela de horários
        frameHorarios.place_forget()
        frame_botoes.place_forget()

        # Re-exibe a tela de cadastro
        widgetCadastro.place(relx=0.5, anchor=N)
        widgetTermo.place(relx=0.5, rely=0.32, anchor=N)
    
    return frameCadastro
        
def vagasDisponiveis(janela):
    academia = db.Academia()
    widgetVagas = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetVagas.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    widgetVagas.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    widgetVagas.grid_rowconfigure(1, weight=1)
    
    label = ctk.CTkLabel(widgetVagas, text="Vagas Disponíveis", font=("Segoe UI Black", 30))
    label.grid(row=0, column=0, columnspan=5, padx=5, pady=20)
    
    scroll_frame = ctk.CTkScrollableFrame(widgetVagas, fg_color="transparent")
    scroll_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
    scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    
    label_cabecalhoSeg = ctk.CTkLabel(scroll_frame, text="Segunda", font=("Arial", 15, "bold"))
    label_cabecalhoSeg.grid(row=2, column=0, pady=10)
    label_cabecalhoTer = ctk.CTkLabel(scroll_frame, text="Terça", font=("Arial", 15, "bold"))
    label_cabecalhoTer.grid(row=2, column=1, pady=10)
    label_cabecalhoQua = ctk.CTkLabel(scroll_frame, text="Quarta", font=("Arial", 15, "bold"))
    label_cabecalhoQua.grid(row=2, column=2, pady=10)
    label_cabecalhoQui = ctk.CTkLabel(scroll_frame, text="Quinta", font=("Arial", 15, "bold"))
    label_cabecalhoQui.grid(row=2, column=3, pady=10)
    label_cabecalhoSex = ctk.CTkLabel(scroll_frame, text="Sexta", font=("Arial", 15, "bold"))
    label_cabecalhoSex.grid(row=2, column=4, pady=10)

    weekdays = ["segunda", "terça", "quarta", "quinta", "sexta"]

    for j, dia in enumerate(weekdays, start=0):
        vagas_do_dia = academia.mostraVagas(dia)

        if not vagas_do_dia:
            text = "Todos os horários estão disponíveis"
            entrytext = ctk.CTkLabel(scroll_frame, text=text, font=("Arial", 15))
            entrytext.grid(row=3, column=j, padx=5, pady=5, sticky='n')
            continue

        for i, vaga in enumerate(vagas_do_dia, start=3):
            horario, ocupado, limite, vagas = vaga
            
            text = f"{horario}h: {ocupado}/{limite} ({vagas} vagas)"
            
            entrytext = ctk.CTkLabel(scroll_frame, text=text, font=("Arial", 15))
            entrytext.grid(row=i, column=j, padx=5, pady=5, sticky='n')

    return widgetVagas

def mensalidades_vencidas(janela):
    academia = db.Academia()
    widgetMensalidades = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetMensalidades.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    label = ctk.CTkLabel(widgetMensalidades, text="Página de Mensalidades", font=("Segoe UI Black", 30))
    label.pack(pady=100)
    return widgetMensalidades
    
def lista_alunas(janela):
    academia = db.Academia()
    widgetLista = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetLista.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    widgetLista.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
    widgetLista.grid_rowconfigure(1, weight=1)
    
    label = ctk.CTkLabel(widgetLista, text="Lista de Alunas", font=("Segoe UI Black", 30))
    label.grid(row=0, column=0, columnspan=7, padx=5, pady=20)

    scroll_frame = ctk.CTkScrollableFrame(widgetLista, fg_color="transparent")
    scroll_frame.grid(row=1, column=0, columnspan=7, sticky="nsew", padx=10, pady=10)
    scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    label_cabecalhoNome = ctk.CTkLabel(scroll_frame, text="Nome", font=("Arial", 15, "bold"))
    label_cabecalhoNome.grid(row=0, column=0, pady=10)
    label_cabecalhoApelido = ctk.CTkLabel(scroll_frame, text="Apelido", font=("Arial", 15, "bold"))
    label_cabecalhoApelido.grid(row=0, column=1, padx=5, pady=10)
    label_cabecalhoCPF = ctk.CTkLabel(scroll_frame, text="CPF", font=("Arial", 15, "bold"))
    label_cabecalhoCPF.grid(row=0, column=2, pady=10)
    label_cabecalhoDias = ctk.CTkLabel(scroll_frame, text="Dias", font=("Arial", 15, "bold"))
    label_cabecalhoDias.grid(row=0, column=3, pady=10)
    label_cabecalhoHorario = ctk.CTkLabel(scroll_frame, text="Horário", font=("Arial", 15, "bold"))
    label_cabecalhoHorario.grid(row=0, column=4, pady=10)
    label_cabecalhoValor = ctk.CTkLabel(scroll_frame, text="Valor", font=("Arial", 15, "bold"))
    label_cabecalhoValor.grid(row=0, column=5, pady=10)
    label_cabecalhoVencimento = ctk.CTkLabel(scroll_frame, text="Vencimento", font=("Arial", 15, "bold"))
    label_cabecalhoVencimento.grid(row=0, column=6, padx=5, pady=10)

    for i, aluna in enumerate(academia.listaAlunas(), start=1):
        nome, apelido, cpf, dias, horario, valor, vencimento = aluna
        
        entryNome = ctk.CTkLabel(scroll_frame, text=nome, font=("Arial", 15))
        entryNome.grid(row=i, column=0, padx=5, pady=5)
        entryApelido = ctk.CTkLabel(scroll_frame, text=apelido, font=("Arial", 15))
        entryApelido.grid(row=i, column=1, padx=5, pady=5)
        entryCPF = ctk.CTkLabel(scroll_frame, text=cpf, font=("Arial", 15))
        entryCPF.grid(row=i, column=2, padx=5, pady=5)
        entryDias = ctk.CTkLabel(scroll_frame, text=dias, font=("Arial", 15))
        entryDias.grid(row=i, column=3, padx=5, pady=5)
        entryHorario = ctk.CTkLabel(scroll_frame, text=horario, font=("Arial", 15))
        entryHorario.grid(row=i, column=4, padx=5, pady=5)
        entryValor = ctk.CTkLabel(scroll_frame, text=f"R${valor}", font=("Arial", 15))
        entryValor.grid(row=i, column=5, padx=5, pady=5)
        entryVencimento = ctk.CTkLabel(scroll_frame, text=vencimento, font=("Arial", 15))
        entryVencimento.grid(row=i, column=6, padx=5, pady=5)

    return widgetLista
    
def entrada():
    janela = ctk.CTk()
    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    janela.geometry(f"{screen_width}x{screen_height}+0+0")
    janela.title("Lu Mafra Personal Trainer")
    
    # Dicionário para rastrear a página (frame) ativa
    app_state = {"active_page_frame": None}

    try:
        # Imagem grande (Home)
        imagem_largura_g = 300 
        imagem_altura_g = 180
        img_grande = Image.open("imagens/lu_mafra.png").resize((imagem_largura_g, imagem_altura_g))
        img_grande_dark = Image.open("imagens/lu_mafra2.png").resize((imagem_largura_g, imagem_altura_g))
        labelImagemGrande = ctk.CTkImage(light_image=img_grande, dark_image=img_grande_dark, size=(imagem_largura_g, imagem_altura_g))
        
        # Imagem pequena (Subpáginas)
        imagem_largura_p = 225
        imagem_altura_p = 110
        img_pequena = Image.open("imagens/lu_mafra.png").resize((imagem_largura_p, imagem_altura_p))
        img_pequena_dark = Image.open("imagens/lu_mafra2.png").resize((imagem_largura_p, imagem_altura_p))
        labelImagemPequena = ctk.CTkImage(light_image=img_pequena, dark_image=img_pequena_dark, size=(imagem_largura_p, imagem_altura_p))
    except FileNotFoundError:
        print("ERRO CRÍTICO: Imagens 'lu_mafra.png' ou 'lu_mafra2.png' não encontradas.")
        labelImagemGrande = None
        labelImagemPequena = None
    except Exception as e:
        print(f"Erro ao carregar imagens: {e}")
        labelImagemGrande = None
        labelImagemPequena = None

    # widget1 (Título da Home)
    widget1 = ctk.CTkFrame(janela, fg_color="transparent")
    widget1.place(relx=0.5, rely=0.15, anchor=CENTER)
    set_theme = ctk.get_appearance_mode()
    label_titulo = ctk.CTkLabel(widget1, text="Lu Mafra Personal Trainer", font=("Arial", 30, "bold"), text_color="light green" if set_theme == "Dark" else "green")
    label_titulo.pack()
    
    # widget2 (Container do Logo)
    widget2 = ctk.CTkFrame(janela, fg_color="transparent")
    widget2.place(relx=0.65, rely=0.5, anchor=CENTER)
    label_da_imagem = ctk.CTkLabel(widget2, text="")
    if labelImagemGrande:
        label_da_imagem.configure(image=labelImagemGrande)
    else:
        label_da_imagem.configure(text="Imagem não encontrada")
    label_da_imagem.pack()

    # widget3 (Container do Menu)
    botao_altura = int(screen_height * 0.02)
    widget3 = ctk.CTkFrame(janela, fg_color="transparent")
            
    #funções de navegação entre páginas
    def go_home():        
        #Destrói a página ativa
        if app_state["active_page_frame"]:
            app_state["active_page_frame"].destroy()
            app_state["active_page_frame"] = None
            
        #Restaura o layout da "Home"
        widget1.place(relx=0.5, rely=0.15, anchor=CENTER) # Mostra o Título
        widget2.place(relx=0.5, rely=0.55, anchor=CENTER) # Move o Logo para o centro
        widget3.place(relx=0.5, rely=0.30, anchor=CENTER) # Move o Menu para o centro
        
        label_titulo.configure(text="Bem vinda ao site da Lu Mafra Personal Trainer")
        #Restaura a imagem grande
        if labelImagemGrande:
            label_da_imagem.configure(image=labelImagemGrande)
            
        #Esconde o próprio botão "Início"
        botao_inicio.grid_forget()

    def clear_and_show_page(page_function):
        #Destrói a página antiga
        if app_state["active_page_frame"]:
            app_state["active_page_frame"].destroy()
            app_state["active_page_frame"] = None
            
        #Esconde o Título da Home
        widget1.place_forget()
        
        #Move o Menu e o Logo para o TOPO
        widget3.place(relx=0.5, rely=0.17, anchor=N)
        widget3.rowconfigure(1, weight=0)
        widget2.place(relx=0.5, rely=0.02, anchor=N)
        
        #Muda para a imagem pequena
        if labelImagemPequena:
            label_da_imagem.configure(image=labelImagemPequena)
            
        #Mostra o botão "Início" (na coluna 4 do grid do widget2)
        botao_inicio.grid(row=1, column=4, padx=5, pady=5)
        
        #Cria e armazena a nova página
        app_state["active_page_frame"] = page_function(janela)

    #botões do menu
    botao_cadastro = ctk.CTkButton(widget3, image= imageAdd_ctk, hover_color= "#292B25", width=imageAdd_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(cadastro))
    botao_cadastro.grid(row=1, column=0, padx=5, pady=5)
    labelCadastro = ctk.CTkLabel(widget3, text= "Cadastro", font= ("Segoe UI Black", 18))
    labelCadastro.grid(row = 2, column=0, padx=5, pady=5)
    
    botao_vagas = ctk.CTkButton(widget3, image= imageVagas_ctk, hover_color= "#292B25", width=imageVagas_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(vagasDisponiveis))
    botao_vagas.grid(row=1, column=1, padx=5, pady=5)
    labelVagas = ctk.CTkLabel(widget3, text= "Vagas Disponíveis", font= ("Segoe UI Black", 18))
    labelVagas.grid(row=2, column=1, padx=5, pady=5)

    botao_mensalidades = ctk.CTkButton(widget3, image= imageVenc_ctk, hover_color= "#292B25", width=imageVenc_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(mensalidades_vencidas))
    botao_mensalidades.grid(row=1, column=2, padx=5, pady=5)
    labelMensalidades = ctk.CTkLabel(widget3, text= "Mensalidades", font= ("Segoe UI Black", 18))
    labelMensalidades.grid(row=2, column=2, padx=5, pady=5)

    botao_lista = ctk.CTkButton(widget3, image= imageAlunas_ctk, hover_color= "#292B25", width=imageAlunas_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(lista_alunas))
    botao_lista.grid(row=1, column=3, padx=5, pady=5)
    labelLista = ctk.CTkLabel(widget3, text= "Lista de Alunas", font= ("Segoe UI Black", 18))
    labelLista.grid(row=2, column=3, padx=5, pady=5)
    
    botao_inicio = ctk.CTkButton(widget3, image= imageHome_ctk, hover_color= "#292B25", width=imageHome_ctk.__sizeof__(), height=botao_altura , text="", fg_color="transparent", command=go_home)

    botao_sair = ctk.CTkButton(janela, text="Sair", hover_color= "#292B25", command=janela.quit)
    botao_sair.pack(side="bottom", pady=10)
    
    widgetAutenticacao = ctk.CTkFrame(janela, fg_color="transparent")
    labelUser = ctk.CTkLabel(widgetAutenticacao, text="Usuário:", font=("Segoe UI Black", 20))
    labelUser.grid(row=0, column=0, padx=5, pady=5)
    entryUser = ctk.CTkEntry(widgetAutenticacao, font=("Arial", 20))
    entryUser.grid(row=0, column=1, padx=5, pady=5)
    labelSenha = ctk.CTkLabel(widgetAutenticacao, text="Senha:", font=("Segoe UI Black", 20))
    labelSenha.grid(row=1, column=0, padx=5, pady=5)
    entrySenha = ctk.CTkEntry(widgetAutenticacao, font=("Arial", 20), show="*")
    entrySenha.grid(row=1, column=1, padx=5, pady=5)
    
    def autenticar():
        if entryUser.get() == "admin" and entrySenha.get() == "admin":
            widgetAutenticacao.place_forget()
            go_home()
        else:
            erro_label = ctk.CTkLabel(janela, text="Usuário ou senha incorretos.", text_color="red", font=("Arial", 20))
            erro_label.place(relx=0.5, rely=0.6, anchor=CENTER)
            erro_label.after(2000, erro_label.destroy)
    
    botaoLogin = ctk.CTkButton(widgetAutenticacao, image=imageInput_ctk, hover_color= "#292B25", width=imageInput_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: autenticar())
    botaoLogin.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    widgetAutenticacao.place(relx=0.35, rely=0.5, anchor=CENTER)
    
    janela.mainloop()

if __name__ == "__main__":
    entrada()