class Clientes:
    def __init__(self, id_cliente: int | None, nome: str, email: str, senha: str, codigo_cliente: str):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.senha = senha
        self.codigo_cliente = codigo_cliente  # O identificador único ex: CLI-0001
