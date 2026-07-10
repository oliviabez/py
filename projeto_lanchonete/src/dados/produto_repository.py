# dados/produto_repository.py
import pymysql


class ProdutoRepositorio:
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar_por_id(self, id_produto):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "SELECT id_produto, nome, categoria, tamanho, preco, estoque, ativo FROM produtos WHERE id_produto = %s",
                (id_produto,)
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def listar_todos(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "SELECT id_produto, nome, categoria, tamanho, preco, estoque, ativo FROM produtos WHERE ativo = TRUE"
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def inserir_produto(self, nome, categoria, tamanho, preco, estoque):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO produtos (nome, categoria, tamanho, preco, estoque) VALUES (%s, %s, %s, %s, %s)",
                (nome, categoria, tamanho, preco, estoque)
            )
            self.conexao.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            print(f"Erro ao inserir produto: {e}")
            self.conexao.rollback()
            return None
        finally:
            cursor.close()

    def atualizar_produto(self, id_produto, nome, categoria, tamanho, preco, estoque):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "UPDATE produtos SET nome=%s, categoria=%s, tamanho=%s, preco=%s, estoque=%s WHERE id_produto=%s",
                (nome, categoria, tamanho, preco, estoque, id_produto)
            )
            self.conexao.commit()
            return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"Erro ao atualizar produto: {e}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()

    def deletar_produto(self, id_produto):
        """Fisicamente remove — se preferir soft-delete, trocar por UPDATE ativo=FALSE."""
        cursor = self.conexao.cursor()
        try:
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
            self.conexao.commit()
            return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"Erro ao deletar produto: {e}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()