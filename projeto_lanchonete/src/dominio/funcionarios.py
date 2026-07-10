
class Funcionarios:
    def __init__(self, id_funcionarios: int | None, nome: str, usuario: str, senha: str):
        self.id_funcionarios = id_funcionarios
        self.nome = nome
        self.usuario = usuario
        self.senha = senha