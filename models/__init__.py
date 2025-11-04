from flask_login import UserMixin
from storage import obter_conexao
from werkzeug.security import generate_password_hash

class User(UserMixin):
    def __init__(self, id, email, senha_hash, data, numero = None, nome=None, cpf=None, multa = None):
        self.id = id
        self.email = email
        self.senha_hash = senha_hash
        self.numero = numero
        self.nome = nome
        self.cpf = cpf
        self.data = data
        self.multa = multa

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_usuarios WHERE usr_id = ?"
        resultado = cursor.execute(sql, (user_id,)).fetchone()
        conexao.close()
        if resultado:
            return User(id=resultado['usr_id'],email=resultado['usr_email'], senha_hash=resultado['usr_senha'])
        return None

    @classmethod
    def all(cls):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_usuarios"
        resultados = cursor.execute(sql, ).fetchall()
        conexao.close()
        usuarios = []
        for i in resultados:
            usuario = User(id=i['usr_id'],email=i['usr_email'], senha_hash=i['usr_senha'])
            usuarios.append(usuario)
        return usuarios

    def save(self):
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Verifica se usuário já existe
        sql = "SELECT * FROM tb_usuarios WHERE usr_email = ?"
        resultado = cursor.execute(sql, (self.email,)).fetchone()
        if resultado:
            conexao.close()
            return None
        else:
            # Insere novo usuário
            sql_insert = "INSERT INTO tb_usuarios (usr_email, usr_senha) VALUES (?, ?, ?)"
            cursor = cursor.execute(sql_insert, (self.email, self.senha_hash, int(self.is_admin)))
            self.id = cursor.lastrowid
            conexao.commit()
            conexao.close()
            return True

    @classmethod
    def delete(cls, email):
        conexao = obter_conexao()
        cursor = conexao.cursor()

        sql = "DELETE FROM tb_usuarios WHERE usr_email = ?"
        cursor.execute(sql, (email,))
        conexao.commit()
        conexao.close()

    def update(self, email, senha, nome, cpf): #nao chequei tudo dessa função
        conexao = obter_conexao()
        cursor = conexao.cursor()
        senha_hash = generate_password_hash(senha) #hash para a senha nova
        sql = "UPDATE tb_usuarios SET usr_email = ?, usr_senha = ?, usr_nome = ?, usr_cpf = ? WHERE usr_id = ?"
        cursor.execute(sql, (email, senha_hash, nome, cpf, self.id))
        conexao.commit()
        conexao.close()
        #atualiza os atributos do objeto pra ficar de igual com os dados novos
        self.email = email
        self.senha_hash = senha_hash
        self.nome = nome
        self.cpf = cpf

class Livros():
    def __init__(self, id_livro, titulo, ISBN, Ano_publicacao, autor_id, editora_id, genero_id, quantidade_disponivel, resumo):
        self.id = id_livro
        self.titulo = titulo
        self.isbn = isbn
        self.ano = Ano_publicacao
        self.autor_id = autor_id
        self.editora_id = editora_id
        self.categoria = categoria
        self.genero_id = Genero_id
        self.quantidade = quantidade_disponivel
        self.resumo = resumo

    @classmethod
    def get(cls, id_livro):
        conexao = obter_conexao()
        sql = "SELECT * FROM Livros WHERE id_livro = ?"
        resultado = conexao.execute(sql, (id_livro,)).fetchone()
        conexao.close()
        if resultado:
            return Livro(id=['ID_livro'], titulo=["Titulo"], genero_id=["Genero_id"], editora_id=["Editoa_id"], quantidade = ["Quantidade_disponivel"])
        return None

    @classmethod
    def all(cls):
        conexao = obter_conexao()
        sql = "SELECT * FROM Livros"
        resultados = conexao.execute(sql, ).fetchall()
        conexao.close()
        livros = []
        for i in resultados:
            livro = Livro(id=['ID_livro'], titulo=["Titulo"], genero_id=["Genero_id"], editora_id=["Editoa_id"], quantidade = ["Quantidade_disponivel"])
            produtos.append(livro)
        return produtos

    def save(self):
        conexao = obter_conexao()

        # Insere novo produto
        sql_insert = "INSERT INTO tb_produtos (pro_nome, pro_preco, pro_url_imagem) VALUES (?, ?, ?)"
        conexao.execute(sql_insert, (self.nome, self.preco, self.imagem))
        sql_insert = "INSERT INTO tb_produtos (pro_nome, pro_preco, pro_url_imagem, pro_categoria) VALUES (?, ?, ?, ?)"
        conexao.execute(sql_insert, (self.nome, self.preco, self.imagem, self.categoria))
        conexao.commit()
        conexao.close()
        return True
        