from sqlalchemy import text
from storage import obter_sessao

class LogAuditoria:
    @staticmethod
    def listar_por_tabela(tabela):
        sessao = obter_sessao()
        sql = text("""
            SELECT *
            FROM Log_Auditoria
            WHERE Tabela_afetada = :tabela
            ORDER BY Data_operacao DESC
        """)
        resultado = sessao.execute(sql, {"tabela": tabela}).mappings().fetchall()
        sessao.close()
        return resultado