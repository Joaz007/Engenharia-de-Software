import re # Importe a biblioteca de Expressões Regulares
from tkinter import *
import customtkinter as ctk
from PIL import Image
import requests
#cadastro
#fazer comprovante
#verificar mensalidades vencidas
#exibir a lista de alunas
#exibir a lista de alunas por turma
#remover aluna
#editar aluna
#aniversariantes do mês
#alunas com mensalidades atrasadas
#criar um banco de dados

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
    
    #Pega o texto atual e a posição do cursor
    texto_atual = entry.get()
    
    #Limpa o texto, mantendo apenas os dígitos
    numeros = re.sub(r'\D', '', texto_atual)

    #Limita a 11 dígitos (tamanho máximo de um CPF)
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

    #Atualiza o texto no Entry
    entry.delete(0, ctk.END)
    entry.insert(0, novo_texto)
    
def cadastro(janela):
    widgetCadastro = ctk.CTkFrame(janela, fg_color= "transparent", width=1400, height=750)
    widgetCadastro.place(relx=0.5, rely=0.22, anchor=N)
    
    labelCadastro = ctk.CTkLabel(widgetCadastro, text="Cadastro", font=("Arial",30))
    labelCadastro.grid(row=0, column=0, columnspan=9, pady= 30)
    
    desc = BooleanVar()
    entryButtonDesc2 = ctk.CTkRadioButton(widgetCadastro, text="Aluna sem desconto", font=("Arial", 15), variable=desc, value=True)
    entryButtonDesc2.grid(row=0, column=8, pady=10, padx= 10, sticky=W)
    
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

    def verificar_cep(cep):
        labelResp = ctk.CTkLabel(widgetCadastro, text="", font=("Arial", 15))
        labelResp.grid(row=2, column=2, pady=10, sticky=W)
        
        if len(cep) != 8:
            labelResp.configure(text="CEP inválido.")
            labelResp.after(2000, lambda: labelResp.configure(text=""))
        else:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url)
            data = response.json()
            if "erro" in data:
                labelResp.configure(text="CEP não encontrado.")
                labelResp.after(2000, lambda: labelResp.configure(text=""))
            else:
                return data

    labelCEP = ctk.CTkLabel(widgetCadastro, text="CEP:", font=("Arial", 15))
    labelCEP.grid(row=2, column=0, pady=10, sticky=E)
    entryCEP = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryCEP.grid(row=2, column=1, pady=10, padx= 10, sticky=W)

    labelEndereco = ctk.CTkLabel(widgetCadastro, text="Endereço:", font=("Arial", 15))
    labelEndereco.grid(row=2, column=3, pady=10, sticky=E)
    entryEndereco = ctk.CTkEntry(widgetCadastro, font=("Arial", 15), width=250)
    entryEndereco.grid(row=2, column=4, pady=10, padx= 10, sticky=W)
    
    labelBairro = ctk.CTkLabel(widgetCadastro, text="Bairro:", font=("Arial", 15))
    labelBairro.grid(row=2, column=5, pady=10, sticky=E)
    entryBairro = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryBairro.grid(row=2, column=6, pady=10, padx= 10, sticky=W)
    
    def buscar_cep():
        cep = entryCEP.get()
        resultado = verificar_cep(cep)
    
        if isinstance(resultado, dict):
            entryEndereco.insert(0, resultado['logradouro'])        
            entryBairro.insert(0, resultado['bairro'])

    botaoBuscarCEP = ctk.CTkButton(widgetCadastro, text="Buscar CEP", width= 50, command=buscar_cep)
    botaoBuscarCEP.grid(row=2, column=2, pady=10, padx=10, sticky=W)
     
    labelNumero = ctk.CTkLabel(widgetCadastro, text="Celular:", font=("Arial", 15))
    labelNumero.grid(row=2, column=7, pady=10, sticky=E)
    entryNumero = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryNumero.grid(row=2, column=8, pady=10, padx= 10, sticky=W)
    entryNumero.bind("<KeyRelease>", formatar_telefone)

    labelCPF = ctk.CTkLabel(widgetCadastro, text="CPF:", font=("Arial", 15))
    labelCPF.grid(row=3, column=0, pady=10, sticky=E)
    entryCPF = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryCPF.grid(row=3, column=1, pady=10, padx= 10, sticky=W)
    entryCPF.bind("<KeyRelease>", formatar_cpf)
    
    dia_semana = IntVar()
    labelQuantDias = ctk.CTkLabel(widgetCadastro, text="Quantidade de Dias:", font=("Arial", 15))
    labelQuantDias.grid(row=3, column=2, pady=10, padx= 10, sticky=E)
    entry2 = ctk.CTkRadioButton(widgetCadastro, text="2x", font=("Arial", 15), variable=dia_semana, value=2)
    entry2.grid(row=3, column=3, pady=10, sticky=W)
    entry3 = ctk.CTkRadioButton(widgetCadastro, text="3x", font=("Arial", 15), variable=dia_semana, value=3)
    entry3.grid(row=3, column=4, pady=10, padx= 5, sticky=W)

    if desc.get():
        if dia_semana.get() == 2:
            valor = "200,00"
        elif dia_semana.get() == 3:
            valor = "230,00"
    else:
        valor = " " # Valor com desconto a ser definido
    
    labelMensalidade = ctk.CTkLabel(widgetCadastro, text="Valor da Mensalidade:", font=("Arial", 15))
    labelMensalidade.grid(row=3, column=5, pady=10, sticky=E)
    entryMensalidade = ctk.CTkEntry(widgetCadastro, font=("Arial", 15))
    entryMensalidade.grid(row=3, column=6, pady=10, padx= 10, sticky=W)
    entryMensalidade.insert(0, valor)

    widgetVenc = ctk.CTkFrame(janela, fg_color= "transparent", width=1400, height=150)
    widgetVenc.place(relx=0.533, rely=0.5, anchor=NE)
    
    vencimento_var = StringVar()
    labelVencimento = ctk.CTkLabel(widgetVenc, text="Vencimento:", font=("Arial", 15))
    labelVencimento.grid(row=0, column=0, pady=10, padx= 5, sticky=E)
    entryVenc5 = ctk.CTkRadioButton(widgetVenc, text="5", font=("Arial", 15), variable=vencimento_var, value="5")
    entryVenc5.grid(row=0, column=1, pady=10, padx= 5, sticky=W)
    entryVenc10 = ctk.CTkRadioButton(widgetVenc, text="10", font=("Arial", 15), variable=vencimento_var, value="10")
    entryVenc10.grid(row=0, column=2, pady=10, padx= 5, sticky=W)
    entryVenc15 = ctk.CTkRadioButton(widgetVenc, text="15", font=("Arial", 15), variable=vencimento_var, value="15")
    entryVenc15.grid(row=0, column=3, pady=10, padx= 5, sticky=W)
    entryVenc20 = ctk.CTkRadioButton(widgetVenc, text="20", font=("Arial", 15), variable=vencimento_var, value="20")
    entryVenc20.grid(row=0, column=4, pady=10, padx= 5, sticky=W)
    entryVenc25 = ctk.CTkRadioButton(widgetVenc, text="25", font=("Arial", 15), variable=vencimento_var, value="25")
    entryVenc25.grid(row=0, column=5, pady=10, padx= 5, sticky=W)
    entryVenc30 = ctk.CTkRadioButton(widgetVenc, text="30", font=("Arial", 15), variable=vencimento_var, value="30")
    entryVenc30.grid(row=0, column=6, columnspan= 3, pady=10, padx= 5, sticky=W)
    
    widgetTermo = ctk.CTkFrame(janela, fg_color= "transparent", width=1400, height=150)
    widgetTermo.place(relx=0.5, rely=0.55, anchor=N)
    
    labelTermo = ctk.CTkLabel(widgetTermo, text="Termo de Responsabilidade para Prática de Atividade Física", font=("Arial", 25))
    labelTermo.pack(pady=20)
    labelContrato = ctk.CTkLabel(widgetTermo, text="Estou ciente de que é recomendável conversar com um médico antes de aumentar meu nível atual de atividade física, tenho pleno conhecimento da minha atual condição de saúde. Sei também que a realização de atividades físicas pode acarretar algum risco, caso existam problemas clínicos que a contraindiquem total ou parcialmente. Assumo plena responsabilidade por qualquer atividade física praticada sem o atendimento a essa recomendação e DECLARO que aceito as responsabilidades inerentes à participação no treino, bem como isento de qualquer responsabilidade a \"Lu Mafra Personal Trainer\".\n\nConcorda com o Termo de Responsabilidade para Prática de Atividade Física?", font=("Arial", 18), wraplength=1400, justify= "left")
    labelContrato.pack(pady=10)
    
    checkTermo = ctk.CTkCheckBox(widgetTermo, text="Concordo", font=("Arial", 15))
    checkTermo.pack(pady=10, anchor=W)
    
    labelEnviar = ctk.CTkButton(widgetTermo, text="Enviar", font=("Arial", 15))
    labelEnviar.pack(pady=10, anchor=E)

