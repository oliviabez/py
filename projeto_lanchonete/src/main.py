# main.py — Ponto de entrada da aplicação BK Express.


import sys
import os
import tkinter as tk

# Garante que o Python reconheça a pasta raiz do projeto nos caminhos de busca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dados.conexao_singleton       import ConexaoSingleton
from src.dados.cliente_repository      import ClienteRepositorio
from src.dados.funcionarios_repository import FuncionarioRepositorio
from src.dados.produto_repository      import ProdutoRepositorio
from src.dados.pedido_repository       import PedidoRepositorio
from src.dados.item_pedido_repository  import ItemPedidoRepository

from src.negocio.autenticacao_service  import AutenticacaoService
from src.negocio.pedido_service        import PedidoService

from src.apresentacao.login            import mostrar_login


def principal() -> None:
    print("PASSO 1: Tentando inicializar o sistema...")
    
    # --- Configuração e Abertura do Banco de Dados ---------------------------
    try:
        conexao = ConexaoSingleton.obter_conexao()
        print(" PASSO 2: Banco de dados conectado!")
    except Exception as erro:
        print("\n ERRO CRÍTICO NA CONEXÃO COM O BANCO:")
        print(erro)
        print("\n----------------------------------------")
        return

    # --- Inicialização dos Repositórios --------------------------------------
    repo_cliente      = ClienteRepositorio(conexao)
    repo_atendente    = FuncionarioRepositorio(conexao)
    repo_admin        = FuncionarioRepositorio(conexao)
    repo_produto      = ProdutoRepositorio(conexao)
    repo_pedido       = PedidoRepositorio(conexao)
    repo_item_pedido  = ItemPedidoRepository(conexao)
    
    print(" PASSO 3: Todos os repositórios foram lidos com sucesso!")

    # --- Inicialização dos Services (Regras de Negócio) ----------------------
    autenticacao_service = AutenticacaoService(conexao)
    pedido_service       = PedidoService(conexao)

    # --- Inicialização dos Services (Regras de Negócio) ----------------------
    autenticacao_service = AutenticacaoService(conexao)
    pedido_service       = PedidoService(conexao)

    # --- Injeção de Dependências nas Telas Secundárias ------------------------
    import src.apresentacao.interface_cliente       as _ic
    import src.apresentacao.interface_atendente     as _iat
    import src.apresentacao.interface_admin as _iad

    _orig_cliente = _ic.mostrar_interface_cliente
    def _cliente_injetado(root, usuario, auth_s):
        _orig_cliente(root, usuario, auth_s, pedido_service)
    _ic.mostrar_interface_cliente = _cliente_injetado

    _orig_atendente = _iat.mostrar_interface_atendente
    def _atendente_injetado(root, usuario, auth_s):
        _orig_atendente(root, usuario, auth_s, pedido_service)
    _iat.mostrar_interface_atendente = _atendente_injetado

    _orig_admin = _iad.mostrar_interface_administrador
    def _admin_injetado(root, usuario, auth_s):
        _orig_admin(root, usuario, auth_s, pedido_service)
    _iad.mostrar_interface_administrador = _admin_injetado

    # --- Configuração da Janela Principal (Tkinter) --------------------------
    root = tk.Tk()
    root.title("BK Express")
    root.resizable(True, True)

    # Exibe a tela de login inicial do BK Express injetando o serviço de autenticação
    mostrar_login(root, autenticacao_service)

    # --- Ciclo de Execução da Aplicação --------------------------------------
    try:
        root.mainloop()
    finally:
        # Garante o fechamento seguro da conexão com o banco ao encerrar o app
        ConexaoSingleton.fechar_conexao()


if __name__ == "__main__":
    principal()