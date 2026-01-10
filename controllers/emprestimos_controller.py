from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.emprestimo import Emprestimo
from datetime import date, datetime
from models.log_auditoria import LogAuditoria
from models.livros import Livro
from models.user import Usuario

emprestimo_bp = Blueprint("emprestimo", __name__, url_prefix="/emprestimos")


@emprestimo_bp.route("/")
def listar_emprestimos():
    emprestimos = Emprestimo.all()

    return render_template("emprestimos/emprestimos.html", emprestimos=emprestimos, Usuario=Usuario, Livro=Livro)

@emprestimo_bp.route("/adicionar", methods=["GET", "POST"])
def adicionar_emprestimo():
    usuarios = Usuario.all()
    livros = Livro.all()
    hoje = date.today().isoformat()

    if request.method == "POST":
        usuario_id = request.form.get("usuario_id")
        livro_id = request.form.get("livro_id")
        data_prevista = request.form.get("data_prevista") or None

        if not usuario_id or not livro_id or not data_prevista:
            flash("Preencha todos os campos obrigatórios!", "error")
            return redirect(url_for("emprestimo.adicionar_emprestimo"))

        emprestimo = Emprestimo(
            id=None,
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_emprestimo=hoje,
            data_prevista=data_prevista,
            data_real=None,
            status=None #EXEMPLO DE GATILHO DE GERAÇÃO AUTOMÁTICA DE VALORES !!!!!!!!!  
        )

        try:
            emprestimo.save()
            flash("Empréstimo registrado com sucesso!", "success")

        except Exception as e:
            msg = str(e.orig) if hasattr(e, "orig") else str(e)
            flash(msg, "error")

        return redirect(url_for("emprestimo.listar_emprestimos"))

    return render_template("emprestimos/adicionar_emprestimo.html", usuarios=usuarios,livros=livros,hoje=hoje)


@emprestimo_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_emprestimo(id):
    emprestimo = Emprestimo.get(id)
    usuarios = Usuario.all()
    livros = Livro.all()
    if not emprestimo:
        flash("Empréstimo não encontrado!", "error")
        return redirect(url_for("emprestimo.listar_emprestimos"))

    if request.method == "POST":
        usuario_id = request.form.get("usuario_id")
        livro_id = request.form.get("livro_id")
        data_prevista = request.form.get("data_prevista") or None
        data_real = request.form.get("data_real") or None

        emprestimo.usuario_id = usuario_id
        emprestimo.livro_id = livro_id
        emprestimo.data_prevista = data_prevista
        emprestimo.data_real = data_real

        try:
            emprestimo.update(
                usuario_id=usuario_id,
                livro_id=livro_id,
                data_prevista=data_prevista,
                data_real=data_real,
            )
            flash("Empréstimo atualizado com sucesso!", "success")

        except Exception as e:
            msg = str(e.orig) if hasattr(e, "orig") else str(e)
            flash(msg, "error")

        return redirect(url_for("emprestimo.listar_emprestimos"))

    return render_template("emprestimos/editar_emprestimo.html", emprestimo=emprestimo, usuarios=usuarios, livros=livros)

@emprestimo_bp.route("/devolver/<int:id>", methods=["POST"])
def devolver_emprestimo(id):
    emprestimo = Emprestimo.get(id)
    if not emprestimo:
        flash("Empréstimo não encontrado!", "error")
        return redirect(url_for("emprestimo.listar_emprestimos"))

    try:
        emprestimo.update(
            usuario_id=emprestimo.usuario_id,
            livro_id=emprestimo.livro_id,
            data_prevista=emprestimo.data_prevista,
            data_real=date.today().isoformat(),
            status="devolvido"
        )
        flash("Devolução registrada com sucesso!", "success")

    except Exception as e:
        msg = str(e.orig) if hasattr(e, "orig") else str(e)
        flash(msg, "error")

    return redirect(url_for("emprestimo.listar_emprestimos"))


@emprestimo_bp.route("/remover/<int:id>", methods=["POST"])
def remover_emprestimo(id):
    emprestimo = Emprestimo.get(id)
    if emprestimo:
        try:
            Emprestimo.delete(id)
            flash("Empréstimo removido com sucesso!", "success")
        except Exception as e:
            msg = str(e.orig) if hasattr(e, "orig") else str(e)
            flash(msg, "error")
    else:
        flash("Empréstimo não encontrado!", "error")
    return redirect(url_for("emprestimo.listar_emprestimos"))

@emprestimo_bp.route("/logs")
def logs_emprestimos():
    logs = LogAuditoria.listar_por_tabela("Emprestimos")

    return render_template(
        "logs/logs.html",
        logs=logs,
        tabela="Empréstimos"
    )