def comprovante(janela):
    widgetComprovante = ctk.CTkFrame(janela, width=1400, height=750)
    widgetComprovante.place(relx=0.5, rely=0.57, anchor=CENTER)
    
def mensalidades_vencidas(janela):
    widgetMensalidades = ctk.CTkFrame(janela, width=1400, height=750)
    widgetMensalidades.place(relx=0.5, rely=0.57, anchor=CENTER)
    
def lista_alunas(janela):
    widgetLista = ctk.CTkFrame(janela, width=1400, height=750)
    widgetLista.place(relx=0.5, rely=0.57, anchor=CENTER)
        
def clear_label(label_frame, botao_cadastro, botao_comprovante, botao_mensalidades, botao_lista, widget1, widget2, widget3, labelImagem):
    widget1.destroy()
    label_frame.configure(text="")
    
    widget2.place(relx=0.5, rely=0.15, anchor= N)
    botao_cadastro.grid(row=0, column=0, padx=5, pady=5)
    botao_comprovante.grid(row=0, column=1, padx=5, pady=5)
    botao_mensalidades.grid(row=0, column=2, padx=5, pady=5)
    botao_lista.grid(row=0, column=3, padx=5, pady=5)
    
    widget3.place(relx=0.5, rely=0.02, anchor= N)
    labelImagem.configure(size=(225,110))

