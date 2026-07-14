import pymysql


class ClienteRepositorio:
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar_por_email_senha(self, email, senha):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "SELECT id_cliente, nome, email, codigo_cliente FROM clientes WHERE email = %s AND senha = %s",
                (email, senha)
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def buscar_por_id(self, id_cliente):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                "SELECT id_cliente, nome, email, codigo_cliente FROM clientes WHERE id_cliente = %s",
                (id_cliente,)
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def inserir_cliente(self, nome, email, senha, codigo_cliente):
        cursor = self.conexao.cursor()
        try:
            sql = """
                INSERT INTO clientes (nome, email, senha, codigo_cliente)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, email, senha, codigo_cliente))
            self.conexao.commit()
            return True
        except pymysql.Error as e:
            print(f"Erro ao inserir cliente no MySQL: {e}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()

    def obter_ultimo_id(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT MAX(id_cliente) AS max_id FROM clientes")
            resultado = cursor.fetchone()
            return resultado["max_id"] if resultado["max_id"] is not None else 0
        finally:
            cursor.close()

    def listar_todos(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT id_cliente, nome, email, codigo_cliente FROM clientes")
            return cursor.fetchall()
        finally:
            cursor.close()

    def deletar_cliente(self, id_cliente):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
            self.conexao.commit()
            return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"Erro ao deletar cliente: {e}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()