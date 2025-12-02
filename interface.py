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
#aniversariantes do mês - ok
#alunas com mensalidades atrasadas
#criar um banco de dados - ok
imageAdd_ctk = ctk.CTkImage(dark_image= Image.open("imagens/add.png"), size=(30, 30))
imageAlunas_ctk = ctk.CTkImage(dark_image= Image.open("imagens/alunas.png"), size=(35, 35))
imageHome_ctk = ctk.CTkImage(dark_image= Image.open("imagens/home.png"), size=(30, 30))
imageFit_ctk = ctk.CTkImage(dark_image= Image.open("imagens/fit.png"), size=(30, 30))
imageNiver_ctk = ctk.CTkImage(dark_image= Image.open("imagens/niver.png"), size=(30, 30))
imagePay_ctk = ctk.CTkImage(dark_image= Image.open("imagens/pay.png"), size=(30, 30))
imageEdit_ctk = ctk.CTkImage(dark_image= Image.open("imagens/person_edit.png"), size=(30, 30))
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
    texto_atual = entry.get()
    numeros = re.sub(r'\D', '', texto_atual)
    numeros = numeros[:8]
    
    novo_texto = ""
    if len(numeros) > 0:
        novo_texto = numeros[:2] # DD
    if len(numeros) >= 3:
        novo_texto += "/" + numeros[2:4] # /MM
    if len(numeros) >= 5:
        novo_texto += "/" + numeros[4:] # /AAAA 

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
        
    labelContinuar = ctk.CTkButton(widgetCadastro, text="Continuar", font=("Arial", 15), command= lambda: continuar())
    labelContinuar.grid(row = 9, column = 8, pady=10, padx= 10, sticky=E)
    
    #novo frame para os horários
    frameHorarios = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)

    labelHorario = ctk.CTkLabel(frameHorarios, text="Horários Disponíveis", font=("Segoe UI Black", 28))
    labelHorario.grid(row=0, column=0, columnspan=9, pady= 30)

    labelDias = ctk.CTkLabel(frameHorarios, text="Selecione os dias da semana e o horário:", font=("Arial", 15))
    labelDias.grid(row=1, column=0, columnspan=9, pady= 30)

    entryDiasSemana1 = ctk.CTkComboBox(frameHorarios, values=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], font=("Arial", 15), command=lambda dia: defineHorario(entryDiasSemana1, entryHorario1))
    entryDiasSemana2 = ctk.CTkComboBox(frameHorarios, values=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], font=("Arial", 15), command=lambda dia: defineHorario(entryDiasSemana2, entryHorario2))
    entryDiasSemana3 = ctk.CTkComboBox(frameHorarios, values=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], font=("Arial", 15), command=lambda dia: defineHorario(entryDiasSemana3, entryHorario3))
    entryDiasSemana1.set("Selecione um dia")
    entryDiasSemana2.set("Selecione um dia")
    entryDiasSemana3.set("Selecione um dia")
    entryHorario1 = ctk.CTkComboBox(frameHorarios, values= ["Selecione um horário"], font=("Arial", 15))
    entryHorario2 = ctk.CTkComboBox(frameHorarios, values= ["Selecione um horário"], font=("Arial", 15))
    entryHorario3 = ctk.CTkComboBox(frameHorarios, values= ["Selecione um horário"], font=("Arial", 15))
    entryHorario1.set("Selecione um horário")
    entryHorario2.set("Selecione um horário")
    entryHorario3.set("Selecione um horário")      
    
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
    
    def defineDia(entrada):
        entryMensalidade.delete(0, ctk.END)
        entryMensalidade.insert(0, valor(entrada))
    
    def continuar():
        # Validação simples
        entryNome.configure(border_color="#565B5E")
        entryCPF.configure(border_color="#565B5E")
        entryData.configure(border_color="#565B5E")
        entryNumero.configure(border_color="#565B5E")
        labelQuantDias.configure(text_color="#FFFFFF")
        labelVencimento.configure(text_color="#FFFFFF")
        checkTermo.configure(border_color="#565B5E")
        if (not entryNome.get().strip()):
            entryNome.configure(border_color="red")
            return
        if not entryCPF.get().strip() or not db.validar_cpf(entryCPF.get()):
            entryCPF.configure(border_color="red")
            return
        if (not entryData.get().strip() or not db.validar_data(entryData.get())):
            entryData.configure(border_color="red")
            return
        if (not entryNumero.get().strip() or not db.validar_telefone(entryNumero.get())):
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
        
        if dia_semana.get() == 2:
            entryDiasSemana1.grid(row=2, column=3, pady= 30)
            entryHorario1.grid(row=2, column=4, pady= 30)
            entryDiasSemana2.grid(row=3, column=3, pady= 30)
            entryHorario2.grid(row=3, column=4, pady= 30)
        elif dia_semana.get() == 3:
            entryDiasSemana1.grid(row=2, column=3, pady= 30)
            entryHorario1.grid(row=2, column=4, pady= 30)
            entryDiasSemana2.grid(row=3, column=3, pady= 30)
            entryHorario2.grid(row=3, column=4, pady= 30)
            entryDiasSemana3.grid(row=4, column=3, pady= 30)
            entryHorario3.grid(row=4, column=4, pady= 30)
    
    def defineHorario(entryDia, entryHorario):
        horarios = []
        if entryDia.get() == "Segunda":
            horarios = ['06:00', '07:00', '08:00', '09:00', '11:00', '11:30', '14:30', '15:30', '16:30', '17:30', '18:30', '19:30']
        elif entryDia.get() == "Terça":
            horarios = ['06:00', '07:00', '08:00', '09:00', '15:30', '16:30', '17:30', '18:30', '19:30']
        elif entryDia.get() == "Quarta":
            horarios = ['06:00', '07:00', '08:00', '09:00', '11:00', '11:30', '14:30', '15:30', '16:30', '17:30', '18:30', '19:30']
        elif entryDia.get() == "Quinta":
            horarios = ['06:00', '07:00', '08:00', '09:00', '15:30', '16:30', '17:30', '18:30', '19:30']
        elif entryDia.get() == "Sexta":
            horarios = ['06:00', '07:00', '08:00', '09:00', '11:00', '11:30', '14:30', '15:30', '16:30', '17:30', '18:30']
        
        if entryDia.get() == "Selecione um dia":
            horarios = []
            
        entryHorario.configure(values= horarios)            
    
    def voltar():
        # Esconde a tela de horários
        frameHorarios.place_forget()
        frame_botoes.place_forget()

        # Re-exibe a tela de cadastro
        widgetCadastro.place(relx=0.5, anchor=N)
        widgetTermo.place(relx=0.5, rely=0.32, anchor=N)
        
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
        entryHorario1.set("")
        entryDiasSemana2.set("")
        entryHorario2.set("")
        entryDiasSemana3.set("")
        entryHorario3.set("")
        
        entryNome.configure(border_color="#565B5E")
        entryCPF.configure(border_color="#565B5E")
        entryData.configure(border_color="#565B5E")
        entryNumero.configure(border_color="#565B5E")
        labelVencimento.configure(text_color="white")
        checkTermo.configure(border_color="#565B5E")
        
    def enviar_dados():
        labelverificacao.configure(text="")  # Limpa a mensagem de verificação
                
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
            label.grid(row=5, column=0, columnspan=9, pady=30)
            label.configure(text=text, text_color="green")
            label.after(3000, lambda: (label.destroy(), voltar(), limpaInfo()))
        else:
            print("Erro ao enviar os dados.")
    
    return frameCadastro