def entrada():
    janela = ctk.CTk()
    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    janela.geometry(f"{screen_width}x{screen_height}+0+0")
    janela.title("Lu Mafra Personal Trainer")
    
    # Frame principal
    widget1 = ctk.CTkFrame(janela, fg_color="transparent")
    widget1.place(relx=0.5, rely=0.25, relwidth=0.8, relheight=0.2, anchor=CENTER)
    
    set_theme = ctk.get_appearance_mode()
    label = ctk.CTkLabel(widget1, text="Lu Mafra Personal Trainer", font=("Arial", 30, "bold"), text_color="light green" if set_theme == "Dark" else "green")
    label.pack()
    
    # Botões ajustados dinamicamente
    botao_largura = int(screen_width * 0.1)
    botao_altura = int(screen_height * 0.05)
    
    widget2 = ctk.CTkFrame(janela, fg_color="transparent")
    widget2.place(relx=0.5, rely=0.30, anchor=CENTER)
    label_frame = ctk.CTkLabel(janela, text="")
    
    botao_cadastro = ctk.CTkButton(widget2, width=botao_largura, height=botao_altura, text="Cadastro", font=("Arial", 18), command=lambda: [clear_label(label_frame, botao_cadastro, botao_comprovante, botao_mensalidades, botao_lista, widget1, widget2, widget3, labelImagem), cadastro(janela)])
    botao_cadastro.grid(row=1, column=0, padx=5, pady=5)
    
    botao_comprovante = ctk.CTkButton(widget2, width=botao_largura, height=botao_altura, text="Comprovante", font=("Arial", 18), command=lambda: [clear_label(label_frame, botao_cadastro, botao_comprovante, botao_mensalidades, botao_lista, widget1, widget2, widget3, labelImagem), comprovante(janela)])
    botao_comprovante.grid(row=1, column=1, padx=5, pady=5)
    
    botao_mensalidades = ctk.CTkButton(widget2, width=botao_largura, height=botao_altura, text="Mensalidades Vencidas", font=("Arial", 18), command=lambda: [clear_label(label_frame, botao_cadastro, botao_comprovante, botao_mensalidades, botao_lista, widget1, widget2, widget3, labelImagem), mensalidades_vencidas(janela)])
    botao_mensalidades.grid(row=1, column=2, padx=5, pady=5)    
    
    botao_lista = ctk.CTkButton(widget2, width=botao_largura, height=botao_altura, text="Lista de Alunas", font=("Arial", 18), command=lambda: [clear_label(label_frame, botao_cadastro, botao_comprovante, botao_mensalidades, botao_lista, widget1, widget2, widget3, labelImagem), lista_alunas(janela)])
    botao_lista.grid(row=1, column=3, padx=5, pady=5)
    
    # Imagem ajustada dinamicamente
    imagem_largura = int(screen_width * 0.3)
    imagem_altura = int(screen_height * 0.15)
    
    widget3 = ctk.CTkFrame(janela, fg_color="transparent", width=900, height=550)
    widget3.place(relx=0.5, rely=0.55, anchor=CENTER)
    
    labelImagem = ctk.CTkImage(
        light_image=Image.open("imagens/lu_mafra.png").resize((imagem_largura, imagem_altura)),
        dark_image=Image.open("imagens/lu_mafra2.png").resize((imagem_largura, imagem_altura)),
        size=(imagem_largura, imagem_altura)
    )
    label = ctk.CTkLabel(widget3, image=labelImagem, text="")
    label.pack()
    
    botao_sair = ctk.CTkButton(janela, text="Sair", command=janela.quit)
    botao_sair.pack(side="bottom", pady=10)
    
    janela.mainloop()
    
if __name__ == "__main__":
    entrada()