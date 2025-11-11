from sqlalchemy import text
from storage import obter_sessao

class Autor:
    def __init__(self, nome, id=None,  nacionalidade=None, data_nascimento=None, biografia=None):
        self.id = id
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.data_nascimento = data_nascimento
        self.biografia = biografia

    @classmethod
    def get(cls, id_autor):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Autores WHERE ID_autor = :id_autor")
        resultado = conexao.execute(sql, {"id_autor": id_autor}).mappings().fetchone()
        conexao.close()

        if resultado:
            return Autor(
                id=resultado["ID_autor"],
                nome=resultado["Nome_autor"],
                nacionalidade=resultado["Nacionalidade"],
                data_nascimento=resultado["Data_nascimento"],
                biografia=resultado["Biografia"],
            )
        return None

    @classmethod
    def all(cls):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Autores")
        resultados = conexao.execute(sql).mappings().fetchall()
        conexao.close()

        autores = []
        for i in resultados:
            autores.append(
                Autor(
                    id=i["ID_autor"],
                    nome=i["Nome_autor"],
                    nacionalidade=i["Nacionalidade"],
                    data_nascimento=i["Data_nascimento"],
                    biografia=i["Biografia"],
                )
            )
        return autores

    def save(self):
        conexao = obter_sessao()
        sql = text("""
            INSERT INTO Autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia)
            VALUES (:nome, :nacionalidade, :data_nascimento, :biografia)
        """)
        cursor = conexao.execute(sql, {
            "nome": self.nome,
            "nacionalidade": self.nacionalidade,
            "data_nascimento": self.data_nascimento,
            "biografia": self.biografia
        })
        conexao.commit()
        self.id = cursor.lastrowid
        conexao.close()
        return True

    def update(self, nome, nacionalidade, data_nascimento, biografia):
        conexao = obter_sessao()
        sql = text("""
            UPDATE Autores
            SET Nome_autor = :nome,
                Nacionalidade = :nacionalidade,
                Data_nascimento = :data_nascimento,
                Biografia = :biografia
            WHERE ID_autor = :id
        """)
        conexao.execute(sql, {
            "nome": nome,
            "nacionalidade": nacionalidade,
            "data_nascimento": data_nascimento,
            "biografia": biografia,
            "id": self.id
        })
        conexao.commit()
        conexao.close()

        self.nome = nome
        self.nacionalidade = nacionalidade
        self.data_nascimento = data_nascimento
        self.biografia = biografia

    @classmethod
    def delete(cls, id_autor):
        conexao = obter_sessao()
        sql = text("DELETE FROM Autores WHERE ID_autor = :id_autor")
        conexao.execute(sql, {"id_autor": id_autor})
        conexao.commit()
        conexao.close()