def editar_alunas(janela):
    academia = db.Academia()
    widgetEditar = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetEditar.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    widgetEditar.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    label = ctk.CTkLabel(widgetEditar, text="Editar Aluna", font=("Segoe UI Black", 30))
    label.grid(row=0, column=0, columnspan=6, pady=20)

    labelInstrucao = ctk.CTkLabel(widgetEditar, text="Insira o nome ou CPF da aluna:", font=("Arial", 15))
    labelInstrucao.grid(row=1, column=1, padx=5, pady=10, sticky=E)
    entryEditar = ctk.CTkEntry(widgetEditar, font=("Arial", 15), width=300)
    entryEditar.grid(row=1, column=2, columnspan=2, pady=10)
    botaoPesquisar = ctk.CTkButton(widgetEditar, text="Buscar", font=("Arial", 15), command=lambda: buscar_alunas())
    botaoPesquisar.grid(row=1, column=4, pady=10, sticky=W)
    
    label_status = ctk.CTkLabel(widgetEditar, text="", font=("Arial", 15))
    entryacao = None
    alunaEdit = None
    cpf_para_editar = None
    boxInfo = None 
    entry_nova_info = None
    scroll = None
    switch_editar = {
        "Nome": "nome", "Data de Nascimento": "nascimento", "CEP": "cep", "Endereço": "endereco",
        "Bairro": "bairro", "Celular": "celular", "CPF": "cpf", "Quantidade de Dias": "dias",
        "Dias da Semana": "diasSemana", "Horário": "horario", "Valor da Mensalidade": "valor", "Vencimento": "vencimento"}
    
    
    def executar_edicao(alunas_listadas, scroll):
        nonlocal entryacao, alunaEdit, cpf_para_editar, boxInfo, entry_nova_info
        
        if not entryacao:
            label_status.configure(text="Erro: Campo de ID não encontrado.", text_color="red")
            label_status.grid(row=2, column=0, columnspan=6, pady=5)
            return
            
        try:
            id_visual = int(entryacao.get().strip())
            cpf_para_editar = alunas_listadas[id_visual - 1][1]

        except ValueError:
            msg = "Erro: Insira um ID numérico válido."
            label_status.configure(text=msg, text_color="red")
            label_status.grid(row=2, column=0, columnspan=6, pady=5)
            return

        except IndexError:
            msg = "Erro: ID fora do intervalo da lista."
            label_status.configure(text=msg, text_color="red")
            label_status.grid(row=2, column=0, columnspan=6, pady=5)
            return
        
        alunaEdit = academia.listaAlunas(cpf=cpf_para_editar)
        
        scroll.destroy()
        labelInstrucao.grid_forget()
        entryEditar.grid_forget()
        
        for widget in widgetEditar.grid_slaves():
            if int(widget.grid_info()["row"]) >= 2:
                widget.destroy()
                
        label_status.configure(text=f"Selecione o campo para editar de {alunaEdit[0][1]}:", text_color="white")
        label_status.grid(row=1, column=1, padx=5, pady=10, sticky=E)
        
        boxInfo = ctk.CTkComboBox(
            widgetEditar, 
            values=list(switch_editar.keys()), 
            font=("Arial", 15), 
            width=200
        )
        boxInfo.grid(row=1, column=2, columnspan=2, pady=10)
        boxInfo.set("Selecione uma informação")
        entry_nova_info = ctk.CTkEntry(
            widgetEditar, 
            placeholder_text="Insira a nova informação:", 
            font=("Arial", 15),
            width=200
        )
        entry_nova_info.grid(row=3, column=2, columnspan=2, pady=10)
        
        def atualizar_mascara(valor):
            try:
                entry_nova_info.unbind("<KeyRelease>")
            except Exception:
                pass

            if valor == "Data de Nascimento":
                entry_nova_info.bind("<KeyRelease>", formatar_data)
            elif valor == "CPF":
                entry_nova_info.bind("<KeyRelease>", formatar_cpf)
            elif valor == "Celular":
                entry_nova_info.bind("<KeyRelease>", formatar_telefone)
            else:
                pass

        boxInfo.configure(command=lambda v=None: atualizar_mascara(boxInfo.get()))
        
        botaoPesquisar.configure(text="Editar", command= lambda: exibeTexto())
        
        def exibeTexto():
            campo = switch_editar.get(boxInfo.get())
            novo_valor = entry_nova_info.get().strip()

            if campo is None:
                label_status.configure(text="Selecione um campo válido.", text_color="red")
                return

            dados = {campo: novo_valor}

            # para "Dias da Semana" e "Horário"
            if campo == "diasSemana":
                dados["diasSemana"] = novo_valor.split(",")
            if campo == "horario":
                dados["horario"] = novo_valor.split(",")

            resultado = academia.editarAluna(cpf_para_editar, **dados)

            labelResultado = ctk.CTkLabel(widgetEditar, text=resultado, font=("Segoe UI", 15))
            labelResultado.grid(row=4, column=0, columnspan=6, pady=5)
            
            def restaurar_interface():
                # Destrói todos os elementos específicos da fase de edição
                boxInfo.destroy() 
                entry_nova_info.destroy()
                labelResultado.destroy()
                label_status.destroy()

                # Restaura os widgets de busca para a Fase 1
                labelInstrucao.grid(row=1, column=1, padx=5, pady=10, sticky=E)
                entryEditar.grid(row=1, column=2, columnspan=2, pady=10) 
                botaoPesquisar.configure(text="Buscar", command=lambda: buscar_alunas())
                
            if resultado == "Dados da aluna atualizados com sucesso.":
                labelResultado.after(2000, restaurar_interface)
            else:
                labelResultado.after(2000, labelResultado.destroy)
                
        
    def buscar_alunas():
        nonlocal entryacao
        
        for widget in widgetEditar.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                widget.destroy()
                
        label_status.configure(text="")
        label_status.grid_forget()

        scroll = ctk.CTkScrollableFrame(widgetEditar, fg_color="transparent")
        scroll.grid(row=2, column=0, columnspan=6, sticky="nsew", padx=20, pady=10)
        scroll.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        alunas = academia.buscarPorNome_ou_Cpf(entryEditar.get().strip())
        
        # Limpa o campo de ação antigo
        if entryacao:
            entryacao.destroy()
            entryacao = None
            
        if not alunas:
            labelaluna = ctk.CTkLabel(scroll, text="Nenhuma aluna encontrada com essa informação", font=("Arial", 18))
            labelaluna.grid(row=0, column=0, columnspan=6, pady=10, padx=5)
        else:            
            # Cabeçalhos
            labelID = ctk.CTkLabel(scroll, text="ID", font=("Arial", 15))
            labelID.grid(row=0, column=0, pady=5, padx=5)
            labelnome = ctk.CTkLabel(scroll, text="Nome", font=("Arial", 15))
            labelnome.grid(row=0, column=1, pady=5, padx=5)
            labelcpf = ctk.CTkLabel(scroll, text="CPF", font=("Arial", 15))
            labelcpf.grid(row=0, column=2, pady=5, padx=5)
            labelvalor = ctk.CTkLabel(scroll, text="Valor", font=("Arial", 15))
            labelvalor.grid(row=0, column=3, pady=5, padx=5)
            labelvencimento = ctk.CTkLabel(scroll, text="Vencimento", font=("Arial", 15))
            labelvencimento.grid(row=0, column=4, pady=5, padx=5)

            # Campo e Botão de Ação (criados no scroll para centralizar)
            entryacao = ctk.CTkEntry(scroll, placeholder_text="ID", font=("Arial", 12), width=50)
            entryacao.grid(row=0, column=5, pady=5, padx=5, sticky=W)
            
            # Passa a lista de alunas para o comando de edição
            botaoEnter = ctk.CTkButton(scroll, text="Editar", font=("Arial", 12), command=lambda: executar_edicao(alunas, scroll))
            botaoEnter.grid(row=0, column=5, pady=5, padx=5, sticky=E)

            for i, aluna in enumerate(alunas, start=1):
                nome, cpf, nascimento, valor, vencimento = aluna
                
                entryID = ctk.CTkLabel(scroll, text=str(i), font=("Arial", 15)) # i = ID visual
                entryID.grid(row=i, column=0, pady=5, padx=5)
                entrynome = ctk.CTkLabel(scroll, text=nome, font=("Arial", 15))
                entrynome.grid(row=i, column=1, pady=5, padx=5)
                entrycpf = ctk.CTkLabel(scroll, text=cpf, font=("Arial", 15))
                entrycpf.grid(row=i, column=2, pady=5, padx=5)
                entryvalor = ctk.CTkLabel(scroll, text=f"R${valor:.2f}", font=("Arial", 15))
                entryvalor.grid(row=i, column=3, pady=5, padx=5)
                entryvencimento = ctk.CTkLabel(scroll, text=str(vencimento), font=("Arial", 15))
                entryvencimento.grid(row=i, column=4, pady=5, padx=5)

    return widgetEditar

