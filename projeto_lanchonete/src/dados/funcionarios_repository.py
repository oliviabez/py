import pymysql


class FuncionarioRepositorio:
    def __init__(self, conexao):
        self.conexao = conexao

    def buscar_por_usuario_senha(self, usuario, senha, cargo):
        cursor = self.conexao.cursor()

       
        tabela = "atendentes" if cargo.lower() == "atendente" else "administradores"
        id_coluna = "id_atendente" if cargo.lower() == "atendente" else "id_administrador"

        try:
            query = f"SELECT {id_coluna}, nome, usuario FROM {tabela} WHERE usuario = %s AND senha = %s"
            cursor.execute(query, (usuario, senha))
            return cursor.fetchone()
        finally:
            cursor.close()

    def buscar_por_usuario(self, usuario, cargo="atendente"):
        """Usado para checar duplicidade antes de cadastrar."""
        cursor = self.conexao.cursor()
        tabela = "atendentes" if cargo.lower() == "atendente" else "administradores"
        try:
            cursor.execute(f"SELECT 1 FROM {tabela} WHERE usuario = %s", (usuario,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def inserir_atendente(self, nome, usuario, senha):
        """Cadastra na tabela 'atendentes'."""
        cursor = self.conexao.cursor()
        try:
            sql = "INSERT INTO atendentes (nome, usuario, senha) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, usuario, senha))
            self.conexao.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            print(f"Erro ao inserir atendente: {e}")
            self.conexao.rollback()
            return None
        finally:
            cursor.close()

    def inserir_administrador(self, nome, usuario, senha):
        """Cadastra na tabela 'administradores'."""
        cursor = self.conexao.cursor()
        try:
            sql = "INSERT INTO administradores (nome, usuario, senha) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, usuario, senha))
            self.conexao.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            print(f"Erro ao inserir administrador: {e}")
            self.conexao.rollback()
            return None
        finally:
            cursor.close()