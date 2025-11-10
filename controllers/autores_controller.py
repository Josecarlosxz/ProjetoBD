from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.autores import Autor

autor_bp = Blueprint("autor", __name__, url_prefix="/autores")

@autor_bp.route("/")
def listar_autores():
    autores = Autor.all()
    return render_template("autores/autores.html", autores=autores)

@autor_bp.route("/adicionar", methods=["GET", "POST"])
def adicionar_autor():
    if request.method == "POST":
        nome = request.form.get("nome")
        nacionalidade = request.form.get("nacionalidade") or "Sem Dados"
        data_nascimento = request.form.get("data_nascimento") or "Sem Dados"
        biografia = request.form.get("biografia") or "Sem Dados"

        autor = Autor(
            id=None,
            nome=nome,
            nacionalidade=nacionalidade,
            data_nascimento=data_nascimento,
            biografia=biografia
        )
        autor.save()
        flash("Autor adicionado com sucesso!", "success")
        return redirect(url_for("autor.listar_autores"))

    return render_template("autores/adicionar_autor.html")


@autor_bp.route("/remover/<int:id>", methods=["POST"])
def remover_autor(id):
    autor = Autor.get(id)
    if autor:
        Autor.delete(id)
        flash("Autor removido com sucesso!", "success")
    else:
        flash("Autor não encontrado!", "error")
    return redirect(url_for("autor.listar_autores"))

@autor_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_autor(id):
    autor = Autor.get(id)
    if not autor:
        flash("Autor não encontrado!", "error")
        return redirect(url_for("autor.listar_autores"))

    if request.method == "POST":
        nome = request.form.get("nome")
        nacionalidade = request.form.get("nacionalidade") or None
        data_nascimento = request.form.get("data_nascimento") or None
        biografia = request.form.get("biografia") or None

        autor.update(nome, nacionalidade, data_nascimento, biografia)
        flash("Autor atualizado com sucesso!", "success")
        return redirect(url_for("autor.listar_autores"))

    return render_template("autores/editar_autor.html", autor=autor)