def excluir_alunas(janela):
    academia = db.Academia()
    widgetExcluir = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetExcluir.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    widgetExcluir.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    label = ctk.CTkLabel(widgetExcluir, text="Excluir Aluna", font=("Segoe UI Black", 30))
    label.grid(row=0, column=0, columnspan=6, pady=20)

    labelInstrucao = ctk.CTkLabel(widgetExcluir, text="Insira o nome ou CPF da aluna:", font=("Arial", 15))
    labelInstrucao.grid(row=1, column=1, padx=5, pady=10, sticky=E)
    entryExcluir = ctk.CTkEntry(widgetExcluir, font=("Arial", 15), width=300)
    entryExcluir.grid(row=1, column=2, columnspan=2, pady=10)
    botaoPesquisar = ctk.CTkButton(widgetExcluir, text="Buscar", font=("Arial", 15), command=lambda: buscar_alunas())
    botaoPesquisar.grid(row=1, column=4, pady=10, sticky=W)
    
    label_status = ctk.CTkLabel(widgetExcluir, text="", font=("Arial", 15))
        
    entryacao = None
    
    # Função para executar a exclusão
    def executar_exclusao(alunas_listadas, scroll):
        nonlocal entryacao
        if not entryacao:
            label_status.configure(text="Erro: Campo de ID não encontrado.", text_color="red")
            label_status.grid(row=2, column=0, columnspan=6, pady=5)
            return
            
        try:
            id_visual = int(entryacao.get().strip())
            cpf_para_excluir = alunas_listadas[id_visual - 1][1]
        except ValueError:
            label_status.configure(text="Erro: Insira um ID numérico válido.", text_color="red")
            label_status.grid(row=2, column=0, columnspan=6, pady=5)
            return
        except IndexError:
            label_status.configure(text="Erro: ID fora do intervalo da lista.", text_color="red")
            label_status.grid(row=2, column=0, columnspan=6, pady=5)
            return

        # Pop-up de confirmação
        popup_window = ctk.CTkToplevel(widgetExcluir)
        popup_window.title("Confirmação de Exclusão")
        popup_window.geometry("400x150")
        
        labExcluir = ctk.CTkLabel(popup_window, text=f"Deseja realmente excluir {alunas_listadas[id_visual - 1][0]}?", font=("Arial", 15))
        labExcluir.pack(pady=15)
        
        def confirmar():
            nonlocal entryacao
            if entryacao:
                entryacao.destroy()
                entryacao = None
                
            resultado = academia.excluirAluna(cpf_para_excluir)
            
            if resultado:
                confirmar.destroy()
                cancelar.destroy()
                labExcluir.configure(text="Aluna excluída com sucesso.", text_color="green")
            else:
                labExcluir.configure(text="Erro ao excluir aluna ou CPF não encontrado.", text_color="red")
            
            labExcluir.after(2000, lambda: (popup_window.destroy(), buscar_alunas()))
        
        confirmar = ctk.CTkButton(popup_window, text="Confirmar", command=confirmar, fg_color="red")
        confirmar.pack(side="left", padx=20)
        cancelar = ctk.CTkButton(popup_window, text="Cancelar", command=popup_window.destroy)
        cancelar.pack(side="right", padx=20)
        popup_window.grab_set()

    def buscar_alunas():
        nonlocal entryacao
        
        for widget in widgetExcluir.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                widget.destroy()
                
        label_status.configure(text="")
        label_status.grid_forget()
        
        scroll = ctk.CTkScrollableFrame(widgetExcluir, fg_color="transparent")
        scroll.place(relx=0.5, rely=0.6, anchor=CENTER, relwidth=0.9, relheight=0.7)
        scroll.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        alunas = academia.buscarPorNome_ou_Cpf(entryExcluir.get().strip())
        
        # Limpa o campo de ação antigo
        if entryacao:
            entryacao.destroy()
            entryacao = None
            
        if not alunas:
            labelaluna = ctk.CTkLabel(scroll, text="Nenhuma aluna encontrada com essa informação", font=("Arial", 18))
            labelaluna.grid(row=0, column=0, columnspan=6, pady=10, padx=5)
        else:            
            # Cabeçalhos
            labelID = ctk.CTkLabel(scroll, text="ID", font=("Arial", 15))
            labelID.grid(row=0, column=0, pady=5, padx=5)
            labelnome = ctk.CTkLabel(scroll, text="Nome", font=("Arial", 15))
            labelnome.grid(row=0, column=1, pady=5, padx=5)
            labelcpf = ctk.CTkLabel(scroll, text="CPF", font=("Arial", 15))
            labelcpf.grid(row=0, column=2, pady=5, padx=5)
            labelvalor = ctk.CTkLabel(scroll, text="Valor", font=("Arial", 15))
            labelvalor.grid(row=0, column=3, pady=5, padx=5)
            labelvencimento = ctk.CTkLabel(scroll, text="Vencimento", font=("Arial", 15))
            labelvencimento.grid(row=0, column=4, pady=5, padx=5)

            # Campo e Botão de Ação (criados no scroll para centralizar)
            entryacao = ctk.CTkEntry(scroll, placeholder_text="ID", font=("Arial", 12), width=50)
            entryacao.grid(row=0, column=5, pady=5, padx=5, sticky=W)
            
            # Passa a lista de alunas para o comando de exclusão
            botaoEnter = ctk.CTkButton(scroll, text="Excluir", font=("Arial", 12), command=lambda: executar_exclusao(alunas, scroll))
            botaoEnter.grid(row=0, column=5, pady=5, padx=5, sticky=E)

            for i, aluna in enumerate(alunas, start=1):
                nome, cpf, nascimento, valor, vencimento = aluna
                
                entryID = ctk.CTkLabel(scroll, text=str(i), font=("Arial", 15)) # i = ID visual
                entryID.grid(row=i, column=0, pady=5, padx=5)
                entrynome = ctk.CTkLabel(scroll, text=nome, font=("Arial", 15))
                entrynome.grid(row=i, column=1, pady=5, padx=5)
                entrycpf = ctk.CTkLabel(scroll, text=cpf, font=("Arial", 15))
                entrycpf.grid(row=i, column=2, pady=5, padx=5)
                entryvalor = ctk.CTkLabel(scroll, text=f"R${valor:.2f}", font=("Arial", 15))
                entryvalor.grid(row=i, column=3, pady=5, padx=5)
                entryvencimento = ctk.CTkLabel(scroll, text=str(vencimento), font=("Arial", 15))
                entryvencimento.grid(row=i, column=4, pady=5, padx=5)

    return widgetExcluir
  
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
        
        contaVaga = 0
        for i, vaga in enumerate(vagas_do_dia, start=3):
            horario, ocupado, limite, vagas = vaga
            if vagas == 0:
                continue
            else:
                text = f"{horario}h: {ocupado}/{limite} ({vagas} vagas)"
                
                entrytext = ctk.CTkLabel(scroll_frame, text=text, font=("Arial", 15))
                entrytext.grid(row=i, column=j, padx=5, pady=5, sticky='n')
                contaVaga += 1
        
        if contaVaga == 0:
            text = "Todos os horários estão ocupados"
            entrytext = ctk.CTkLabel(scroll_frame, text=text, font=("Arial", 15))
            entrytext.grid(row=3, column=j, padx=5, pady=5, sticky='n')
    return widgetVagas

