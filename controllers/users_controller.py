from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.emprestimo import Emprestimo
from models.user import Usuario
from models.log_auditoria import LogAuditoria
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

        usuario = Usuario(
            id=None,
            nome=nome,
            email=email,
            numero=telefone,
            data_inscricao=None,
            multa=None
        )

        try:
            usuario.save()
            flash("Usuário adicionado com sucesso!", "success")
            return redirect(url_for("usuario.listar_usuarios"))

        except Exception as e:
            # Captura erro vindo da trigger
            msg = str(e.orig) if hasattr(e, "orig") else str(e)
            flash(msg, "error")
            return redirect(url_for("usuario.listar_usuarios"))
    return render_template("users/adicionar_usuario.html")

@usuario_bp.route("/remover/<int:id>", methods=["POST"])
def remover_usuario(id):
    num_emprestimos = Emprestimo.verificar_emprestimos_usuario(id)
    
    if num_emprestimos > 0:
        flash(f"Não é possível remover este usuário, pois ele possui {num_emprestimos} empréstimos. Se quiser remover-lo, remova os empréstimos primeiro.", "error")
    else:
        Usuario.delete(id)
        flash("Usuário removido com sucesso!", "success")
        
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

        try:
            usuario.update(nome, email, telefone, multa_atual)
            flash("Usuário atualizado com sucesso!", "success")

        except Exception as e:
            mensagem = e.orig.args[1]
            flash(mensagem, "error")

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

        nova_multa = float(usuario.multa or 0) + valor

        try:
            usuario.update(usuario.nome, usuario.email, usuario.numero, nova_multa)
            flash(f"Multa de R${valor:.2f} adicionada com sucesso!", "success")

        except Exception as e:
            mensagem = e.orig.args[1]
            flash(mensagem, "error")

        return redirect(url_for("usuario.listar_usuarios"))

    return render_template("users/adicionar_multa.html", usuario=usuario)

@usuario_bp.route("/logs")
def logs_usuarios():
    logs = LogAuditoria.listar_por_tabela("Usuarios")

    return render_template(
        "logs/logs.html",
        logs=logs,
        tabela="Usuários"
    )
