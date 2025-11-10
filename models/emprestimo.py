from sqlalchemy import text
from datetime import date
from storage import obter_sessao


class Emprestimo:
    def __init__(self, usuario_id, livro_id, data_emprestimo, data_prevista, id=None, data_real=None, status='pendente'):
        self.id = id
        self.usuario_id = usuario_id
        self.livro_id = livro_id
        self.data_emprestimo = data_emprestimo
        self.data_prevista = data_prevista
        self.data_real = data_real
        self.status = status

    @classmethod
    def get(cls, id_emprestimo):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Emprestimos WHERE ID_emprestimo = :id_emprestimo")
        resultado = conexao.execute(sql, {"id_emprestimo": id_emprestimo}).mappings().fetchone()
        if resultado:
            emprestimo = Emprestimo(
                id=resultado['ID_emprestimo'],
                usuario_id=resultado['Usuario_id'],
                livro_id=resultado['Livro_id'],
                data_emprestimo=resultado['Data_emprestimo'],
                data_prevista=resultado['Data_devolucao_prevista'],
                data_real=resultado['Data_devolucao_real'],
                status=resultado['Status_emprestimo']
            )
            emprestimo.verificar_e_atualizar_status()
            conexao.close()
            return emprestimo
        conexao.close()
        return None

    @classmethod
    def all(cls):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Emprestimos")
        resultados = conexao.execute(sql).mappings().fetchall()
        emprestimos = []
        for r in resultados:
            e = Emprestimo(
                id=r['ID_emprestimo'],
                usuario_id=r['Usuario_id'],
                livro_id=r['Livro_id'],
                data_emprestimo=r['Data_emprestimo'],
                data_prevista=r['Data_devolucao_prevista'],
                data_real=r['Data_devolucao_real'],
                status=r['Status_emprestimo']
            )
            e.verificar_e_atualizar_status()
            emprestimos.append(e)
        conexao.close()
        return emprestimos

    def save(self):
        conexao = obter_sessao()
        sql = text("""
            INSERT INTO Emprestimos 
            (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, Data_devolucao_real, Status_emprestimo)
            VALUES (:usuario_id, :livro_id, :data_emprestimo, :data_prevista, :data_real, :status)
        """)
        cursor = conexao.execute(sql, {
            "usuario_id": self.usuario_id,
            "livro_id": self.livro_id,
            "data_emprestimo": self.data_emprestimo,
            "data_prevista": self.data_prevista,
            "data_real": self.data_real,
            "status": self.status
        })
        self.id = cursor.lastrowid if hasattr(cursor, "lastrowid") else None
        conexao.commit()
        conexao.close()
        return True

    def update(self, data_real=None, status=None):
        conexao = obter_sessao()
        if data_real is not None and status is not None:
            sql = text("""
                UPDATE Emprestimos
                SET Data_devolucao_real = :data_real, Status_emprestimo = :status
                WHERE ID_emprestimo = :id
            """)
            conexao.execute(sql, {"data_real": data_real, "status": status, "id": self.id})
            self.data_real = data_real
            self.status = status
        elif data_real is not None:
            sql = text("""
                UPDATE Emprestimos
                SET Data_devolucao_real = :data_real
                WHERE ID_emprestimo = :id
            """)
            conexao.execute(sql, {"data_real": data_real, "id": self.id})
            self.data_real = data_real
        elif status is not None:
            sql = text("""
                UPDATE Emprestimos
                SET Status_emprestimo = :status
                WHERE ID_emprestimo = :id
            """)
            conexao.execute(sql, {"status": status, "id": self.id})
            self.status = status

        conexao.commit()
        conexao.close()

    @classmethod
    def delete(cls, id_emprestimo):
        conexao = obter_sessao()
        sql = text("DELETE FROM Emprestimos WHERE ID_emprestimo = :id_emprestimo")
        conexao.execute(sql, {"id_emprestimo": id_emprestimo})
        conexao.commit()
        conexao.close()

    def verificar_e_atualizar_status(self):
        hoje = date.today()
        if (
            self.status == "pendente"
            and self.data_prevista
            and self.data_real is None
            and self.data_prevista < hoje
        ):
            self.status = "atrasado"
            conexao = obter_sessao()
            sql = text("UPDATE Emprestimos SET Status_emprestimo = :status WHERE ID_emprestimo = :id")
            conexao.execute(sql, {"status": self.status, "id": self.id})
            conexao.commit()
            conexao.close()