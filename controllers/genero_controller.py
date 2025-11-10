from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.generos import Genero
from models.livros import Livro  

genero_bp = Blueprint("genero", __name__, url_prefix="/generos")

@genero_bp.route("/")
def listar_generos():
    generos = Genero.all()
    return render_template("generos/generos.html", generos=generos)

@genero_bp.route("/adicionar", methods=["GET", "POST"])
def adicionar_genero():
    if request.method == "POST":
        nome = request.form.get("nome_genero")

        if not nome:
            flash("O nome do gênero é obrigatório!", "error")
            return redirect(url_for("genero.adicionar_genero"))

        genero = Genero(nome=nome)
        genero.save()
        flash("Gênero adicionado com sucesso!", "success")
        return redirect(url_for("genero.listar_generos"))

    return render_template("generos/adicionar_genero.html")

@genero_bp.route("/remover/<int:id>", methods=["POST"])
def remover_genero(id):
    num_generos = Livro.verificar_livros_genero(id) #Vê qnts livros o genero tem, e se pode apagar ele
    
    if num_generos > 0: #Não deixa apagar o autor que tem generos
        flash(f"Não é possível remover este gêner, pois ele possui {num_generos} livros. Se quiser remover-lo, remova os livros primeiro.", "error")
    else:
        Genero.delete(id)
        flash("Autor removido com sucesso!", "success")

    return redirect(url_for("genero.listar_generos"))

@genero_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_genero(id):
    genero = Genero.get(id)
    if not genero:
        flash("Gênero não encontrado!", "error")
        return redirect(url_for("genero.listar_generos"))

    if request.method == "POST":
        novo_nome = request.form.get("nome_genero")
        if not novo_nome:
            flash("O nome do gênero não pode ser vazio!", "error")
            return redirect(url_for("genero.editar_genero", id=id))

        genero.update(novo_nome)
        flash("Gênero atualizado com sucesso!", "success")
        return redirect(url_for("genero.listar_generos"))
    return render_template("generos/editar_genero.html", genero=genero)