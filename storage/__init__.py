import MySQLdb

def obter_conexao():
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="senha123",
        db="meubanco",
        charset="utf8mb4"
    )
    return conn