# tela_cliente.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from .componentes import COR_FUNDO_INTERNO, COR_HEADER, COR_VERMELHO_BK, COR_AMARELO_BK
from .componentes import (
    montar_header, montar_card_stat, montar_abas, 
    botao_principal, botao_secundario, treeview_estilizado
)

class PedidoDominio:
    def __init__(self, numero_pedido, id_cliente, forma_pagamento, status_pedido, valor_total):
        self.numero_pedido = numero_pedido
        self.id_cliente = id_cliente
        self.forma_pagamento = forma_pagamento
        self.status_pedido = status_pedido
        self.valor_total = valor_total

class ItemPedidoDominio:
    def __init__(self, id_pedido, id_produto, quantidade, tamanho, preco_unitario, subtotal):
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.subtotal = subtotal

class TelaClienteView:
    def __init__(self, root, usuario, ao_sair):
        self.root = root
        self.usuario = usuario
        self.ao_sair = ao_sair
        
        self.root.title("BK Express - Área do Cliente")
        self.root.geometry("1024x600")
        self.root.configure(bg=COR_FUNDO_INTERNO)
        
        self.header = montar_header(self.root, self.usuario, ao_sair=self.ao_sair)
        for child in self.header.winfo_children():
            if isinstance(child, tk.Label) and "Biblioteca" in child.cget("text"):
                child.configure(text="🍔  BK Express - Cliente")

        self.conteudo = tk.Frame(self.root, bg=COR_FUNDO_INTERNO)
        self.conteudo.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.area_trabalho = tk.Frame(self.conteudo, bg=COR_FUNDO_INTERNO)
        
        abas = [
            ("Cardápio", self.tela_cardapio),
            ("Meus Pedidos", self.tela_meus_pedidos)
        ]
        montar_abas(self.conteudo, abas, cor_fundo=COR_FUNDO_INTERNO)
        self.area_trabalho.pack(fill="both", expand=True, pady=10)
        self.tela_cardapio()

    def limpar_tela(self):
        for widget in self.area_trabalho.winfo_children():
            widget.destroy()

    def tela_cardapio(self):
        """Cardápio do Cliente trazendo a coluna de estoque para validação visual oculta"""
        self.limpar_tela()
        tk.Label(self.area_trabalho, text="🍔 Cardápio BK", font=("Arial", 14, "bold"), bg=COR_AMARELO_BK, fg="#FFFFFF").pack(anchor="w", pady=(0, 10))
        
        colunas = [("categoria", "Categoria", 120), ("nome", "Produto", 220), ("tamanho", "Tamanho", 100), ("preco", "Preço", 100)]
        frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        frame.pack(fill="both", expand=True)
        
        self.tree_cardapio = treeview_estilizado(frame, colunas)
        
        try:
            from dados.conexao_singleton import ConexaoSingleton
            conn = ConexaoSingleton.obter_conexao()
            if conn:
                cursor = conn.cursor()
                # Trazemos o estoque junto para validar antes de fechar a compra
                cursor.execute("SELECT id_produto, nome, categoria, tamanho, preco, estoque FROM produtos")
                lista_produtos = cursor.fetchall()
                
                for prod in lista_produtos:
                    if isinstance(prod, dict):
                        p_id = prod.get('id_produto')
                        p_nome = prod.get('nome')
                        p_cat = prod.get('categoria')
                        p_tam = prod.get('tamanho') or "Regular"
                        p_preco = prod.get('preco')
                        p_est = prod.get('estoque', 99)
                    else:
                        p_id, p_nome, p_cat, p_tam, p_preco, p_est = prod[0], prod[1], prod[2], prod[3], prod[4], prod[5]
                        
                    # Salvamos o estoque atual na tag do item para checagem rápida
                    self.tree_cardapio.insert("", "end", iid=p_id, values=(p_cat, p_nome, p_tam, f"R$ {float(p_preco):.2f}"), tags=(str(p_est),))
        except Exception as e:
            print(f"Erro ao carregar cardápio dinâmico: {e}")
            self.tree_cardapio.insert("", "end", iid="1", values=("Sanduíches", "Whopper Especial", "Grande", "R$ 34,90"), tags=("10",))
        
        botoes_container = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        botoes_container.pack(fill="x", pady=10)
        
        lbl_pag = tk.Label(botoes_container, text="Forma de Pagamento:", font=("Arial", 10, "bold"), bg=COR_FUNDO_INTERNO, fg="#FFFFFF")
        lbl_pag.pack(side="right", padx=(10, 5))
        
        self.cb_pagamento = ttk.Combobox(botoes_container, values=["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix"], state="readonly", width=15, font=("Arial", 10))
        self.cb_pagamento.set("Pix")
        self.cb_pagamento.pack(side="right", padx=5)

        lbl_qtd = tk.Label(botoes_container, text="Qtd:", font=("Arial", 10, "bold"), bg=COR_FUNDO_INTERNO, fg="#FFFFFF")
        lbl_qtd.pack(side="right", padx=(15, 5))
        
        self.sp_quantidade = tk.Spinbox(botoes_container, from_=1, to=5, width=5, state="readonly", font=("Arial", 10))
        self.sp_quantidade.pack(side="right", padx=5)

        btn = botao_principal(botoes_container, "🛒 Fazer Pedido", self.acao_criar_pedido)
        btn.configure(bg=COR_VERMELHO_BK) 
        btn.pack(side="right", padx=5)

    def tela_meus_pedidos(self):
        """Histórico de pedidos do cliente em tempo real"""
        self.limpar_tela()
        total_pedidos_hoje = 0
        total_gasto_hoje = 0.0
        historico_pedidos = []
        
        try:
            from dados.conexao_singleton import ConexaoSingleton
            from dados.pedido_repository import PedidoRepositorio
            conn = ConexaoSingleton.obter_conexao()
            if conn:
                repo_pedido = PedidoRepositorio(conn)
                id_cliente = self.usuario.get('id_cliente') or self.usuario.get('id') if isinstance(self.usuario, dict) else getattr(self.usuario, 'id_cliente', getattr(self.usuario, 'id', None))
                email_cliente = self.usuario.get('email') if isinstance(self.usuario, dict) else getattr(self.usuario, 'email', '')
                
                total_pedidos_hoje = repo_pedido.contar_pedidos_cliente_hoje(id_cliente)
                historico_pedidos = repo_pedido.buscar_por_email_cliente(email_cliente)
                
                from datetime import datetime
                hoje_str = datetime.now().strftime("%Y-%m-%d")
                for p in historico_pedidos:
                    if isinstance(p, dict):
                        dt_p, v_p = str(p.get('data_pedido')), float(p.get('valor_total') or 0)
                    else:
                        dt_p, v_p = str(p[3]), float(p[6] or 0)
                    if hoje_str in dt_p:
                        total_gasto_hoje += v_p
        except Exception as e:
            print(f"Erro ao computar estatísticas: {e}")
        
        p_cards = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        p_cards.pack(fill="x", pady=(0, 15))
        montar_card_stat(p_cards, f"{total_pedidos_hoje}", "Pedidos Realizados Hoje", COR_HEADER)
        montar_card_stat(p_cards, f"R$ {total_gasto_hoje:.2f}", "Total Consumido Hoje", COR_VERMELHO_BK)

        colunas = [("numero", "Nº Pedido", 80), ("detalhes", "Item (Qtd)", 180), ("pagamento", "Pagamento", 110), ("data", "Data/Hora", 130), ("valor", "Total", 80), ("status", "Status", 130)]
        frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        frame.pack(fill="both", expand=True)
        
        self.tree_pedidos = treeview_estilizado(frame, colunas)
        
        if historico_pedidos:
            try:
                from dados.conexao_singleton import ConexaoSingleton
                cursor = ConexaoSingleton.obter_conexao().cursor()
                
                for ped in historico_pedidos:
                    if isinstance(ped, dict):
                        id_p, num_p, dt_p, v_tot, st_p, f_pag = ped.get('id_pedido'), ped.get('numero_pedido'), ped.get('data_pedido'), ped.get('valor_total'), ped.get('status_pedido'), ped.get('forma_pagamento')
                    else:
                        id_p, num_p, dt_p, f_pag, st_p, v_tot = ped[0], ped[1], ped[3], ped[4], ped[5], ped[6]
                    
                    cursor.execute("""
                        SELECT ip.quantidade, pr.nome 
                        FROM itens_pedido ip 
                        LEFT JOIN produtos pr ON ip.id_produto = pr.id_produto 
                        WHERE ip.id_pedido = %s LIMIT 1
                    """, (id_p,))
                    item_info = cursor.fetchone()
                    
                    if item_info:
                        qtd_item = item_info.get('quantidade') if isinstance(item_info, dict) else item_info[0]
                        nome_item = item_info.get('nome') if isinstance(item_info, dict) else item_info[1]
                        detalhes_texto = f"{nome_item} ({qtd_item}x)" if nome_item else "Pedido Lanchonete"
                    else:
                        detalhes_texto = "Pedido Lanchonete"
                    
                    self.tree_pedidos.insert("", "end", iid=id_p, values=(num_p, detalhes_texto, f_pag, dt_p, f"R$ {float(v_tot):.2f}", st_p))
            except Exception as e:
                print(f"Erro ao tratar exibição de itens na árvore: {e}")

        btn_frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        btn_frame.pack(fill="x", pady=10)
        
        botao_principal(btn_frame, "➕ Novo Pedido", self.tela_cardapio).pack(side="left", padx=5)
        botao_secundario(btn_frame, " Alterar (Até 20 min)", self.acao_alterar_pedido).pack(side="left", padx=5)

    def acao_criar_pedido(self):
        """Valida o estoque disponível do BK antes de permitir a criação do pedido"""
        try:
            selecionado = self.tree_cardapio.selection()
            forma_escolhida = self.cb_pagamento.get()
            qtd_escolhida = int(self.sp_quantidade.get())
        except AttributeError:
            return

        if not selecionado:
            messagebox.showwarning("Seleção", "Por favor, escolha um item do cardápio para fazer o pedido!")
            return

        id_produto = selecionado[0]
        # Resgata o estoque que guardamos nas tags do Treeview
        estoque_atual = int(self.tree_cardapio.item(id_produto)['tags'][0])

        if qtd_escolhida > estoque_atual:
            messagebox.showerror("Falta de Estoque", f"Desculpe! Só temos {estoque_atual} unidades deste item disponíveis em estoque no momento.")
            return

        valores = self.tree_cardapio.item(id_produto)['values']
        nome_produto, tamanho_produto = valores[1], valores[2]
        preco_unitario = float(str(valores[3]).replace("R$ ", "").replace(",", ".").strip())
        valor_total_pedido = preco_unitario * qtd_escolhida
        
        id_cliente = self.usuario.get('id_cliente') or self.usuario.get('id') if isinstance(self.usuario, dict) else getattr(self.usuario, 'id_cliente', getattr(self.usuario, 'id', None))
        codigo_cliente = self.usuario.get('codigo_cliente') if isinstance(self.usuario, dict) else self.usuario.codigo_cliente

        confirmar = messagebox.askyesno("Confirmar", f"Deseja confirmar o pedido de:\n{qtd_escolhida}x {nome_produto}\nTotal: R$ {valor_total_pedido:.2f}?")
        if confirmar:
            try:
                from dados.conexao_singleton import ConexaoSingleton
                from dados.pedido_repository import PedidoRepositorio
                from dados.item_pedido_repository import ItemPedidoRepository
                
                conn = ConexaoSingleton.obter_conexao()
                if conn:
                    repo_pedido = PedidoRepositorio(conn)
                    repo_item = ItemPedidoRepository(conn)
                    numero_diario = repo_pedido.gerar_numero_pedido()
                    
                    novo_pedido = PedidoDominio(numero_diario, id_cliente, forma_escolhida, "Pedido recebido com sucesso", valor_total_pedido)
                    id_pedido_gerado = repo_pedido.inserir(novo_pedido)
                    
                    if id_pedido_gerado:
                        novo_item = ItemPedidoDominio(id_pedido_gerado, id_produto, qtd_escolhida, tamanho_produto, preco_unitario, valor_total_pedido)
                        if repo_item.inserir(novo_item):
                            messagebox.showinfo("Sucesso", f"Pedido Criado!\nSenha da fila: {numero_diario}")
                            self.tela_meus_pedidos()
            except Exception as err:
                messagebox.showerror("Erro", f"Erro crítico: {err}")

    def acao_alterar_pedido(self):
        """Altera o pedido validando estoque caso o cliente peça mais itens"""
        try:
            selecionado = self.tree_pedidos.selection()
        except AttributeError:
            return

        if not selecionado:
            messagebox.showwarning("Alterar", "Selecione um pedido do seu histórico para alterar!")
            return

        id_pedido_selecionado = selecionado[0]
        
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Alterar Pedido")
        janela_edicao.geometry("360x220")
        janela_edicao.configure(bg=COR_FUNDO_INTERNO)
        janela_edicao.grab_set()

        tk.Label(janela_edicao, text="Ajustar Detalhes do Pedido", font=("Arial", 11, "bold"), bg=COR_AMARELO_BK, fg="#FFFFFF").pack(fill="x", pady=(0, 15))

        frame_q = tk.Frame(janela_edicao, bg=COR_FUNDO_INTERNO)
        frame_q.pack(fill="x", padx=20, pady=5)
        tk.Label(frame_q, text="Nova Quantidade:", font=("Arial", 10), bg=COR_FUNDO_INTERNO, fg="#FFFFFF").pack(side="left")
        sp_nova_qtd = tk.Spinbox(frame_q, from_=1, to=5, width=5, state="readonly")
        sp_nova_qtd.pack(side="right")

        frame_p = tk.Frame(janela_edicao, bg=COR_FUNDO_INTERNO)
        frame_p.pack(fill="x", padx=20, pady=5)
        tk.Label(frame_p, text="Forma de Pagamento:", font=("Arial", 10), bg=COR_FUNDO_INTERNO, fg="#FFFFFF").pack(side="left")
        cb_novo_pag = ttk.Combobox(frame_p, values=["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix"], state="readonly", width=15)
        cb_novo_pag.set("Pix")
        cb_novo_pag.pack(side="right")

        def salvar_alteracoes():
            try:
                nova_qtd = int(sp_nova_qtd.get())
                nova_forma = cb_novo_pag.get()
                
                from dados.conexao_singleton import ConexaoSingleton
                conn = ConexaoSingleton.obter_conexao()
                cursor = conn.cursor()
                
                # Busca as informações atuais do produto no pedido
                cursor.execute("SELECT id_produto, quantidade, preco_unitario FROM itens_pedido WHERE id_pedido = %s LIMIT 1", (id_pedido_selecionado,))
                res = cursor.fetchone()
                if res:
                    id_prod = res.get('id_produto') if isinstance(res, dict) else res[0]
                    qtd_antiga = res.get('quantidade') if isinstance(res, dict) else res[1]
                    preco_un = float(res.get('preco_unitario') if isinstance(res, dict) else res[2])
                    
                    # Se ele está aumentando a quantidade, checa se a cozinha tem estoque físico reserva
                    if nova_qtd > qtd_antiga:
                        diferenca = nova_qtd - qtd_antiga
                        cursor.execute("SELECT estoque FROM produtos WHERE id_produto = %s", (id_prod,))
                        res_est = cursor.fetchone()
                        est_disponivel = res_est.get('estoque') if isinstance(res_est, dict) else res_est[0]
                        
                        if diferenca > est_disponivel:
                            messagebox.showerror("Sem Estoque", f"Não há insumos suficientes para aumentar o pedido em +{diferenca} unidades.")
                            return
                    
                    novo_total = preco_un * nova_qtd
                    cursor.execute("UPDATE pedidos SET forma_pagamento = %s, valor_total = %s WHERE id_pedido = %s", (nova_forma, novo_total, id_pedido_selecionado))
                    cursor.execute("UPDATE itens_pedido SET quantidade = %s, subtotal = %s WHERE id_pedido = %s", (nova_qtd, novo_total, id_pedido_selecionado))
                    conn.commit()
                    
                    messagebox.showinfo("Sucesso", "Pedido modificado com sucesso!")
                    janela_edicao.destroy()
                    self.tela_meus_pedidos()
            except Exception as ex:
                messagebox.showerror("Erro", f"Falha ao modificar: {ex}")

        tk.Button(janela_edicao, text="💾 Salvar Alterações", font=("Arial", 10, "bold"), fg="#FFFFFF", bg=COR_VERMELHO_BK, command=salvar_alteracoes, relief="flat", cursor="hand2").pack(pady=20)


def mostrar_interface_cliente(root, usuario, usuario_service):
    for w in root.winfo_children():
        w.destroy()
    def ao_sair_para_login():
        from apresentacao.login import mostrar_login
        mostrar_login(root, usuario_service)
    TelaClienteView(root, usuario, ao_sair=ao_sair_para_login)