from sqlalchemy import text
from storage import obter_sessao

class Livro:
    def __init__(self, titulo, isbn, ano_publicacao, autor_id, genero_id, editora_id, quantidade,id=None, resumo=None):
        self.id = id
        self.titulo = titulo
        self.isbn = isbn
        self.ano_publicacao = ano_publicacao
        self.autor_id = autor_id
        self.genero_id = genero_id
        self.editora_id = editora_id
        self.quantidade = quantidade
        self.resumo = resumo

    @classmethod
    def get(cls, id_livro):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Livros WHERE ID_livro = :id")
        resultado = conexao.execute(sql, {"id": id_livro}).mappings().fetchone()
        conexao.close()
        if resultado:
            return Livro(
                id=resultado['ID_livro'],
                titulo=resultado['Titulo'],
                isbn=resultado['ISBN'],
                ano_publicacao=resultado['Ano_publicacao'],
                autor_id=resultado['Autor_id'],
                genero_id=resultado['Genero_id'],
                editora_id=resultado['Editora_id'],
                quantidade=resultado['Quantidade_disponivel'],
                resumo=resultado['Resumo']
            )
        return None

    @classmethod
    def all(cls):
        conexao = obter_sessao()
        sql = text("SELECT * FROM Livros")
        resultados = conexao.execute(sql).mappings().fetchall()
        conexao.close()
        livros = []
        for i in resultados:
            livros.append(Livro(
                id=i['ID_livro'],
                titulo=i['Titulo'],
                isbn=i['ISBN'],
                ano_publicacao=i['Ano_publicacao'],
                autor_id=i['Autor_id'],
                genero_id=i['Genero_id'],
                editora_id=i['Editora_id'],
                quantidade=i['Quantidade_disponivel'],
                resumo=i['Resumo']
            ))
        return livros

    def save(self):
        conexao = obter_sessao()
        sql = text("""
            INSERT INTO Livros (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo)
            VALUES (:titulo, :autor_id, :isbn, :ano, :genero_id, :editora_id, :quantidade, :resumo)
        """)
        cursor = conexao.execute(sql, {
            "titulo": self.titulo,
            "autor_id": self.autor_id,
            "isbn": self.isbn,
            "ano": self.ano_publicacao,
            "genero_id": self.genero_id,
            "editora_id": self.editora_id,
            "quantidade": self.quantidade,
            "resumo": self.resumo
        })
        self.id = cursor.lastrowid if hasattr(cursor, "lastrowid") else None
        conexao.commit()
        conexao.close()
        return True

    def update(self, titulo, isbn, ano_publicacao, autor_id, genero_id, editora_id, quantidade, resumo):
        conexao = obter_sessao()
        sql = text("""
            UPDATE Livros
            SET Titulo=:titulo, ISBN=:isbn, Ano_publicacao=:ano, Autor_id=:autor_id,
                Genero_id=:genero_id, Editora_id=:editora_id, Quantidade_disponivel=:quantidade, Resumo=:resumo
            WHERE ID_livro=:id
        """)
        
        conexao.execute(sql, {
            "titulo": titulo,
            "isbn": isbn,
            "ano": ano_publicacao,
            "autor_id": autor_id,
            "genero_id": genero_id,
            "editora_id": editora_id,
            "quantidade": quantidade,
            "resumo": resumo,
            "id": self.id
        })
        conexao.commit()
        conexao.close()
        self.titulo = titulo
        self.isbn = isbn
        self.ano_publicacao = ano_publicacao
        self.autor_id = autor_id
        self.genero_id = genero_id
        self.editora_id = editora_id
        self.quantidade = quantidade
        self.resumo = resumo

    @classmethod
    def delete(cls, id_livro):
        conexao = obter_sessao()
        sql = text("DELETE FROM Livros WHERE ID_livro = :id")
        conexao.execute(sql, {"id": id_livro})
        conexao.commit()
        conexao.close()

    #FUNÇÕES QUE TRATA O ERRO DE DELETAR UM ELEMENTO QUE TEM FOREIGN KEY EM UM LIVRO
    @classmethod
    def verificar_livros_autor(cls, autor_id):        
        conexao = obter_sessao()
        sql = text("SELECT COUNT(*) FROM Livros WHERE Autor_id = :id")
        
        resultado = conexao.execute(sql, {"id": autor_id}).fetchone()
        conexao.close()
        
        return resultado[0] if resultado else 0

    @classmethod
    def verificar_livros_genero(cls, genero_id):
        conexao = obter_sessao()
        sql = text("SELECT COUNT(*) FROM Livros WHERE Genero_id = :id")
        
        resultado = conexao.execute(sql, {"id": genero_id}).fetchone()
        conexao.close()
        
        return resultado[0] if resultado else 0

    @classmethod
    def verificar_livros_editora(cls, editora_id):
        conexao = obter_sessao()
        sql = text("SELECT COUNT(*) FROM Livros WHERE Editora_id = :id")
        
        resultado = conexao.execute(sql, {"id": editora_id}).fetchone()
        conexao.close()
        
        return resultado[0] if resultado else 0
    
    