def mensalidades_vencidas(janela):
    academia = db.Academia()
    widgetMensalidades = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetMensalidades.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    label = ctk.CTkLabel(widgetMensalidades, text="Página de Mensalidades", font=("Segoe UI Black", 30))
    label.pack(pady=100)
    return widgetMensalidades

def pesquisa_alunas(janela):
    academia = db.Academia()
    widgetPesquisa = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetPesquisa.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    widgetPesquisa.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    
    label = ctk.CTkLabel(widgetPesquisa, text="Pesquisar Alunas", font=("Segoe UI Black", 30))
    label.grid(row=0, column=0, columnspan=5, pady=20)
    
    label_pesquisar = ctk.CTkLabel(widgetPesquisa, text="Digite o nome ou CPF da aluna: ", font=("Arial", 15))
    label_pesquisar.grid(row=1, column=1, pady=10, padx=5, sticky=E)
    entry_pesquisar = ctk.CTkEntry(widgetPesquisa, font=("Arial", 15), width=300)
    entry_pesquisar.grid(row=1, column=2, pady=10, padx=5, sticky=W)
    botao_pesquisar = ctk.CTkButton(widgetPesquisa, text="Pesquisar", font=("Arial", 15), command=lambda: pesquisar(widgetPesquisa, entry_pesquisar, academia))
    botao_pesquisar.grid(row=1, column=4, pady=10, sticky=W)
    
    return widgetPesquisa

