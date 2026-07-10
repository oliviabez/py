# dominio/produtos.py

class Produtos:
    def __init__(self, id_produto: int | None, nome: str, categoria: str, tamanho: str, preco: float, estoque: int):
        self.id_produto = id_produto
        self.nome = nome
        self.categoria = categoria
        self.tamanho = tamanho
        self.preco = preco
        self.estoque = estoque