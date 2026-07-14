# negocio/cliente_service.py
from dados.cliente_repository import ClienteRepositorio
from dados.funcionarios_repository import FuncionarioRepositorio
from dominio.cliente import Clientes
from dominio.funcionarios import Funcionarios

class ClienteService:
    def __init__(self):
        self.cliente_repo = ClienteRepositorio()
        self.func_repo = FuncionarioRepositorio()

    def login(self, identificador, senha, tipo_login):
        """Autentica o usuário baseado no tipo (Cliente, Atendente ou Admin)"""
        if not identificador or not senha:
            raise ValueError("Usuário/E-mail e senha são obrigatórios.")

        id_limpo = identificador.strip()

        if tipo_login == "cliente":
            usuario = self.cliente_repo.buscar_por_email_senha(id_limpo, senha)
            if not usuario:
                raise ValueError("E-mail ou senha do cliente incorretos.")
            # Retorna o objeto de Domínio Clientes
            return Clientes(
                id_cliente=usuario["id_cliente"],
                nome=usuario["nome"],
                email=usuario["email"],
                senha=usuario["senha"],
                codigo_cliente=usuario["codigo_cliente"]
            )
        else:
            # Atendente ou Administrador
            usuario = self.func_repo.buscar_por_usuario_senha(id_limpo, senha, tipo_login)
            if not usuario:
                raise ValueError(f"Usuário ou senha de {tipo_login} incorretos.")
            
            # Como a tabela pode ter id_atendente ou id_admin, tratamos dinamicamente
            id_chave = "id_atendente" if tipo_login == "atendente" else "id_admin"
            
            # Retorna o objeto de Domínio Funcionarios
            return Funcionarios(
                id_funcionarios=usuario[id_chave],
                nome=usuario["nome"],
                usuario=usuario["usuario"],
                senha=usuario["senha"]
            )

    def cadastrar_cliente(self, nome, email, senha):
        """HU01 - Valida os dados e gera o código CLI-XXXX sequencial único"""
        if not nome or not email or not senha:
            raise ValueError("Todos os campos de cadastro são obrigatórios.")
        
        if "@" not in email:
            raise ValueError("Por favor, insira um e-mail válido.")

        # Regra de Negócio: Buscar o último ID para gerar o próximo código único
        ultimo_id = self.cliente_repo.obtain_ultimo_id()
        proximo_id = ultimo_id + 1
        codigo_unico = f"CLI-{proximo_id:04d}" # Gera CLI-0001, CLI-0002...

        sucesso = self.cliente_repo.inserir_cliente(nome, email, senha, codigo_unico)
        if not sucesso:
            raise ValueError("Erro ao salvar cliente. E-mail já pode estar cadastrado.")
        
        return True

    def listar_clientes(self):
        """Retorna a lista de clientes convertida em objetos de Domínio para o Admin"""
        lista_dados = self.cliente_repo.listar_todos()
        return [
            Clientes(c["id_cliente"], c["nome"], c["email"], "", c["codigo_cliente"])
            for c in lista_dados
        ]

    def excluir_cliente(self, id_cliente):
        """HU03 - Permite o admin excluir um cliente"""
        if not id_cliente:
            raise ValueError("ID do cliente inválido para exclusão.")
        return self.cliente_repo.deletar_cliente(id_cliente)