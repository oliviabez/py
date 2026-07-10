# src/negocio/autenticacao_service.py
from src.dados.cliente_repository import ClienteRepositorio
from src.dados.funcionarios_repository import FuncionarioRepositorio
from src.dominio.funcionarios import Funcionarios


class UsuarioLogado:
    """
    Objeto único devolvido por qualquer tipo de login (cliente, atendente,
    administrador), para que as telas (montar_header, tela_cliente etc.)
    sempre encontrem os mesmos atributos: .tipo, .nome, .id, .codigo_cliente
    """
    def __init__(self, tipo, id, nome, codigo_cliente=None, email=None, usuario=None):
        self.tipo = tipo                    # 'cliente' | 'atendente' | 'administrador'
        self.id = id
        self.nome = nome
        self.codigo_cliente = codigo_cliente
        self.email = email
        self.usuario = usuario


class AutenticacaoService:
    """
    Centraliza cadastro e login de cliente, atendente e administrador,
    e define o papel (perfil de acesso) do usuário autenticado.
    """

    def __init__(self, conexao):
        self.cliente_repository = ClienteRepositorio(conexao)
        self.atendente_repository = FuncionarioRepositorio(conexao)
        self.administrador_repository = FuncionarioRepositorio(conexao)

    def login(self, identificador, senha, tipo_login):
        tipo_login = tipo_login.lower()
        if tipo_login == 'cliente':
            return self.login_cliente(identificador, senha)
        elif tipo_login == 'atendente':
            return self.login_atendente(identificador, senha)
        elif tipo_login == 'administrador':
            return self.login_administrador(identificador, senha)
        else:
            raise ValueError(f"Tipo de login desconhecido: {tipo_login}")

    def login_cliente(self, email, senha):
        cliente = self.cliente_repository.buscar_por_email_senha(email, senha)
        if cliente is None:
            raise ValueError("E-mail ou senha inválidos.")

        return UsuarioLogado(
            tipo='cliente',
            id=cliente['id_cliente'],
            nome=cliente['nome'],
            codigo_cliente=cliente['codigo_cliente'],
            email=cliente['email'],
        )

    def cadastrar_usuario(self, nome, usuario, senha, tipo_usuario):
        import random
        codigo_gerado = f"CLI-{random.randint(1000, 9999)}"
        sucesso = self.cliente_repository.inserir_cliente(nome, usuario, senha, codigo_gerado)
        if not sucesso:
            raise ValueError("Não foi possível cadastrar. O e-mail já pode estar em uso.")
        return sucesso

    def cadastrar_atendente(self, nome, usuario, senha):
        """HU12 - cadastro de atendente."""
        if not nome or not usuario or not senha:
            raise ValueError("Todos os campos são obrigatórios.")

        atendente = Funcionarios(id_atendente=None, nome=nome, usuario=usuario, senha=senha)
        novo_id = self.atendente_repository.inserir_atendente(nome, usuario, senha)
        return novo_id

    def login_atendente(self, usuario, senha):
        """HU12 - login de atendente."""
        atendente = self.atendente_repository.buscar_por_usuario_senha(usuario, senha, cargo="atendente")
        if atendente is None:
            raise ValueError("Usuário ou senha inválidos.")

        return UsuarioLogado(
            tipo='atendente',
            id=atendente['id_atendente'],
            nome=atendente['nome'],
            usuario=atendente['usuario'],
        )

    def cadastrar_administrador(self, nome, usuario, senha):
        """HU13 - cadastro de administrador."""
        if not nome or not usuario or not senha:
            raise ValueError("Todos os campos são obrigatórios.")

        novo_id = self.administrador_repository.inserir_administrador(nome, usuario, senha)
        return novo_id

    def login_administrador(self, usuario, senha):
        """HU13 - login de administrador."""
        administrador = self.administrador_repository.buscar_por_usuario_senha(usuario, senha, cargo="administrador")
        if administrador is None:
            raise ValueError("Usuário ou senha inválidos.")

        return UsuarioLogado(
            tipo='administrador',
            id=administrador['id_administrador'],
            nome=administrador['nome'],
            usuario=administrador['usuario'],
        )