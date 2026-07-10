# negocio/produto_service.py
from dados.produto_repository import ProdutoRepositorio
from dominio.produto import Produtos

class ProdutoService:
    def __init__(self):
        self.produto_repo = ProdutoRepositorio()

    def listar_cardapio(self):
        """HU05 - Retorna todos os produtos ativos do BK convertidos em Objetos de Domínio"""
        produtos_banco = self.produto_repo.listar_todos()
        return [
            Produtos(
                id_produto=p["id_produto"],
                nome=p["nome"],
                categoria=p["categoria"],
                tamanho=p["tamanho"],
                preco=float(p["preco"]),
                estoque=p["estoque"]
            ) for p in produtos_banco
        ]

    def adicionar_produto(self, nome, categoria, tamanho, preco, estoque):
        """HU04 - Regra de negócio: Preço e Estoque não podem ser negativos"""
        if not nome or not categoria or not tamanho:
            raise ValueError("Preencha todos os campos do produto.")
        
        if preco <= 0:
            raise ValueError("O preço do produto deve ser maior que R$ 0,00.")
        
        if estoque < 0:
            raise ValueError("O estoque inicial não pode ser negativo.")

        return self.produto_repo.inserir_produto(nome, categoria, tamanho, preco, estoque)

    def alterar_produto(self, id_produto, nome, categoria, tamanho, preco, estoque):
        """HU06 - Altera dados validando as regras de valores"""
        if preco <= 0 or estoque < 0:
            raise ValueError("Valores de preço ou estoque inválidos.")
        return self.produto_repo.atualizar_produto(id_produto, nome, categoria, tamanho, preco, estoque)

    def remover_produto(self, id_produto):
        """HU07 - Remove o item do cardápio"""
        return self.produto_repo.deletar_produto(id_produto)