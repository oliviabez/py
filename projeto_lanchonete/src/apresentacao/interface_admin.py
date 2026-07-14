# tela_administrador.py
import tkinter as tk
from tkinter import messagebox
from .componentes import COR_FUNDO_INTERNO, COR_VERMELHO_BK
from .componentes import montar_header, montar_abas, botao_principal, botao_secundario, treeview_estilizado, separador

class TelaAdministradorView:
    def __init__(self, root, usuario, ao_sair):
        self.root = root
        self.usuario = usuario
        self.ao_sair = ao_sair
        
        self.root.title("BK Express - Painel de Controle Administrativo")
        self.root.geometry("1024x600")
        self.root.configure(bg=COR_FUNDO_INTERNO)
        
        # Monta o Header e customiza o logo para o tema BK
        self.header = montar_header(self.root, self.usuario, ao_sair=self.ao_sair)
        for child in self.header.winfo_children():
            if isinstance(child, tk.Label) and "Biblioteca" in child.cget("text"):
                child.configure(text="🍔  BK Express - Administrador")

        self.conteudo = tk.Frame(self.root, bg=COR_FUNDO_INTERNO)
        self.conteudo.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.area_trabalho = tk.Frame(self.conteudo, bg=COR_FUNDO_INTERNO)
        
        # Configuração das Abas do Admin (HU03, HU04, HU06, HU07)
        abas = [
            ("Gerenciar Cardápio", self.tela_gerenciar_produtos),
            ("Clientes Cadastrados", self.tela_gerenciar_clientes)
        ]
        montar_abas(self.conteudo, abas, cor_fundo=COR_FUNDO_INTERNO)
        self.area_trabalho.pack(fill="both", expand=True, pady=10)
        self.tela_gerenciar_produtos()

    def limpar_tela(self):
        for widget in self.area_trabalho.winfo_children():
            widget.destroy()

    def tela_gerenciar_produtos(self):
        """HU04, HU06, HU07 - Operações CRUD do Mix de Produtos BK usando ProdutoRepositorio"""
        self.limpar_tela()
        tk.Label(self.area_trabalho, text="Configurações do Cardápio / Produtos", font=("Arial", 14, "bold"), bg=COR_VERMELHO_BK, fg="#FFFFFF").pack(anchor="w", pady=(0, 10))
        
        # Colunas atualizadas de acordo com o SELECT do ProdutoRepositorio
        colunas = [("id", "ID", 50), ("nome", "Produto", 180), ("categoria", "Categoria", 120), ("tamanho", "Tamanho", 80), ("preco", "Preço", 100), ("estoque", "Estoque", 80)]
        frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        frame.pack(fill="both", expand=True)
        
        tree = treeview_estilizado(frame, colunas)
        
        # ---------------------------------------------------------------------
        # UTILIZANDO PRODUTOREPOSITORIO PARA CARREGAR OS DADOS
        # ---------------------------------------------------------------------
        def carregar_produtos_db():
            for item in tree.get_children():
                tree.delete(item)
            try:
                from dados.conexao_singleton import ConexaoSingleton
                from dados.produto_repository import ProdutoRepositorio 
                
                db_conn = ConexaoSingleton.obter_conexao()
                if db_conn:
                    repo = ProdutoRepositorio(db_conn)
                    lista_produtos = repo.listar_todos() # Usa o método listar_todos()
                    
                    if lista_produtos:
                        for prod in lista_produtos:
                            if isinstance(prod, dict):
                                p_id = prod.get('id_produto') or ""
                                p_nome = prod.get('nome') or ""
                                p_cat = prod.get('categoria') or ""
                                p_tam = prod.get('tamanho') or "Único"
                                p_preco = prod.get('preco') or 0.0
                                p_est = prod.get('estoque') or 0
                            else:
                                p_id = prod[0] if len(prod) > 0 else ""
                                p_nome = prod[1] if len(prod) > 1 else ""
                                p_cat = prod[2] if len(prod) > 2 else ""
                                p_tam = prod[3] if len(prod) > 3 else "Único"
                                p_preco = prod[4] if len(prod) > 4 else 0.0
                                p_est = prod[5] if len(prod) > 5 else 0
                                
                            tree.insert("", "end", values=(p_id, p_nome, p_cat, p_tam, f"R$ {float(p_preco):.2f}", p_est))
                        return
            except Exception as e:
                print(f"Aviso ao carregar produtos: {e}")
            
            # Fallback seguro caso o banco esteja vazio
            tree.insert("", "end", values=("1", "Hamburguer Whopper", "Lanche", "Regular", "R$ 18,50", "20"))

        carregar_produtos_db()
        
        btn_frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        btn_frame.pack(fill="x", pady=10)
        
        # HU04 - ADICIONAR PRODUTO VIA REPOSITÓRIO
        def executar_adicionar():
            janela_add = tk.Toplevel(self.area_trabalho)
            janela_add.title("HU04 - Adicionar Produto")
            janela_add.geometry("350x380")
            janela_add.configure(bg=COR_FUNDO_INTERNO)
            janela_add.grab_set()
            
            tk.Label(janela_add, text="Nome do Produto:", bg=COR_FUNDO_INTERNO, font=("Arial", 9, "bold")).pack(pady=(10,0))
            ent_nome = tk.Entry(janela_add, width=30)
            ent_nome.pack()
            
            tk.Label(janela_add, text="Categoria:", bg=COR_FUNDO_INTERNO, font=("Arial", 9, "bold")).pack(pady=(10,0))
            ent_cat = tk.Entry(janela_add, width=30)
            ent_cat.pack()

            tk.Label(janela_add, text="Tamanho (ex: Regular, Grande):", bg=COR_FUNDO_INTERNO, font=("Arial", 9, "bold")).pack(pady=(10,0))
            ent_tam = tk.Entry(janela_add, width=30)
            ent_tam.insert(0, "Regular")
            ent_tam.pack()
            
            tk.Label(janela_add, text="Preço (ex: 18.50):", bg=COR_FUNDO_INTERNO, font=("Arial", 9, "bold")).pack(pady=(10,0))
            ent_preco = tk.Entry(janela_add, width=30)
            ent_preco.pack()

            tk.Label(janela_add, text="Quantidade em Estoque:", bg=COR_FUNDO_INTERNO, font=("Arial", 9, "bold")).pack(pady=(10,0))
            ent_est = tk.Entry(janela_add, width=30)
            ent_est.insert(0, "10")
            ent_est.pack()
            
            def salvar():
                nome, cat, tam, preco, est = ent_nome.get().strip(), ent_cat.get().strip(), ent_tam.get().strip(), ent_preco.get().strip(), ent_est.get().strip()
                if not nome or not cat or not preco or not est:
                    messagebox.showerror("Erro", "Campos obrigatórios vazios.")
                    return
                try:
                    from dados.conexao_singleton import ConexaoSingleton
                    from dados.produto_repository import ProdutoRepositorio
                    conn = ConexaoSingleton.obter_conexao()
                    if conn:
                        repo = ProdutoRepositorio(conn)
                        # Chama método inserir_produto()
                        res = repo.inserir_produto(nome, cat, tam, float(preco), int(est))
                        if res:
                            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                            janela_add.destroy()
                            carregar_produtos_db()
                except Exception as erro:
                    messagebox.showerror("Erro", f"Erro ao salvar: {erro}")
            
            tk.Button(janela_add, text="Salvar no Banco", bg=COR_VERMELHO_BK, fg="#FFFFFF", command=salvar, font=("Arial", 10, "bold")).pack(pady=20)

        # HU06 - ALTERAR PRODUTO VIA REPOSITÓRIO
        def executar_alterar():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("HU06 - Seleção", "Selecione um produto para alterar.")
                return
            valores = tree.item(selecionado)['values']
            p_id, p_nome, p_cat, p_tam, p_preco_str, p_estoque = valores[0], valores[1], valores[2], valores[3], valores[4], valores[5]
            preco_limpo = str(p_preco_str).replace("R$ ", "").replace(",", ".").strip()

            janela_edit = tk.Toplevel(self.area_trabalho)
            janela_edit.title("HU06 - Alterar Item")
            janela_edit.geometry("350x360")
            janela_edit.configure(bg=COR_FUNDO_INTERNO)
            janela_edit.grab_set()
            
            tk.Label(janela_edit, text="Nome:", bg=COR_FUNDO_INTERNO).pack(pady=(5,0))
            ent_n = tk.Entry(janela_edit, width=25)
            ent_n.insert(0, p_nome)
            ent_n.pack()

            tk.Label(janela_edit, text="Categoria:", bg=COR_FUNDO_INTERNO).pack(pady=(5,0))
            ent_c = tk.Entry(janela_edit, width=25)
            ent_c.insert(0, p_cat)
            ent_c.pack()

            tk.Label(janela_edit, text="Tamanho:", bg=COR_FUNDO_INTERNO).pack(pady=(5,0))
            ent_t = tk.Entry(janela_edit, width=25)
            ent_t.insert(0, p_tam)
            ent_t.pack()
            
            tk.Label(janela_edit, text="Preço:", bg=COR_FUNDO_INTERNO).pack(pady=(5,0))
            ent_p = tk.Entry(janela_edit, width=25)
            ent_p.insert(0, preco_limpo)
            ent_p.pack()

            tk.Label(janela_edit, text="Estoque:", bg=COR_FUNDO_INTERNO).pack(pady=(5,0))
            ent_e = tk.Entry(janela_edit, width=25)
            ent_e.insert(0, str(p_estoque))
            ent_e.pack()
            
            def salvar_alt():
                try:
                    from dados.conexao_singleton import ConexaoSingleton
                    from dados.produto_repository import ProdutoRepositorio
                    conn = ConexaoSingleton.obter_conexao()
                    if conn:
                        repo = ProdutoRepositorio(conn)
                        # Chama método atualizar_produto()
                        repo.atualizar_produto(p_id, ent_n.get(), ent_c.get(), ent_t.get(), float(ent_p.get()), int(ent_e.get()))
                        messagebox.showinfo("Sucesso", "Item atualizado!")
                        janela_edit.destroy()
                        carregar_produtos_db()
                except Exception as err:
                    messagebox.showerror("Erro", f"Falha na atualização: {err}")

            tk.Button(janela_edit, text="Confirmar Alterações", bg=COR_VERMELHO_BK, fg="#FFFFFF", command=salvar_alt).pack(pady=10)

        # HU07 - EXCLUIR PRODUTO VIA REPOSITÓRIO
        def executar_remover():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("HU07 - Seleção", "Selecione um produto para remover.")
                return
            valores = tree.item(selecionado)['values']
            p_id, p_nome = valores[0], valores[1]
            
            if messagebox.askokcancel("HU07 - Remover", f"Deseja excluir permanentemente '{p_nome}' do cardápio?"):
                try:
                    from dados.conexao_singleton import ConexaoSingleton
                    from dados.produto_repository import ProdutoRepositorio
                    conn = ConexaoSingleton.obter_conexao()
                    if conn:
                        repo = ProdutoRepositorio(conn)
                        # Chama seu método deletar_produto()
                        repo.deletar_produto(p_id)
                        messagebox.showinfo("Sucesso", "Produto removido!")
                        carregar_produtos_db()
                except Exception as err:
                    messagebox.showerror("Erro", f"Falha ao remover: {err}")

        b1 = botao_principal(btn_frame, "Adicionar Produto", executar_adicionar)
        b1.configure(bg=COR_VERMELHO_BK)
        b1.pack(side="left", padx=5)
        
        botao_secundario(btn_frame, "Alterar Preço/Estoque ", executar_alterar).pack(side="left", padx=5)
        botao_secundario(btn_frame, "Remover Produto ", executar_remover).pack(side="left", padx=5)

    def tela_gerenciar_clientes(self):
        """HU03 - Monitoramento e exclusão de contas de cliente"""
        self.limpar_tela()
        tk.Label(self.area_trabalho, text="Gerenciamento de Clientes da Base", font=("Arial", 14, "bold"), bg=COR_VERMELHO_BK, fg="#FFFFFF").pack(anchor="w", pady=(0, 10))
        
        colunas = [("id", "ID", 60), ("nome", "Nome", 180), ("email", "E-mail", 200), ("codigo", "Código Identificador (HU01)", 150)]
        frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        frame.pack(fill="both", expand=True)
        
        tree = treeview_estilizado(frame, colunas)
        
        try:
            from dados.conexao_singleton import ConexaoSingleton
            db_conn = ConexaoSingleton.obter_conexao()
            if db_conn:
                cursor = db_conn.cursor()
                cursor.execute("SELECT id_cliente, nome, email, codigo_cliente FROM clientes")
                lista_clientes = cursor.fetchall()
                cursor.close()
                
                for cliente in lista_clientes:
                    if isinstance(cliente, dict):
                        c_id = cliente.get('id_cliente') or cliente.get('id') or ""
                        c_nome = cliente.get('nome') or ""
                        c_email = cliente.get('email') or ""
                        c_codigo = cliente.get('codigo_cliente') or ""
                    else:
                        c_id = getattr(cliente, 'id_cliente', getattr(cliente, 'id', ""))
                        c_nome = getattr(cliente, 'nome', "")
                        c_email = getattr(cliente, 'email', "")
                        c_codigo = getattr(cliente, 'codigo_cliente', "")
                        
                    tree.insert("", "end", values=(c_id, c_nome, c_email, c_codigo))
            else:
                tree.insert("", "end", values=("1", "Maria (Mock)", "maria@email.com", "CLI-0001"))
                tree.insert("", "end", values=("2", "Joao (Mock)", "joao@email.com", "CLI-0002"))
        except Exception as e:
            tree.insert("", "end", values=("1", "Maria (Mock)", "maria@email.com", "CLI-0001"))
            tree.insert("", "end", values=("2", "Joao (Mock)", "joao@email.com", "CLI-0002"))
            print(f"Aviso no carregamento: {e}")

        btn_frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        btn_frame.pack(fill="x", pady=10)
        
        def executar_exclusao():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("HU03 - Seleção", "Por favor, selecione um cliente na tabela para excluir.")
                return
                
            valores = tree.item(selecionado)['values']
            id_cliente = valores[0]
            nome_cliente = valores[1]
            
            confirmar = messagebox.askokcancel("HU03 - Exclusão", f"Deseja remover o cliente {nome_cliente} (ID: {id_cliente}) e suas chaves do banco lanchonete_db?")
            if confirmar:
                try:
                    from dados.conexao_singleton import ConexaoSingleton
                    conn = ConexaoSingleton.obter_conexao()
                    if conn:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
                        conn.commit()
                        cur.close()
                        messagebox.showinfo("Sucesso", f"Cliente {nome_cliente} removido com sucesso!")
                        self.tela_gerenciar_clientes()
                except Exception as erro_del:
                    messagebox.showerror("Erro", f"Não foi possível excluir do banco: {erro_del}")

        b_del = botao_principal(btn_frame, "Excluir Cliente", executar_exclusao)
        b_del.configure(bg=COR_VERMELHO_BK)
        b_del.pack(side="left", padx=5)

def mostrar_interface_administrador(root, usuario, usuario_service):
    for w in root.winfo_children():
        w.destroy()

    def ao_sair_para_login():
        from apresentacao.login import mostrar_login
        mostrar_login(root, usuario_service)

    TelaAdministradorView(root, usuario, ao_sair=ao_sair_para_login)