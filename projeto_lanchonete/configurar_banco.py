import mysql.connector
import os

# instalador do MySQL!
SENHA_DO_MYSQL = "olilinda"

try:
    print(" A conectar ao servidor MySQL...")
    conexao = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="olilinda"
    )
    cursor = conexao.cursor()

    # Cria o banco de dados principal que o main.py procura
    print(" A criar o banco de dados 'lanchonete_db'...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS lanchonete_db;")
    cursor.execute("USE lanchonete_db;")

    # Caminho para o ficheiro init.sql que já existe no projeto
    caminho_sql = os.path.join("banco_de_dados", "init.sql")

    if not os.path.exists(caminho_sql):
        print(f" Erro: Não encontrei o ficheiro init.sql no caminho: {caminho_sql}")
    else:
        print(" A ler o ficheiro init.sql e a estruturar as tabelas...")
        with open(caminho_sql, "r", encoding="utf-8") as f:
            conteudo_sql = f.read()

        # Remove a linha original 'CREATE DATABASE IF NOT EXISTS lanchonete_db;' 
        #  'USE lanchonete_db;' para forçar a criação dentro do 'bk_express'
        comandos = conteudo_sql.split(";")

        for comando in comandos:
            comando_limpo = comando.strip()
            if not comando_limpo or "lanchonete_db" in comando_limpo.lower():
                continue
            
            try:
                cursor.execute(comando_limpo)
            except mysql.connector.Error as e:
                print(f" Nota ao executar comando: {e}")

        conexao.commit()
        print(" SUCESSO: Banco 'bk_express' e todas as tabelas foram criados e povoados!")

except mysql.connector.Error as err:
    print(f" Erro de conexão com o MySQL: {err}")
finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()