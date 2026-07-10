# login.py — Tela de Login e Cadastro (BK Design — US01, US02)
"""
Tela única com duas abas: ENTRAR e CADASTRAR-SE.
Redireciona Clientes, Atendentes e Administradores para suas respectivas interfaces.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

# =========================================================================
# PALETA DE CORES — IDENTIDADE BURGER KING 
# =========================================================================
COR_HEADER = "#120000"              # Marrom Grelhado BK (Escuro)
COR_FUNDO_ESCURO = "#120000"        # Fundo geral da tela
COR_FUNDO_CARD_LOGIN = "#FDF2E2"    # Creme suave / Off-white BK
COR_VERMELHO_BK = "#DA291C"         # Vermelho oficial BK
COR_AMARELO_BK = "#F2A900"          # Amarelo/Mostarda oficial BK
COR_TEXTO_CLARO = "#FFFFFF"
COR_CAMPO_FUNDO = "#FFFFFF"
COR_CAMPO_TEXTO = "#120000"
COR_BORDA_CAMPO = "#706352"
COR_TEXTO_SECUNDARIO = "#706352"
COR_LINHA_ABA = "#DA291C"           

# =========================================================================
# CONFIGURAÇÃO DE FONTES
# =========================================================================
FONTE_TITULO_GRANDE = ("Arial Black", 20, "bold")
FONTE_SUBTITULO = ("Arial", 9, "bold")
FONTE_LABEL = ("Arial Black", 9)
FONTE_CAMPO = ("Arial", 10)
FONTE_BOTAO = ("Arial Black", 11)
FONTE_ABA = ("Arial Black", 11)

class UsuarioObjeto:
    """Classe utilitária para converter o dicionário do banco em objeto com atributos."""
    def __init__(self, dicionario, tipo):
        self.tipo = tipo
        # Copia todas as chaves do dicionário como atributos (ex: nome, email, senha)
        for chave, valor in dicionario.items():
            setattr(self, chave, valor)
        
        # Garante compatibilidade caso a outra tela busque especificamente por 'nome' ou 'usuario'
        if 'nome' not in dicionario and 'usuario' in dicionario:
            self.nome = dicionario['usuario']
        if 'nome' not in dicionario and 'email' in dicionario:
            self.nome = dicionario['email']

def _obter_conexao_direta():
    """Busca a conexão ativa usando o singleton nativo do projeto."""
    try:
        from dados.conexao_singleton import ConexaoSingleton
        return ConexaoSingleton.obter_conexao()
    except Exception:
        try:
            from dados.conexao_factory import ConexaoFactory
            return ConexaoFactory.criar_conexao()
        except Exception:
            return None

def mostrar_login(root, usuario_service):
    """Renderiza a tela de login/cadastro na janela root."""
    for w in root.winfo_children():
        w.destroy()

    root.configure(bg=COR_FUNDO_ESCURO)
    root.geometry("700x640")
    root.title("Burger King Express")

    # --- Topo / Branding -----------------------------------------------------
    topo = tk.Frame(root, bg=COR_FUNDO_ESCURO)
    topo.pack(pady=(30, 10))

    tk.Label(topo, text="🍔", font=("Arial", 32), bg=COR_FUNDO_ESCURO, fg=COR_AMARELO_BK).pack()
    tk.Label(topo, text="BK Express", font=FONTE_TITULO_GRANDE, bg=COR_FUNDO_ESCURO, fg=COR_TEXTO_CLARO).pack()
    tk.Label(topo, text="SISTEMA DE GESTÃO E PEDIDOS", font=FONTE_SUBTITULO, bg=COR_FUNDO_ESCURO, fg=COR_TEXTO_SECUNDARIO).pack(pady=(2, 0))

    # --- Alternador de Abas --------------------------------------------------
    frame_abas = tk.Frame(root, bg=COR_FUNDO_ESCURO)
    frame_abas.pack(pady=(15, 0))

    lbl_entrar   = tk.Label(frame_abas, text="ENTRAR", font=FONTE_ABA, bg=COR_FUNDO_ESCURO, fg=COR_AMARELO_BK, cursor="hand2", padx=20)
    lbl_cadastro = tk.Label(frame_abas, text="CADASTRAR-SE", font=FONTE_ABA, bg=COR_FUNDO_ESCURO, fg=COR_TEXTO_SECUNDARIO, cursor="hand2", padx=20)
    lbl_entrar.grid(row=0, column=0)
    lbl_cadastro.grid(row=0, column=1)

    linha_entrar   = tk.Frame(frame_abas, height=3, width=120, bg=COR_LINHA_ABA)
    linha_cadastro = tk.Frame(frame_abas, height=3, width=120, bg=COR_FUNDO_ESCURO)
    linha_entrar.grid(row=1, column=0, sticky="ew")
    linha_cadastro.grid(row=1, column=1, sticky="ew")

    # --- Card de Conteúdo ----------------------------------------------------
    card = tk.Frame(root, bg=COR_FUNDO_CARD_LOGIN, padx=30, pady=24)
    card.pack(padx=60, pady=10, fill="x")

    conteudo = tk.Frame(card, bg=COR_FUNDO_CARD_LOGIN)
    conteudo.pack(fill="x")

    # =========================================================================
    # ABA: ENTRAR
    # =========================================================================
    def montar_entrar():
        for w in conteudo.winfo_children():
            w.destroy()

        lbl_entrar.configure(fg=COR_AMARELO_BK)
        lbl_cadastro.configure(fg=COR_TEXTO_SECUNDARIO)
        linha_entrar.configure(bg=COR_LINHA_ABA)
        linha_cadastro.configure(bg=COR_FUNDO_ESCURO)

        def campo(rotulo, placeholder, oculto=False):
            tk.Label(conteudo, text=rotulo, font=FONTE_LABEL, bg=COR_FUNDO_CARD_LOGIN, fg=COR_HEADER).pack(anchor="w", pady=(10, 3))
            e = tk.Entry(conteudo, font=FONTE_CAMPO, bg=COR_CAMPO_FUNDO, fg=COR_CAMPO_TEXTO, relief="solid", bd=1)
            e.insert(0, placeholder)
            e.configure(fg="#888888")

            def on_focus_in(ev):
                if e.get() == placeholder:
                    e.delete(0, tk.END)
                    e.configure(fg=COR_CAMPO_TEXTO)
                    if oculto: e.configure(show="•")

            def on_focus_out(ev):
                if not e.get():
                    if oculto: e.configure(show="")
                    e.insert(0, placeholder)
                    e.configure(fg="#888888")

            e.bind("<FocusIn>", on_focus_in)
            e.bind("<FocusOut>", on_focus_out)
            e.pack(fill="x", ipady=8)
            return e

        e_usuario = campo("E-MAIL / USUÁRIO", "Digite seu e-mail ou usuário do sistema")
        e_senha = campo("SENHA", "••••••••", oculto=True)

        tk.Label(conteudo, text="ACESSAR COMO:", font=FONTE_LABEL, bg=COR_FUNDO_CARD_LOGIN, fg=COR_HEADER).pack(anchor="w", pady=(12, 3))

        tipo_login_var = tk.StringVar(value="cliente")
        frame_radio = tk.Frame(conteudo, bg=COR_FUNDO_CARD_LOGIN)
        frame_radio.pack(anchor="w", fill="x")

        tk.Radiobutton(frame_radio, text="Cliente", variable=tipo_login_var, value="cliente", bg=COR_FUNDO_CARD_LOGIN, fg=COR_HEADER, font=FONTE_SUBTITULO).pack(side="left", padx=(0, 15))
        tk.Radiobutton(frame_radio, text="Atendente", variable=tipo_login_var, value="atendente", bg=COR_FUNDO_CARD_LOGIN, fg=COR_HEADER, font=FONTE_SUBTITULO).pack(side="left", padx=(0, 15))
        tk.Radiobutton(frame_radio, text="Admin", variable=tipo_login_var, value="administrador", bg=COR_FUNDO_CARD_LOGIN, fg=COR_HEADER, font=FONTE_SUBTITULO).pack(side="left")

        def fazer_login():
            identificador = e_usuario.get().strip()
            senha = e_senha.get().strip()
            tipo_login = tipo_login_var.get().lower().strip()

            if identificador == "Digite seu e-mail ou usuário do sistema": identificador = ""
            if senha == "••••••••": senha = ""
                
            if not identificador or not senha:
                messagebox.showerror("Erro de Validação", "Por favor, preencha todos os campos.")
                return

            db_conn = _obter_conexao_direta()
            if db_conn:
                try:
                    cursor = db_conn.cursor()
                    
                    if "cliente" in tipo_login:
                        cursor.execute("SELECT * FROM clientes WHERE email = %s AND senha = %s", (identificador, senha))
                    elif "atendente" in tipo_login:
                        cursor.execute("SELECT * FROM atendentes WHERE usuario = %s AND senha = %s", (identificador, senha))
                    else:
                        cursor.execute("SELECT * FROM administradores WHERE usuario = %s AND senha = %s", (identificador, senha))
                    
                    row = cursor.fetchone()
                    cursor.close()
                    
                    if row:
                        # Se o retorno for um dicionário puro, nós envelopamos ele na classe utilitária
                        if isinstance(row, dict):
                            usuario_adaptado = UsuarioObjeto(row, tipo_login)
                        else:
                            # Caso venha como tupla/objeto, tentamos mapear diretamente
                            usuario_adaptado = row
                            
                        _redirecionar(root, usuario_adaptado, usuario_service, tipo_login)
                    else:
                        messagebox.showerror("Erro de Login", "Credenciais incorretas para o perfil selecionado.")
                except Exception as err:
                    messagebox.showerror("Erro de Login", f"Falha na autenticação: {str(err)}")
            else:
                messagebox.showerror("Erro de Login", "A base de dados não pôde ser acessada.")

        tk.Button(conteudo, text="ENTRAR", command=fazer_login, bg=COR_VERMELHO_BK, fg=COR_TEXTO_CLARO, font=FONTE_BOTAO, relief="flat", cursor="hand2", pady=10).pack(fill="x", pady=(20, 0))

    # =========================================================================
    # ABA: CADASTRAR-SE
    # =========================================================================
    def montar_cadastro():
        for w in conteudo.winfo_children():
            w.destroy()

        lbl_entrar.configure(fg=COR_TEXTO_SECUNDARIO)
        lbl_cadastro.configure(fg=COR_AMARELO_BK)
        linha_entrar.configure(bg=COR_FUNDO_ESCURO)
        linha_cadastro.configure(bg=COR_LINHA_ABA)

        def campo(rotulo, placeholder, oculto=False):
            tk.Label(conteudo, text=rotulo, font=FONTE_LABEL, bg=COR_FUNDO_CARD_LOGIN, fg=COR_HEADER).pack(anchor="w", pady=(10, 3))
            e = tk.Entry(conteudo, font=FONTE_CAMPO, bg=COR_CAMPO_FUNDO, fg=COR_CAMPO_TEXTO, relief="solid", bd=1)
            e.insert(0, placeholder)
            e.configure(fg="#888888")

            def on_in(ev):
                if e.get() == placeholder:
                    e.delete(0, tk.END)
                    e.configure(fg=COR_CAMPO_TEXTO)
                    if oculto: e.configure(show="•")

            def on_out(ev):
                if not e.get():
                    if oculto: e.configure(show="")
                    e.insert(0, placeholder)
                    e.configure(fg="#888888")

            e.bind("<FocusIn>", on_in)
            e.bind("<FocusOut>", on_out)
            e.pack(fill="x", ipady=8)
            return e

        e_nome = campo("NOME COMPLETO *", "Seu nome completo")
        e_identificador = campo("E-MAIL / USUÁRIO *", "seu.email@gmail.com ou usuario")
        e_senha = campo("SENHA * (mín. 5 caracteres)", "••••••••", oculto=True)
        
        tk.Label(conteudo, text="Nota: Para novos clientes, o código único será gerado automaticamente.", font=("Arial", 8, "italic"), bg=COR_FUNDO_CARD_LOGIN, fg=COR_VERMELHO_BK).pack(anchor="w", pady=(4, 5))
        tk.Label(conteudo, text="TIPO DE USUÁRIO *", font=FONTE_LABEL, bg=COR_FUNDO_CARD_LOGIN, fg=COR_HEADER).pack(anchor="w", pady=(10, 3))

        tipo_var = tk.StringVar()
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Cadastro.TCombobox", 
            font=FONTE_CAMPO, 
            foreground=COR_CAMPO_TEXTO, 
            fieldbackground=COR_CAMPO_FUNDO, 
            background=COR_FUNDO_CARD_LOGIN, 
            bordercolor=COR_BORDA_CAMPO, 
            arrowcolor=COR_HEADER, 
            padding=8
        )
        style.map(
            "Cadastro.TCombobox",
            fieldbackground=[("readonly", COR_CAMPO_FUNDO), ("focus", COR_CAMPO_FUNDO), ("active", COR_CAMPO_FUNDO)],
            foreground=[("readonly", COR_CAMPO_TEXTO), ("focus", COR_CAMPO_TEXTO), ("active", COR_CAMPO_TEXTO)]
        )

        combo_tipo = ttk.Combobox(conteudo, textvariable=tipo_var, values=["cliente", "atendente", "administrador"], state="readonly", style="Cadastro.TCombobox")
        combo_tipo.current(0)
        combo_tipo.pack(fill="x", ipady=7)

        def criar_conta():
            nome = e_nome.get().strip()
            identificador = e_identificador.get().strip()
            senha = e_senha.get().strip()
            tipo_usuario = tipo_var.get().lower().strip()

            for ph in ("Seu nome completo", "seu.email@gmail.com ou usuario", "••••••••"):
                if nome == ph: nome = ""
                if identificador == ph: identificador = ""
                if senha == ph: senha = ""
                
            if not nome or not identificador or not senha:
                messagebox.showerror("Erro no Cadastro", "Campos obrigatórios não preenchidos.")
                return
                
            db_conn = _obter_conexao_direta()
            if db_conn:
                try:
                    cursor = db_conn.cursor()
                    if "cliente" in tipo_usuario:
                        cod_cli = f"CLI-{random.randint(1000, 9999)}"
                        sql = "INSERT INTO clientes (nome, email, senha, codigo_cliente) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (nome, identificador, senha, cod_cli))
                    elif "atendente" in tipo_usuario:
                        sql = "INSERT INTO atendentes (nome, usuario, senha) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (nome, identificador, senha))
                    else:
                        sql = "INSERT INTO administradores (nome, usuario, senha) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (nome, identificador, senha))
                        
                    db_conn.commit()
                    cursor.close()
                    messagebox.showinfo("Sucesso", f"Cadastro de {tipo_usuario.upper()} concluído com sucesso!")
                    montar_entrar()
                except Exception as erro:
                    messagebox.showerror("Erro no Cadastro", f"Falha ao salvar dados: {str(erro)}")
            else:
                messagebox.showerror("Erro no Cadastro", "Não foi possível estabelecer uma conexão estável com o MySQL.")

        tk.Button(conteudo, text="CRIAR CONTA", command=criar_conta, bg=COR_VERMELHO_BK, fg=COR_TEXTO_CLARO, font=FONTE_BOTAO, relief="flat", cursor="hand2", pady=10).pack(fill="x", pady=(18, 0))

    lbl_entrar.bind("<Button-1>", lambda e: montar_entrar())
    lbl_cadastro.bind("<Button-1>", lambda e: montar_cadastro())
    montar_entrar()

def _redirecionar(root, usuario, usuario_service, tipo_login):
    """Encaminha o usuário para a interface correta fornecendo um objeto compatível com pontos."""
    tipo = tipo_login.lower().strip()
    try:
        if "cliente" in tipo:
            from apresentacao.interface_cliente import mostrar_interface_cliente
            mostrar_interface_cliente(root, usuario, usuario_service)
        elif "atendente" in tipo:
            from apresentacao.interface_atendente import mostrar_interface_atendente
            mostrar_interface_atendente(root, usuario, usuario_service)
        elif "admin" in tipo or "administrador" in tipo:
            from apresentacao.interface_admin import mostrar_interface_administrador
            mostrar_interface_administrador(root, usuario, usuario_service)
        else:
            raise ValueError("Perfil selecionado inválido.")
    except Exception as err:
        messagebox.showerror("Erro de Redirecionamento", f"Não foi possível carregar a tela do {tipo}: {str(err)}")