from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.editoras import Editora
from models.emprestimo import Emprestimo
from models.generos import Genero
from models.livros import Livro
from models.autores import Autor
from models.log_auditoria import LogAuditoria



livro_bp = Blueprint('livro', __name__, url_prefix='/livros')

@livro_bp.route("/")
def listar_livros():
    livros = Livro.all()

    return render_template("livros/livros.html", livros=livros, Autor=Autor, Editora=Editora)

@livro_bp.route("/adicionar", methods=["GET", "POST"])
def adicionar_livro():
    autores = Autor.all()
    generos = Genero.all()
    editoras = Editora.all()


    if request.method == "POST":
        titulo = request.form.get("titulo")
        autor_id = request.form.get("autor_id") or None
        isbn = request.form.get("isbn")
        ano_publicacao = request.form.get("ano_publicacao") or None
        genero_id = request.form.get("genero_id") or None
        editora_id = request.form.get("editora_id") or None
        quantidade = request.form.get("quantidade_disponivel")
        resumo = request.form.get("resumo")

        livro = Livro(
            titulo=titulo,
            autor_id=autor_id,
            isbn=isbn,
            ano_publicacao=ano_publicacao,
            genero_id=genero_id,
            editora_id=editora_id,
            quantidade=quantidade,
            resumo=resumo
        )

        try:
            livro.save()
            flash("Livro adicionado com sucesso!", "success")
        except Exception as e:
            msg = str(e.orig) if hasattr(e, "orig") else str(e)
            flash(msg, "error")
        return redirect(url_for("livro.listar_livros"))

    return render_template("livros/adicionar_livro.html", autores=autores, generos=generos, editoras=editoras)

@livro_bp.route("/remover/<int:id>", methods=["POST"])
def remover_livro(id):
    num_emprestimos = Emprestimo.verificar_emprestimos_livro(id)
    livro = Livro.get(id)

    if num_emprestimos > 0:
        flash(f"Não é possível remover o livro pois ele tem {num_emprestimos} empréstimos. Se quiser remover-lo, remova os empréstimos primeiro.", "error")
    else:
        Livro.delete(id)
        flash(f"Livro '{livro.titulo}' removido com sucesso!", "success")
        
    return redirect(url_for("livro.listar_livros"))

@livro_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_livro(id):
    livro = Livro.get(id)

    autores = Autor.all()
    generos = Genero.all()
    editoras = Editora.all()

    if not livro:
        flash("Livro não encontrado!", "error")
        return redirect(url_for("livro.listar_livros"))

    if request.method == "POST":
        livro.update(
            titulo=request.form.get("titulo"),
            autor_id=request.form.get("autor_id"),
            isbn=request.form.get("isbn"),
            ano_publicacao=request.form.get("ano_publicacao"),
            genero_id=request.form.get("genero_id"),
            editora_id=request.form.get("editora_id"),
            quantidade=request.form.get("quantidade_disponivel"),
            resumo=request.form.get("resumo"),
        )
        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for("livro.listar_livros"))

    return render_template("livros/editar_livro.html", livro=livro, autores=autores, editoras=editoras, generos=generos)

@livro_bp.route("/logs")
def logs_livros():
    logs = LogAuditoria.listar_por_tabela("Livros")

    return render_template(
        "logs/logs.html",
        logs=logs,
        tabela="Livros"
    )
