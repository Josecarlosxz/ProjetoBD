from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import Usuario
from datetime import date

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")

@usuario_bp.route("/")
def listar_usuarios():
    usuarios = Usuario.all()
    return render_template("users/usuarios.html", usuarios=usuarios)

@usuario_bp.route("/adicionar", methods=["GET", "POST"])
def adicionar_usuario():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email") or "Sem Email"
        telefone = request.form.get("numero") or "Sem Número"

        if not nome:
            flash("O nome do usuário é obrigatório!", "error")
            return redirect(url_for("usuario.adicionar_usuario"))

        data_inscricao = date.today()
        multa_atual = 0.00

        usuario = Usuario(
            id=None,
            nome=nome,
            email=email,
            numero=telefone,
            data_inscricao=data_inscricao,
            multa=multa_atual
        )
        usuario.save()
        flash("Usuário adicionado com sucesso!", "success")
        return redirect(url_for("usuario.listar_usuarios"))

    return render_template("users/adicionar_usuario.html")

@usuario_bp.route("/remover/<int:id>", methods=["POST"])
def remover_usuario(id):
    usuario = Usuario.get(id)
    if usuario:
        Usuario.delete(id)
        flash("Usuário removido com sucesso!", "success")
    else:
        flash("Usuário não encontrado!", "error")
    return redirect(url_for("usuario.listar_usuarios"))

@usuario_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    usuario = Usuario.get(id)
    if not usuario:
        flash("Usuário não encontrado!", "error")
        return redirect(url_for("usuario.listar_usuarios"))

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email") or "Sem Email"
        telefone = request.form.get("numero") or "Sem Número"
        multa_atual = request.form.get("multa_atual") or "0"

        try:
            multa_atual = float(multa_atual)
        except ValueError:
            multa_atual = 0.0

        usuario.update(nome, email, telefone, multa_atual)
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("usuario.listar_usuarios"))

    return render_template("users/editar_usuario.html", usuario=usuario)

@usuario_bp.route("/multa/<int:id>/adicionar", methods=["GET", "POST"])
def adicionar_multa(id):
    usuario = Usuario.get(id)
    if not usuario:
        flash("Usuário não encontrado!", "error")
        return redirect(url_for("usuario.listar_usuarios"))

    if request.method == "POST":
        valor = request.form.get("valor")
        try:
            valor = float(valor)
        except ValueError:
            flash("Valor inválido!", "error")
            return redirect(url_for("usuario.adicionar_multa", id=id))

        nova_multa = (usuario.multa or 0) + valor
        usuario.update(usuario.nome, usuario.email, usuario.numero, nova_multa)
        flash(f"Multa de R${valor:.2f} adicionada com sucesso!", "success")
        return redirect(url_for("usuario.listar_usuarios"))

    return render_template("users/adicionar_multa.html", usuario=usuario)