def pesquisar(widget, entry, academia):
    scroll = ctk.CTkScrollableFrame(widget, fg_color="transparent")
    scroll.place(relx=0.5, rely=0.6, anchor=CENTER, relwidth=0.9, relheight=0.7)
    scroll.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    for widget in scroll.winfo_children():
        if int(widget.grid_info().get("row")) >= 2:
            widget.destroy()
            
    alunas = academia.buscarPorNome_ou_Cpf(entry.get().strip())

    if not alunas:
        labelaluna = ctk.CTkLabel(scroll, text="Nenhuma aluna encontrada com essa informação", font=("Arial", 18))
        labelaluna.grid(row=2, column=0, columnspan=5, pady=10, padx=5)
    else:
        labelnome = ctk.CTkLabel(scroll, text="Nome", font=("Arial", 15))
        labelnome.grid(row=2, column=0, pady=5, padx=5)
        labelcpf = ctk.CTkLabel(scroll, text="CPF", font=("Arial", 15))
        labelcpf.grid(row=2, column=1, pady=5, padx=5)
        labelnascimento = ctk.CTkLabel(scroll, text="Data de Nascimento", font=("Arial", 15))
        labelnascimento.grid(row=2, column=2, pady=5, padx=5)
        labelvalor = ctk.CTkLabel(scroll, text="Valor", font=("Arial", 15))
        labelvalor.grid(row=2, column=3, pady=5, padx=5)
        labelvencimento = ctk.CTkLabel(scroll, text="Vencimento", font=("Arial", 15))
        labelvencimento.grid(row=2, column=4, pady=5, padx=5)
        
        for i, aluna in enumerate(alunas, start=3):
            nome, cpf, nascimento, valor, vencimento = aluna
            
            entrynome = ctk.CTkLabel(scroll, text=nome, font=("Arial", 15))
            entrynome.grid(row=i, column=0, pady=5, padx=5)
            entrycpf = ctk.CTkLabel(scroll, text=cpf, font=("Arial", 15))
            entrycpf.grid(row=i, column=1, pady=5, padx=5)
            entrynascimento = ctk.CTkLabel(scroll, text=nascimento, font=("Arial", 15))
            entrynascimento.grid(row=i, column=2, pady=5, padx=5)
            entryvalor = ctk.CTkLabel(scroll, text=f"R${valor:.2f}", font=("Arial", 15))
            entryvalor.grid(row=i, column=3, pady=5, padx=5)
            entryvencimento = ctk.CTkLabel(scroll, text=str(vencimento), font=("Arial", 15))
            entryvencimento.grid(row=i, column=4, pady=5, padx=5)

