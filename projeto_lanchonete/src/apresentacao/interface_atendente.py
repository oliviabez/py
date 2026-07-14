# interface_atendente.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from .componentes import COR_FUNDO_INTERNO, COR_HEADER, COR_VERMELHO_BK, COR_AMARELO_BK
from .componentes import (
    montar_header, montar_card_stat, montar_abas, 
    botao_principal, botao_secundario, treeview_estilizado
)

class TelaAtendenteView:
    def __init__(self, root, usuario, ao_sair):
        self.root = root
        self.usuario = usuario
        self.ao_sair = ao_sair
        
        self.root.title("BK Express - Painel do Atendente")
        self.root.geometry("1024x600")
        self.root.configure(bg=COR_FUNDO_INTERNO)
        
        self.header = montar_header(self.root, self.usuario, ao_sair=self.ao_sair)
        for child in self.header.winfo_children():
            if isinstance(child, tk.Label) and "Biblioteca" in child.cget("text"):
                child.configure(text="👑  BK Express - Atendente")

        self.conteudo = tk.Frame(self.root, bg=COR_FUNDO_INTERNO)
        self.conteudo.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.area_trabalho = tk.Frame(self.conteudo, bg=COR_FUNDO_INTERNO)
        
        abas = [
            ("Fila de Pedidos", self.tela_fila_producao),
            ("Histórico Geral", self.tela_historico_geral)
        ]
        montar_abas(self.conteudo, abas, cor_fundo=COR_FUNDO_INTERNO)
        self.area_trabalho.pack(fill="both", expand=True, pady=10)
        self.tela_fila_producao()

    def limpar_tela(self):
        for widget in self.area_trabalho.winfo_children():
            widget.destroy()

    def tela_fila_producao(self):
        """Exibe a fila ativa de produção da cozinha"""
        self.limpar_tela()
        
        tk.Label(self.area_trabalho, text="🍳 Fila de Produção da Cozinha", 
                 font=("Arial", 14, "bold"), bg=COR_VERMELHO_BK, fg="#FFFFFF").pack(anchor="w", pady=(0, 10))
        
        pedidos_preparo = 0
        aguardando_retirada = 0
        lista_pedidos = []
        
        try:
            from dados.conexao_singleton import ConexaoSingleton
            conn = ConexaoSingleton.obter_conexao()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status_pedido IN ('Pedido recebido com sucesso', 'Pedido sendo feito')")
            res_p = cursor.fetchone()
            pedidos_preparo = res_p.get('COUNT(*)') if isinstance(res_p, dict) else res_p[0]
            
            cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status_pedido = 'Pedido atrasado'")
            res_a = cursor.fetchone()
            aguardando_retirada = res_a.get('COUNT(*)') if isinstance(res_a, dict) else res_a[0]
            
            cursor.execute("""
                SELECT p.id_pedido, p.numero_pedido, c.nome as nome_cliente, p.status_pedido 
                FROM pedidos p
                JOIN clientes c ON p.id_cliente = c.id_cliente
                WHERE p.status_pedido != 'Pedido entregue'
                ORDER BY p.data_pedido ASC
            """)
            lista_pedidos = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar fila do banco: {e}")

        p_cards = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        p_cards.pack(fill="x", pady=(0, 15))
        montar_card_stat(p_cards, f"{pedidos_preparo}", "Pedidos em Preparo", COR_HEADER)
        montar_card_stat(p_cards, f"{aguardando_retirada}", "Alertas / Atrasados", COR_VERMELHO_BK)

        colunas = [("id", "ID", 50), ("numero", "Nº Pedido", 100), ("cliente", "Cliente", 200), ("itens", "Produtos Selecionados", 350), ("status", "Status Atual", 220)]
        frame_tabela = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        frame_tabela.pack(fill="both", expand=True)
        
        self.tree_fila = treeview_estilizado(frame_tabela, colunas)
        
        if lista_pedidos:
            try:
                for ped in lista_pedidos:
                    if isinstance(ped, dict):
                        id_p, num_p, cliente_p, status_p = ped['id_pedido'], ped['numero_pedido'], ped['nome_cliente'], ped['status_pedido']
                    else:
                        id_p, num_p, cliente_p, status_p = ped[0], ped[1], ped[2], ped[3]
                    
                    cursor.execute("""
                        SELECT ip.quantidade, pr.nome 
                        FROM itens_pedido ip
                        JOIN produtos pr ON ip.id_produto = pr.id_produto
                        WHERE ip.id_pedido = %s
                    """, (id_p,))
                    itens = cursor.fetchall()
                    
                    detalhes = []
                    for it in itens:
                        if isinstance(it, dict):
                            detalhes.append(f"{it['quantidade']}x {it['nome']}")
                        else:
                            detalhes.append(f"{it[0]}x {it[1]}")
                    
                    texto_produtos = ", ".join(detalhes) if detalhes else "Combo Especial BK"
                    
                    self.tree_fila.insert("", "end", iid=id_p, values=(id_p, num_p, cliente_p, texto_produtos, status_p))
            except Exception as e:
                print(f"Erro ao renderizar linhas da fila: {e}")
        
        frame_acoes = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        frame_acoes.pack(fill="x", pady=15)
        
        tk.Label(frame_acoes, text="Alterar Status:", font=("Arial", 11, "bold"), bg=COR_HEADER, fg="#FFFFFF").pack(side="left", padx=(0, 10))
        
        self.cb_status = ttk.Combobox(frame_acoes, values=[
            "Pedido recebido com sucesso", 
            "Pedido sendo feito", 
            "Pedido atrasado", 
            "Pedido entregue"
        ], state="readonly", width=25, font=("Arial", 10))
        self.cb_status.set("Pedido sendo feito")
        self.cb_status.pack(side="left", padx=5)
        
        btn_atualizar = botao_principal(frame_acoes, "⚡ Atualizar Status", self.acao_atualizar_status)
        btn_atualizar.configure(bg=COR_AMARELO_BK)
        btn_atualizar.pack(side="left", padx=10)
        
        btn_refresh = botao_secundario(frame_acoes, "🔄 Atualizar Fila", self.tela_fila_producao)
        btn_refresh.pack(side="right", padx=5)

    def tela_historico_geral(self):
        """Aba secundária para listar absolutamente todos os pedidos"""
        self.limpar_tela()
        tk.Label(self.area_trabalho, text="📋 Histórico Completo de Pedidos", font=("Arial", 14, "bold"), bg=COR_HEADER, fg="#FFFFFF").pack(anchor="w", pady=(0, 10))
        
        colunas = [("numero", "Nº Pedido", 120), ("data", "Data/Hora", 180), ("total", "Total Faturado", 150), ("status", "Status Final", 200)]
        frame = tk.Frame(self.area_trabalho, bg=COR_FUNDO_INTERNO)
        frame.pack(fill="both", expand=True)
        self.tree_historico = treeview_estilizado(frame, colunas)
        
        try:
            from dados.conexao_singleton import ConexaoSingleton
            conn = ConexaoSingleton.obter_conexao()
            cursor = conn.cursor()
            cursor.execute("SELECT numero_pedido, data_pedido, valor_total, status_pedido FROM pedidos ORDER BY data_pedido DESC")
            vendas = cursor.fetchall()
            
            for v in vendas:
                if isinstance(v, dict):
                    self.tree_historico.insert("", "end", values=(v['numero_pedido'], v['data_pedido'], f"R$ {float(v['valor_total']):.2f}", v['status_pedido']))
                else:
                    self.tree_historico.insert("", "end", values=(v[0], v[1], f"R$ {float(v[2]):.2f}", v[3]))
        except Exception as e:
            print(f"Erro no histórico geral: {e}")

    def acao_atualizar_status(self):
        """Atualiza o status e realiza a BAIXA AUTOMÁTICA de estoque caso seja entregue"""
        selecionado = self.tree_fila.selection()
        if not selecionado:
            messagebox.showwarning("Seleção Requerida", "Selecione o pedido na tabela antes de mudar o status!")
            return
            
        id_pedido_banco = selecionado[0]
        novo_status_escolhido = self.cb_status.get()
        
        try:
            from dados.conexao_singleton import ConexaoSingleton
            conn = ConexaoSingleton.obter_conexao()
            cursor = conn.cursor()
            
            # 1. Atualiza o status do pedido mestre
            cursor.execute("""
                UPDATE pedidos 
                SET status_pedido = %s 
                WHERE id_pedido = %s
            """, (novo_status_escolhido, id_pedido_banco))
            
            # 2. SE o status for 'Pedido entregue', fazemos a baixa física no estoque de produtos
            if novo_status_escolhido == "Pedido entregue":
                # Busca as quantidades e IDs dos produtos que pertencem a esse pedido
                cursor.execute("""
                    SELECT id_produto, quantidade 
                    FROM itens_pedido 
                    WHERE id_pedido = %s
                """, (id_pedido_banco,))
                itens_baixar = cursor.fetchall()
                
                for item in itens_baixar:
                    if isinstance(item, dict):
                        id_prod = item.get('id_produto')
                        qtd_vendida = item.get('quantidade')
                    else:
                        id_prod = item[0]
                        qtd_vendida = item[1]
                    
                    # Deduz a quantidade do produto base 
                    
                    try:
                        cursor.execute("""
                            UPDATE produtos 
                            SET estoque = estoque - %s 
                            WHERE id_produto = %s AND estoque >= %s
                        """, (qtd_vendida, id_prod, qtd_vendida))
                    except Exception as sql_err:
                    
                        print(f"[Aviso de Estoque] Verifique o nome da coluna de estoque na tabela produtos: {sql_err}")
            
            conn.commit()
            
            messagebox.showinfo("Sucesso", f"Pedido atualizado para:\n'{novo_status_escolhido}'\nEstoque processado com sucesso!")
            self.tela_fila_producao() 
        except Exception as err:
            messagebox.showerror("Erro de Banco", f"Não foi possível salvar: {err}")


def mostrar_interface_atendente(root, usuario, usuario_service):
    for w in root.winfo_children():
        w.destroy()

    def ao_sair_para_login():
        from apresentacao.login import mostrar_login
        mostrar_login(root, usuario_service)

    TelaAtendenteView(root, usuario, ao_sair=ao_sair_para_login)