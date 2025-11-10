from sqlalchemy import text
from storage import obter_sessao

class Usuario:
    def __init__(self, nome, id=None, email=None, numero=None, data_inscricao=None, multa=0.0):
        self.id = id
        self.nome = nome
        self.email = email
        self.numero = numero
        self.data_inscricao = data_inscricao
        self.multa = multa

    @classmethod
    def get(cls, id_usuario):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Usuarios WHERE ID_usuario = :id")
        resultado = conexao.execute(sql, {"id": id_usuario}).mappings().fetchone()
        conexao.close()
        if resultado:
            return Usuario(
                id=resultado['ID_usuario'],
                nome=resultado['Nome_usuario'],
                email=resultado['Email'],
                numero=resultado['Numero_telefone'],
                data_inscricao=resultado['Data_inscricao'],
                multa=resultado['Multa_atual']
            )
        return None

    @classmethod
    def all(cls):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Usuarios ORDER BY Nome_usuario")
        resultados = conexao.execute(sql).mappings().fetchall()
        conexao.close()
        usuarios = []
        for i in resultados:
            usuarios.append(Usuario(
                id=i['ID_usuario'],
                nome=i['Nome_usuario'],
                email=i['Email'],
                numero=i['Numero_telefone'],
                data_inscricao=i['Data_inscricao'],
                multa=i['Multa_atual']
            ))
        return usuarios

    def save(self):
        conexao = obter_sessao()
        sql = text("""
            INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
            VALUES (:nome, :email, :numero, :data_inscricao, :multa)
        """)
        cursor = conexao.execute(sql, {
            "nome": self.nome,
            "email": self.email,
            "numero": self.numero,
            "data_inscricao": self.data_inscricao,
            "multa": self.multa
        })
        self.id = cursor.lastrowid if hasattr(cursor, "lastrowid") else None
        conexao.commit()
        conexao.close()
        return True

    def update(self, nome, email, numero, multa):
        conexao = obter_sessao()
        sql = text("""
            UPDATE Usuarios
            SET Nome_usuario=:nome, Email=:email, Numero_telefone=:numero, Multa_atual=:multa
            WHERE ID_usuario=:id
        """)
        conexao.execute(sql, {
            "nome": nome,
            "email": email,
            "numero": numero,
            "multa": multa,
            "id": self.id
        })
        conexao.commit()
        conexao.close()
        self.nome = nome
        self.email = email
        self.numero = numero
        self.multa = multa

    @classmethod
    def delete(cls, id_usuario):
        conexao = obter_sessao()
        sql = text("DELETE FROM Usuarios WHERE ID_usuario = :id")
        conexao.execute(sql, {"id": id_usuario})
        conexao.commit()
        conexao.close()
