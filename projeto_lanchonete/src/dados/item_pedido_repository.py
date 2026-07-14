# dados/item_pedido_repository.py
import pymysql


class ItemPedidoRepository:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir(self, item_objeto):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, tamanho, preco_unitario, subtotal)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    item_objeto.id_pedido,
                    item_objeto.id_produto,
                    item_objeto.quantidade,
                    item_objeto.tamanho,
                    item_objeto.preco_unitario,
                    item_objeto.subtotal
                )
            )
            self.conexao.commit()
            return True
        except pymysql.Error as e:
            print(f"Erro ao inserir item do pedido: {e}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()

    def remover_por_pedido(self, id_pedido):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("DELETE FROM itens_pedido WHERE id_pedido = %s", (id_pedido,))
            self.conexao.commit()
            return True
        finally:
            cursor.close()

    def buscar_por_pedido(self, id_pedido):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "SELECT id_item, id_pedido, id_produto, quantidade, tamanho, preco_unitario, subtotal FROM itens_pedido WHERE id_pedido = %s",
                (id_pedido,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()