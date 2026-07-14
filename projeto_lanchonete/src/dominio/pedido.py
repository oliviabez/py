# dominio/pedido.py
from datetime import datetime


class Pedidos:
    def __init__(self, id_pedido: int | None, numero_pedido: str, id_cliente: int,
                 forma_pagamento: str, status_pedido: str, valor_total: float,
                 data_pedido: datetime = None):
        self.id_pedido = id_pedido
        self.numero_pedido = numero_pedido
        self.id_cliente = id_cliente
        self.forma_pagamento = forma_pagamento
        self.status_pedido = status_pedido
        self.valor_total = valor_total
        self.data_pedido = data_pedido