def aniversarios_do_mes(janela):
    academia = db.Academia()
    widgetAniversarios = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
    widgetAniversarios.place(relx=0.5, rely=0.58, anchor=CENTER, relwidth=0.9, relheight=0.7)
    widgetAniversarios.grid_columnconfigure((0, 1), weight=1)
    
    label = ctk.CTkLabel(widgetAniversarios, text="Aniversariantes do Mês", font=("Segoe UI Black", 30))
    label.grid(row=0, column=0, columnspan=2, pady=20)
    
    labelniver = ctk.CTkLabel(widgetAniversarios, text="Qual mês deseja verificar:", font=("Arial", 15))
    labelniver.grid(row=1, column=0, pady=10, padx=5, sticky=E)
    entryniver = ctk.CTkComboBox(widgetAniversarios, values=["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], font=("Arial", 15), width=200)
    entryniver.grid(row=1, column=1, pady=10, padx=5, sticky=W)
    entryniver.set("Selecione um mês")
    botao_niver = ctk.CTkButton(widgetAniversarios, text="Verificar", font=("Arial", 15), command=lambda: verificar_aniversariantes())
    botao_niver.grid(row=2, column=0, columnspan=2, pady=10)
    
    meses = {"Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12}
    
    def verificar_aniversariantes():
        scroller = ctk.CTkScrollableFrame(widgetAniversarios, fg_color="transparent")
        scroller.place(relx=0.5, rely=0.68, anchor=CENTER, relwidth=0.9, relheight=0.7)
        scroller.grid_columnconfigure((0, 1), weight=1)
        
        for widget in scroller.winfo_children():
            if int(widget.grid_info().get("row")) >= 3:
                widget.destroy()
        mes = entryniver.get()
        mes_num = meses.get(mes)
        
        if mes == "Selecione um mês":
            labelmsg = ctk.CTkLabel(scroller, text="Por favor, selecione um mês válido.", font=("Arial", 15))
            labelmsg.grid(row=3, column=0, columnspan=2, pady=10)
            return
        
        aniversariantes = academia.aniversariantesMes(mes_num)
        
        if not aniversariantes:
            labelmsg = ctk.CTkLabel(scroller, text=f"Nenhuma aluna faz aniversário em {mes}.", font=("Arial", 15))
            labelmsg.grid(row=3, column=0, columnspan=2, pady=10)
        else:
            labelnome = ctk.CTkLabel(scroller, text="Nome", font=("Arial", 15))
            labelnome.grid(row=3, column=0, pady=5, padx=5)
            labeldata = ctk.CTkLabel(scroller, text="Data de Nascimento", font=("Arial", 15))
            labeldata.grid(row=3, column=1, pady=5, padx=5)
            
            for i, aniversariante in enumerate(aniversariantes, start=4):
                nome, data_nascimento = aniversariante
                
                entrynome = ctk.CTkLabel(scroller, text=nome, font=("Arial", 15))
                entrynome.grid(row=i, column=0, pady=5, padx=5)
                entrydata = ctk.CTkLabel(scroller, text=data_nascimento, font=("Arial", 15))
                entrydata.grid(row=i, column=1, pady=5, padx=5)
    
    return widgetAniversarios

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
    label_titulo = ctk.CTkLabel(widget1, text="Lu Mafra Personal Trainer", font=("Segoe UI Black", 30, "bold"), text_color="light green" if set_theme == "Dark" else "green")
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
    widget3.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    
    #funções de navegação entre páginas
    def autenticacao(janela):
        widgetAutenticacao = ctk.CTkFrame(janela, fg_color="transparent")
        labelUser = ctk.CTkLabel(widgetAutenticacao, text="Usuário:", font=("Segoe UI Black", 20))
        labelUser.grid(row=0, column=0, padx=5, pady=5)
        entryUser = ctk.CTkEntry(widgetAutenticacao, font=("Arial", 20))
        entryUser.grid(row=0, column=1, padx=5, pady=5)
        labelSenha = ctk.CTkLabel(widgetAutenticacao, text="Senha:", font=("Segoe UI Black", 20))
        labelSenha.grid(row=1, column=0, padx=5, pady=5)
        entrySenha = ctk.CTkEntry(widgetAutenticacao, font=("Arial", 20), show="*")
        entrySenha.grid(row=1, column=1, padx=5, pady=5)
        
        botaoLogin = ctk.CTkButton(widgetAutenticacao, image=imageInput_ctk, hover_color= "#292B25", width=imageInput_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: autenticar())
        botaoLogin.grid(row=2, column=0, padx=5, pady=5)
        labelLogin = ctk.CTkLabel(widgetAutenticacao, text="Login", font=("Segoe UI", 12))
        labelLogin.grid(row=3, column=0, padx=5, pady=5, sticky=N)
        
        botao_cadastroUser = ctk.CTkButton(widgetAutenticacao, image= imageFit_ctk, hover_color= "#292B25", width=imageFit_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(cadastroUser))
        botao_cadastroUser.grid(row=2, column=1, padx=5, pady=5)
        labelCadastroUser = ctk.CTkLabel(widgetAutenticacao, text= "Novo Usuário", font= ("Segoe UI", 12))
        labelCadastroUser.grid(row=3, column=1, padx=5, pady=5)
        
        widgetAutenticacao.place(relx=0.35, rely=0.5, anchor=CENTER)
        
        def autenticar():
            academia = db.Academia()
            if  academia.autenticar_usuario_simples(entryUser.get().strip(), entrySenha.get().strip()):
                widgetAutenticacao.destroy()
                go_home()
            else:
                erro_label = ctk.CTkLabel(janela, text="Usuário ou senha incorretos.", text_color="red", font=("Arial", 20))
                erro_label.place(relx=0.36, rely=0.6, anchor=CENTER)
                erro_label.after(2000, erro_label.destroy)
                
        return widgetAutenticacao
    
    def go_home():        
        #Destrói a página ativa
        if app_state["active_page_frame"]:
            app_state["active_page_frame"].destroy()
            app_state["active_page_frame"] = None
            
        #Restaura o layout da "Home"
        widget1.place(relx=0.5, rely=0.15, anchor=CENTER) # Mostra o Título
        widget2.place(relx=0.5, rely=0.6, anchor=CENTER) # Move o Logo para o centro
        widget3.place(relx=0.5, rely=0.3, anchor=CENTER) # Move o Menu para o centro
        labelCadastroAluna.grid(row = 1, column=0, padx=10, pady=5)
        labelEditar.grid(row=1, column=1, padx=10, pady=5)
        labelExcluir.grid(row=1, column=2, padx=10, pady=5)
        labelVagas.grid(row=1, column=3, padx=10, pady=5)
        labelMensalidades.grid(row=1, column=4, padx=10, pady=5)
        labelPesquisa.grid(row=1, column=5, padx=10, pady=5)
        labelAniversarios.grid(row=1, column=6, padx=10, pady=5) 
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
        if page_function == cadastroUser:
            widget2.place(relx=0.5, rely=0.1, anchor=N)
            widget2.configure(width=screen_width * 0.1, height=screen_height * 0.1)
            widget3.place_forget()
        elif page_function == autenticacao:
            widget1.place(relx=0.5, rely=0.15, anchor=CENTER)
            widget2.place(relx=0.65, rely=0.5, anchor=CENTER)
            widget3.place_forget()
        else:
            widget2.place(relx=0.5, rely=0.02, anchor=N)
            widget3.place(relx=0.5, rely=0.17, anchor=N)
            labelCadastroAluna.grid_forget()
            labelEditar.grid_forget()
            labelExcluir.grid_forget()
            labelVagas.grid_forget()
            labelMensalidades.grid_forget()
            labelPesquisa.grid_forget()
            labelAniversarios.grid_forget()
        
        #Muda para a imagem pequena
        if labelImagemPequena:
            label_da_imagem.configure(image=labelImagemPequena)
            
        #Mostra o botão "Início" (na coluna 7 do grid do widget3)
        if page_function != autenticacao:
            botao_inicio.grid(row=0, column=7, padx=10, pady=5)
        else:
            botao_inicio.grid_forget()
        
        #Cria e armazena a nova página
        app_state["active_page_frame"] = page_function(janela)

    #botões do menu
    botao_cadastroAluna = ctk.CTkButton(widget3, image= imageAdd_ctk, hover_color= "#292B25", width=imageAdd_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(cadastro))
    botao_cadastroAluna.grid(row=0, column=0, padx=10, pady=5)
    labelCadastroAluna = ctk.CTkLabel(widget3, text= "Cadastro", font= ("Segoe UI", 18))
    
    botao_editar = ctk.CTkButton(widget3, image= imageEdit_ctk, hover_color= "#292B25", width=imageEdit_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(editar_alunas))
    botao_editar.grid(row=0, column=1, padx=10, pady=5)
    labelEditar = ctk.CTkLabel(widget3, text= "Editar", font= ("Segoe UI", 18))
    
    botao_excluir = ctk.CTkButton(widget3, image= imageRemove_ctk, hover_color= "#292B25", width=imageRemove_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(excluir_alunas))
    botao_excluir.grid(row=0, column=2, padx=10, pady=5)
    labelExcluir = ctk.CTkLabel(widget3, text= "Excluir", font= ("Segoe UI", 18))
    
    botao_vagas = ctk.CTkButton(widget3, image= imageVagas_ctk, hover_color= "#292B25", width=imageVagas_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(vagasDisponiveis))
    botao_vagas.grid(row=0, column=3, padx=10, pady=5)
    labelVagas = ctk.CTkLabel(widget3, text= "Vagas Disponíveis", font= ("Segoe UI", 18))

    botao_mensalidades = ctk.CTkButton(widget3, image= imageVenc_ctk, hover_color= "#292B25", width=imageVenc_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(mensalidades_vencidas))
    botao_mensalidades.grid(row=0, column=4, padx=10, pady=5)
    labelMensalidades = ctk.CTkLabel(widget3, text= "Mensalidades", font= ("Segoe UI", 18))
    
    botao_pesquisa = ctk.CTkButton(widget3, image= imageAlunas_ctk, hover_color= "#292B25", width=imageAlunas_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(pesquisa_alunas))
    botao_pesquisa.grid(row=0, column=5, padx=10, pady=5)
    labelPesquisa = ctk.CTkLabel(widget3, text= "Pesquisar", font= ("Segoe UI", 18))
    
    botao_aniversarios = ctk.CTkButton(widget3, image= imageNiver_ctk, hover_color= "#292B25", width=imageNiver_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(aniversarios_do_mes))
    botao_aniversarios.grid(row=0, column=6, padx=10, pady=5)
    labelAniversarios = ctk.CTkLabel(widget3, text= "Aniversariantes", font= ("Segoe UI", 18))
    
    botao_inicio = ctk.CTkButton(widget3, image= imageHome_ctk, hover_color= "#292B25", width=imageHome_ctk.__sizeof__(), height=botao_altura , text="", fg_color="transparent", command=go_home)
    
    def cadastroUser(janela):
        frameCadastroUser = ctk.CTkFrame(janela, fg_color="transparent", width=1450, height=750)
        frameCadastroUser.place(relx=0.5, rely=0.23, anchor=N)
        widgetCadastroUser = ctk.CTkFrame(frameCadastroUser, fg_color= "transparent", width=1450, height=750)
        widgetCadastroUser.place(relx= 0.5, anchor=N)
        
        labelCadastroUser = ctk.CTkLabel(widgetCadastroUser, text="Cadastro de Usuário", font=("Segoe UI Black",28))
        labelCadastroUser.grid(row=0, column=0, columnspan=9, pady= 30)
        
        #linha 1 - Nome de Usuário, Senha
        labelNomeUser = ctk.CTkLabel(widgetCadastroUser, text="Nome de Usuário:", font=("Segoe UI", 15))
        labelNomeUser.grid(row=1, column=0, pady=10, sticky=E)
        entryNomeUser = ctk.CTkEntry(widgetCadastroUser, font=("Segoe UI", 15))
        entryNomeUser.grid(row=1, column=1, columnspan=3, pady=10, padx=10, sticky=EW)

        labelSenha = ctk.CTkLabel(widgetCadastroUser, text="Senha:", font=("Segoe UI", 15))
        labelSenha.grid(row=1, column=4, pady=10, sticky=E)
        entrySenha = ctk.CTkEntry(widgetCadastroUser, font=("Segoe UI", 15), show="*")
        entrySenha.grid(row=1, column=5, pady=10, padx=5, sticky=W)
        
        labelVoltar = ctk.CTkButton(widgetCadastroUser, image=imageVoltar_ctk, hover_color= "#292B25", width=imageVoltar_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: clear_and_show_page(autenticacao))
        labelVoltar.grid(row = 9, column = 7, pady=10, padx= 10, sticky=E)
        labelContinuar = ctk.CTkButton(widgetCadastroUser, image=imageInput_ctk, hover_color= "#292B25", width=imageInput_ctk.__sizeof__(), height=botao_altura, text="", fg_color="transparent", command=lambda: cadastrar_usuario())
        labelContinuar.grid(row = 9, column = 8, pady=10, padx= 10, sticky=E)
        
        def cadastrar_usuario():
            academia = db.Academia()
            usuario = db.Usuario(entryNomeUser.get().strip())
            usuario.set_password(entrySenha.get().strip())

            if academia.add_usuario_simples(usuario):
                sucesso_label = ctk.CTkLabel(widgetCadastroUser, text="Usuário cadastrado com sucesso!", text_color="green", font=("Arial", 15))
                sucesso_label.grid(row=8, column=0, columnspan=9, pady=10)
                sucesso_label.after(1000, lambda: (sucesso_label.destroy, widgetCadastroUser.destroy(), clear_and_show_page(autenticacao)))
            else:
                erro_label = ctk.CTkLabel(widgetCadastroUser, text="Erro ao cadastrar usuário.", text_color="red", font=("Arial", 15))
                erro_label.grid(row=8, column=0, columnspan=9, pady=10)
                erro_label.after(3000, erro_label.destroy)

        return frameCadastroUser
    
    clear_and_show_page(autenticacao)
    janela.mainloop()

if __name__ == "__main__":
    entrada()