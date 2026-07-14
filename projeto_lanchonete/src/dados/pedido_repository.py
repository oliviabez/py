# dados/pedido_repository.py
from datetime import date
import pymysql


class PedidoRepositorio:
    def __init__(self, conexao):
        self.conexao = conexao

    def gerar_numero_pedido(self):
        """
        Gera número de 3 dígitos que reinicia todo dia (regra do schema).
        Conta quantos pedidos já existem hoje e soma 1.
        """
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) AS total FROM pedidos WHERE DATE(data_pedido) = CURDATE()"
            )
            total_hoje = cursor.fetchone()["total"]
            proximo = total_hoje + 1
            return f"{proximo:03d}"  # 001, 002, 003...
        finally:
            cursor.close()

    def contar_pedidos_cliente_hoje(self, id_cliente):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """SELECT COUNT(*) AS total FROM pedidos
                   WHERE id_cliente = %s AND DATE(data_pedido) = CURDATE()
                   AND status_pedido != 'Cancelado'""",
                (id_cliente,)
            )
            return cursor.fetchone()["total"]
        finally:
            cursor.close()

    def inserir(self, pedido):
        """Recebe um objeto de domínio Pedidos e salva na tabela."""
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """INSERT INTO pedidos (numero_pedido, id_cliente, forma_pagamento, status_pedido, valor_total)
                   VALUES (%s, %s, %s, %s, %s)""",
                (
                    pedido.numero_pedido,
                    pedido.id_cliente,
                    pedido.forma_pagamento,
                    pedido.status_pedido,
                    pedido.valor_total,
                )
            )
            self.conexao.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            print(f"Erro ao inserir pedido: {e}")
            self.conexao.rollback()
            return None
        finally:
            cursor.close()

    def buscar_por_id(self, id_pedido):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (id_pedido,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def buscar_por_numero_e_data(self, numero_pedido, data=None):
        """Busca pelo número do pedido (dentro do dia, já que o número se repete entre dias)."""
        data = data or date.today()
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """SELECT * FROM pedidos
                   WHERE numero_pedido = %s AND DATE(data_pedido) = %s""",
                (numero_pedido, data)
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def buscar_por_email_cliente(self, email):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """SELECT p.* FROM pedidos p
                   INNER JOIN clientes c ON p.id_cliente = c.id_cliente
                   WHERE c.email = %s
                   ORDER BY p.data_pedido DESC""",
                (email,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def listar(self):
        """Usado por atendentes/administradores — vê todos os pedidos."""
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """SELECT p.*, c.nome AS nome_cliente FROM pedidos p
                   INNER JOIN clientes c ON p.id_cliente = c.id_cliente
                   ORDER BY p.data_pedido ASC"""
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def listar_fila_cozinha(self):
        """Mostra apenas pedidos ainda não entregues/cancelados, para a tela do atendente."""
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """SELECT p.id_pedido, p.numero_pedido, c.nome AS nome_cliente,
                          p.valor_total, p.status_pedido
                   FROM pedidos p
                   INNER JOIN clientes c ON p.id_cliente = c.id_cliente
                   WHERE p.status_pedido NOT IN ('Pedido entregue', 'Cancelado')
                   ORDER BY p.data_pedido ASC"""
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def atualizar(self, pedido):
        """HU10 - atualiza forma de pagamento e valor total do pedido."""
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """UPDATE pedidos SET forma_pagamento = %s, valor_total = %s
                   WHERE id_pedido = %s""",
                (pedido.forma_pagamento, pedido.valor_total, pedido.id_pedido)
            )
            self.conexao.commit()
            return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"Erro ao atualizar pedido: {e}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_status(self, id_pedido, novo_status):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "UPDATE pedidos SET status_pedido = %s WHERE id_pedido = %s",
                (novo_status, id_pedido)
            )
            self.conexao.commit()
            return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"Erro ao atualizar status do pedido: {e}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()