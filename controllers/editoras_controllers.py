from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.editoras import Editora

editora_bp = Blueprint("editora", __name__, url_prefix="/editoras")

@editora_bp.route("/")
def listar_editoras():
    editoras = Editora.all()
    return render_template("editoras/editoras.html", editoras=editoras)

@editora_bp.route("/adicionar", methods=["GET", "POST"])
def adicionar_editora():
    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco") or None

        if not nome:
            flash("O nome da editora é obrigatório!", "error")
            return redirect(url_for("editora.adicionar_editora"))

        editora = Editora(id=None, nome=nome, endereco=endereco)
        editora.save()
        flash("Editora adicionada com sucesso!", "success")
        return redirect(url_for("editora.listar_editoras"))

    return render_template("editoras/adicionar_editora.html")

@editora_bp.route("/remover/<int:id>", methods=["POST"])
def remover_editora(id):
    editora = Editora.get(id)
    if editora:
        Editora.delete(id)
        flash("Editora removida com sucesso!", "success")
    else:
        flash("Editora não encontrada!", "error")
    return redirect(url_for("editora.listar_editoras"))

@editora_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_editora(id):
    editora = Editora.get(id)
    if not editora:
        flash("Editora não encontrada!", "error")
        return redirect(url_for("editora.listar_editoras"))

    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco") or "Sem Endereço"

        editora.update(nome, endereco)
        flash("Editora atualizada com sucesso!", "success")
        return redirect(url_for("editora.listar_editoras"))

    return render_template("editoras/editar_editora.html", editora=editora)