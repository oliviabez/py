# negocio/pedido_service.py
from datetime import datetime, timedelta

from dados.pedido_repository import PedidoRepositorio
from dados.item_pedido_repository import ItemPedidoRepository
from dados.produto_repository import ProdutoRepositorio
from dados.cliente_repository import ClienteRepositorio
from dominio.pedido import Pedidos
from dominio.item_pedido import ItensPedido


FORMAS_PAGAMENTO_VALIDAS = [
    'Dinheiro', 'Cartão de Débito', 'Cartão de Crédito', 'Pix'
]

STATUS_VALIDOS = [
    'Pedido recebido com sucesso',
    'Pedido sendo feito',
    'Pedido entregue',
    'Cancelado'
]

LIMITE_PEDIDOS_POR_DIA = 3
PRAZO_ALTERACAO_CLIENTE_MINUTOS = 20
PRAZO_CANCELAMENTO_ADMIN_MINUTOS = 60


class PedidoService:

    def __init__(self, conexao):
        self.repository = PedidoRepositorio(conexao)
        self.item_repository = ItemPedidoRepository(conexao)
        self.produto_repository = ProdutoRepositorio(conexao)
        self.cliente_repository = ClienteRepositorio(conexao)

    def criar_pedido(self, id_cliente, itens, forma_pagamento):
        """
        HU08 - registro de pedido.
        itens: lista de dicionários
            [{'id_produto': 1, 'quantidade': 2, 'tamanho': 'Médio'}, ...]
        """

        cliente = self.cliente_repository.buscar_por_id(id_cliente)

        if cliente is None:
            print("Cliente não cadastrado.")
            return None

        if not itens:
            print("O pedido deve conter pelo menos um produto.")
            return None

        if forma_pagamento not in FORMAS_PAGAMENTO_VALIDAS:
            print(
                "Forma de pagamento inválida. Opções aceitas: "
                + ", ".join(FORMAS_PAGAMENTO_VALIDAS)
                + " (não é permitido parcelamento)."
            )
            return None

        pedidos_hoje = self.repository.contar_pedidos_cliente_hoje(id_cliente)

        if pedidos_hoje >= LIMITE_PEDIDOS_POR_DIA:
            print("Limite de 3 pedidos por dia já foi atingido.")
            return None

        itens_validados = []
        valor_total = 0

        for item in itens:

            produto = self.produto_repository.buscar_por_id(item['id_produto'])

            if produto is None or not produto['ativo']:
                print(f"Produto indisponível: id {item['id_produto']}.")
                return None

            quantidade = item['quantidade']
            subtotal = float(produto['preco']) * quantidade
            valor_total += subtotal

            itens_validados.append({
                'id_produto': produto['id_produto'],
                'quantidade': quantidade,
                'tamanho': item.get('tamanho', produto['tamanho']),
                'preco_unitario': float(produto['preco']),
                'subtotal': subtotal
            })

        numero_pedido = self.repository.gerar_numero_pedido()

        pedido = Pedidos(
            id_pedido=None,
            numero_pedido=numero_pedido,
            id_cliente=id_cliente,
            forma_pagamento=forma_pagamento,
            status_pedido='Pedido recebido com sucesso',
            valor_total=valor_total
        )

        id_pedido = self.repository.inserir(pedido)

        for item in itens_validados:

            item_pedido = ItensPedido(
                id_item=None,
                id_pedido=id_pedido,
                id_produto=item['id_produto'],
                quantidade=item['quantidade'],
                tamanho=item['tamanho'],
                preco_unitario=item['preco_unitario'],
                subtotal=item['subtotal']
            )

            self.item_repository.inserir(item_pedido)

        print(
            f"Pedido realizado com sucesso! Número {numero_pedido}, "
            f"valor total R$ {valor_total:.2f}."
        )

        return id_pedido

    def consultar_pedidos(self, email=None, numero_pedido=None):
        """HU09 - consulta de pedidos por e-mail ou número do pedido."""

        if not email and not numero_pedido:
            print("Informe o e-mail do cliente ou o número do pedido.")
            return []

        if numero_pedido:

            pedido = self.repository.buscar_por_numero_e_data(numero_pedido)

            if pedido is None:
                print("Pedido não encontrado.")
                return []

            resultados = [pedido]

        else:
            resultados = self.repository.buscar_por_email_cliente(email)

            if not resultados:
                print("Nenhum pedido encontrado para esse e-mail.")
                return []

        for pedido in resultados:
            print(
                f"Pedido {pedido['numero_pedido']} - "
                f"Status: {pedido['status_pedido']} - "
                f"Valor: R$ {pedido['valor_total']} - "
                f"Data: {pedido['data_pedido']}"
            )

        return resultados

    def _minutos_desde_criacao(self, pedido):

        agora = datetime.now()
        data_pedido = pedido['data_pedido']

        if isinstance(data_pedido, str):
            data_pedido = datetime.fromisoformat(data_pedido)

        diferenca = agora - data_pedido

        return diferenca.total_seconds() / 60

    def atualizar_pedido(self, id_cliente_logado, id_pedido,
                        forma_pagamento=None, itens=None):
        """
        HU10 - atualização de pedido pelo próprio cliente, dentro do
        prazo de 20 minutes e no mesmo dia em que foi criado.
        """

        pedido = self.repository.buscar_por_id(id_pedido)

        if pedido is None:
            print("Pedido não encontrado.")
            return False

        if pedido['id_cliente'] != id_cliente_logado:
            print("Acesso negado: este pedido não pertence a você.")
            return False

        data_pedido = pedido['data_pedido']

        if isinstance(data_pedido, str):
            data_pedido = datetime.fromisoformat(data_pedido)

        if data_pedido.date() != datetime.now().date():
            print("O pedido só pode ser atualizado no mesmo dia em que foi realizado.")
            return False

        if self._minutos_desde_criacao(pedido) > PRAZO_ALTERACAO_CLIENTE_MINUTOS:
            print("O prazo de 20 minutos para atualizar o pedido expirou.")
            return False

        if forma_pagamento is None and not itens:
            print("Nenhuma alteração foi informada.")
            return False

        nova_forma = forma_pagamento or pedido['forma_pagamento']

        if forma_pagamento and forma_pagamento not in FORMAS_PAGAMENTO_VALIDAS:
            print("Forma de pagamento inválida.")
            return False

        novo_valor_total = float(pedido['valor_total'])

        if itens:

            self.item_repository.remover_por_pedido(id_pedido)

            novo_valor_total = 0

            for item in itens:

                produto = self.produto_repository.buscar_por_id(item['id_produto'])

                if produto is None or not produto['ativo']:
                    print(f"Produto indisponível: id {item['id_produto']}.")
                    return False

                subtotal = float(produto['preco']) * item['quantidade']
                novo_valor_total += subtotal

                item_pedido = ItensPedido(
                    id_item=None,
                    id_pedido=id_pedido,
                    id_produto=produto['id_produto'],
                    quantidade=item['quantidade'],
                    tamanho=item.get('tamanho', produto['tamanho']),
                    preco_unitario=float(produto['preco']),
                    subtotal=subtotal
                )

                self.item_repository.inserir(item_pedido)

        pedido_atualizado = Pedidos(
            id_pedido=id_pedido,
            numero_pedido=pedido['numero_pedido'],
            id_cliente=pedido['id_cliente'],
            forma_pagamento=nova_forma,
            status_pedido=pedido['status_pedido'],
            valor_total=novo_valor_total
        )

        self.repository.atualizar(pedido_atualizado)

        print("Pedido atualizado com sucesso.")

        return True

    def cancelar_pedido(self, papel_logado, id_cliente_logado, id_pedido):
        """
        HU11 - cancelamento de pedido.
        Cliente: até 20 minutos após a criação.
        Administrador: somente após 1 hora sem retirada pelo cliente
        (pedido ainda não entregue).
        """

        pedido = self.repository.buscar_por_id(id_pedido)

        if pedido is None:
            print("Pedido não encontrado.")
            return False

        if pedido['status_pedido'] == 'Cancelado':
            print("Este pedido já está cancelado.")
            return False

        minutos = self._minutos_desde_criacao(pedido)

        if papel_logado == 'cliente':

            if pedido['id_cliente'] != id_cliente_logado:
                print("Acesso negado: este pedido não pertence a você.")
                return False

            if minutos > PRAZO_ALTERACAO_CLIENTE_MINUTOS:
                print("O prazo de 20 minutos para cancelar o pedido expirou.")
                return False

        elif papel_logado == 'administrador':

            if pedido['status_pedido'] == 'Pedido entregue':
                print("Não é possível cancelar um pedido já entregue.")
                return False

            if minutos < PRAZO_CANCELAMENTO_ADMIN_MINUTOS:
                print(
                    "O administrador só pode cancelar o pedido após "
                    "1 hora sem retirada pelo cliente."
                )
                return False

        else:
            print("Acesso negado.")
            return False

        self.repository.atualizar_status(id_pedido, 'Cancelado')

        print("Pedido cancelado com sucesso.")

        return True

    def atualizar_status(self, papel_logado, id_pedido, novo_status):
        """HU14 - apenas atendentes e administradores alteram o status."""

        if papel_logado not in ('atendente', 'administrador'):
            print("Acesso negado: apenas atendentes ou administradores "
                  "podem alterar o status do pedido.")
            return False

        if novo_status not in STATUS_VALIDOS:
            print("Status inválido. Opções: " + ", ".join(STATUS_VALIDOS))
            return False

        pedido = self.repository.buscar_por_id(id_pedido)

        if pedido is None:
            print("Pedido não encontrado.")
            return False

        self.repository.atualizar_status(id_pedido, novo_status)

        print(f"Status do pedido atualizado para: {novo_status}")

        return True

    def listar_pedidos(self, papel_logado, id_cliente_logado=None):
        """
        Cliente vê apenas o status dos próprios pedidos.
        Atendente/administrador veem todos os pedidos.
        """

        if papel_logado == 'cliente':

            resultados = self.repository.buscar_por_email_cliente(
                self.cliente_repository.buscar_por_id(id_cliente_logado)['email']
            )

        else:
            resultados = self.repository.listar()

        if not resultados:
            print("Nenhum pedido encontrado.")
            return []

        for pedido in resultados:
            print(pedido)

        return resultados