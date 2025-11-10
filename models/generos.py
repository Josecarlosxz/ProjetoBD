from sqlalchemy import text
from storage import obter_sessao

class Genero:
    def __init__(self, nome, id=None):
        self.id = id
        self.nome = nome

    @classmethod
    def get(cls, id_genero):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Generos WHERE ID_genero = :id_genero")
        resultado = conexao.execute(sql, {"id_genero": id_genero}).mappings().fetchone()
        conexao.close()
        if resultado:
            return Genero(id=resultado['ID_genero'], nome=resultado['Nome_genero'])
        return None

    @classmethod
    def all(cls):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Generos")
        resultados = conexao.execute(sql).mappings().fetchall()
        conexao.close()
        generos = []
        for i in resultados:
            generos.append(Genero(id=i['ID_genero'], nome=i['Nome_genero']))
        return generos

    def save(self):
        conexao = obter_sessao()
        sql = text("INSERT INTO Generos (Nome_genero) VALUES (:nome)")
        cursor = conexao.execute(sql, {"nome": self.nome})
        self.id = cursor.lastrowid if hasattr(cursor, "lastrowid") else None
        conexao.commit()
        conexao.close()
        return True

    def update(self, nome):
        conexao = obter_sessao()
        sql = text("UPDATE Generos SET Nome_genero = :nome WHERE ID_genero = :id")
        conexao.execute(sql, {"nome": nome, "id": self.id})
        conexao.commit()
        conexao.close()
        self.nome = nome

    @classmethod
    def delete(cls, id_genero):
        conexao = obter_sessao()
        sql = text("DELETE FROM Generos WHERE ID_genero = :id_genero")
        conexao.execute(sql, {"id_genero": id_genero})
        conexao.commit()
        conexao.close()