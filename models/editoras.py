from sqlalchemy import text
from storage import obter_sessao

class Editora:
    def __init__(self, nome, endereco, id=None):
        self.id = id
        self.nome = nome
        self.endereco = endereco

    @classmethod
    def get(cls, id_editora):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Editoras WHERE ID_editora = :id_editora")
        resultado = conexao.execute(sql, {"id_editora": id_editora}).mappings().fetchone()
        conexao.close()
        if resultado:
            return Editora(
                id=resultado['ID_editora'],
                nome=resultado['Nome_editora'],
                endereco=resultado['Endereco_editora']
            )
        return None

    @classmethod
    def all(cls):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Editoras")
        resultados = conexao.execute(sql).mappings().fetchall()
        conexao.close()
        editoras = []
        for e in resultados:
            editoras.append(Editora(
                id=e['ID_editora'],
                nome=e['Nome_editora'],
                endereco=e['Endereco_editora']
            ))
        return editoras

    def save(self):
        conexao = obter_sessao()
        sql = text("INSERT INTO Editoras (Nome_editora, Endereco_editora) VALUES (:nome, :endereco)")
        cursor = conexao.execute(sql, {"nome": self.nome, "endereco": self.endereco})
        self.id = cursor.lastrowid if hasattr(cursor, "lastrowid") else None
        conexao.commit()
        conexao.close()
        return True

    def update(self, nome, endereco):
        conexao = obter_sessao()
        sql = text("UPDATE Editoras SET Nome_editora = :nome, Endereco_editora = :endereco WHERE ID_editora = :id")
        conexao.execute(sql, {"nome": nome, "endereco": endereco, "id": self.id})
        conexao.commit()
        conexao.close()
        self.nome = nome
        self.endereco = endereco

    @classmethod
    def delete(cls, id_editora):
        conexao = obter_sessao()
        sql = text("DELETE FROM Editoras WHERE ID_editora = :id_editora")
        conexao.execute(sql, {"id_editora": id_editora})
        conexao.commit()
        conexao.close()