class ItensPedido:
    def __init__(self, id_item: int | None, id_pedido: int, id_produto: int, quantidade: int, preco_unitario: float):
        self.id_item = id_item
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
