import pymysql
import pymysql.cursors


class ConexaoSingleton:

    _conexao = None

    @classmethod
    def obter_conexao(cls):

        if cls._conexao is None or not cls._conexao.open:
            cls._conexao = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='olilinda',
                database='lanchonete_db',
                cursorclass=pymysql.cursors.DictCursor,  # já devolve dicts direto
                autocommit=True,
            )

        return cls._conexao

    @classmethod
    def fechar_conexao(cls):
        if cls._conexao is not None:
            cls._conexao.close()
            cls._conexao = None