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
    label_status.grid(row=2, column=0, columnspan=6, pady=5)
    
    # ⚠️ Mover entryacao para o escopo correto e inicializar com valor None para ser usado
    entryacao = None
    
    # Função para executar a exclusão
    def executar_exclusao(alunas_listadas):
        nonlocal entryacao
        if not entryacao:
            label_status.configure(text="Erro: Campo de ID não encontrado.", text_color="red")
            return
            
        try:
            id_visual = int(entryacao.get().strip())
            # O ID visual é 1-baseado, mas a lista 'alunas_listadas' é 0-baseada.
            cpf_para_excluir = alunas_listadas[id_visual - 1][2]
        except ValueError:
            label_status.configure(text="Erro: Insira um ID numérico válido.", text_color="red")
            return
        except IndexError:
            label_status.configure(text="Erro: ID fora do intervalo da lista.", text_color="red")
            return

        # Pop-up de confirmação
        popup_window = ctk.CTkToplevel(widgetExcluir)
        popup_window.title("Confirmação de Exclusão")
        popup_window.geometry("400x150")
        
        ctk.CTkLabel(popup_window, text=f"Deseja realmente excluir a aluna ID {id_visual}?", font=("Arial", 15)).pack(pady=15)
        
        def confirmar():
            resultado = academia.excluirAluna(cpf_para_excluir)
            popup_window.destroy()
            if resultado:
                label_status.configure(text=f"Aluna ID {id_visual} excluída com sucesso!", text_color="green")
            else:
                label_status.configure(text="Erro ao excluir aluna ou CPF não encontrado.", text_color="red")
            
            label_status.after(2000, lambda: (label_status.configure(text=""), buscar_alunas()))
        
        ctk.CTkButton(popup_window, text="Confirmar", command=confirmar, fg_color="red").pack(side="left", padx=20)
        ctk.CTkButton(popup_window, text="Cancelar", command=popup_window.destroy).pack(side="right", padx=20)
        popup_window.grab_set()


    def buscar_alunas():
        nonlocal entryacao
        label_status.configure(text="")

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
            # ⚠️ ASSUMINDO que a estrutura do retorno do DB é (nome, cpf, nascimento, valor, vencimento)
            
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
            botaoEnter = ctk.CTkButton(scroll, text="Excluir", font=("Arial", 12), command=lambda: executar_exclusao(alunas))
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