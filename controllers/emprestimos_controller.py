from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.emprestimo import Emprestimo
from datetime import date

from models.livros import Livro
from models.user import Usuario

emprestimo_bp = Blueprint("emprestimo", __name__, url_prefix="/emprestimos")


@emprestimo_bp.route("/")
def listar_emprestimos():
    emprestimos = Emprestimo.all()
    hoje = date.today()

    #Só pra exibir isso aqui
    for e in emprestimos:
        if e.status == "pendente" and e.data_prevista and e.data_prevista < hoje:
            e.status = "atrasado"

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

        #Função que pega a data atual e converte pra mandar pro banco
        data_emprestimo = hoje

        #Erro se vier alguma coisa faltando no formulário
        if not usuario_id or not livro_id or not data_prevista:
            flash("Preencha todos os campos obrigatórios!", "error")
            return redirect(url_for("emprestimo.adicionar_emprestimo"))
        
        #Verificando se o livro tá disponível pra emprestar
        livro = Livro.get(int(livro_id))
        if livro.quantidade <= 0:
            flash(f"O livro '{livro.titulo}' não está disponível no momento.", "error")
            return redirect(url_for("emprestimo.adicionar_emprestimo"))


        emprestimo = Emprestimo(
            id=None,
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_emprestimo=data_emprestimo,
            data_prevista=data_prevista,
            data_real=None,
            status="pendente"
        )
        emprestimo.save()


        #Diminuindo -1 na quantidade de livros disponíveis
        livro.quantidade -= 1
        livro.update(
            titulo=livro.titulo,
            isbn=livro.isbn,
            ano_publicacao=livro.ano_publicacao,
            autor_id=livro.autor_id,
            genero_id=livro.genero_id,
            editora_id=livro.editora_id,
            quantidade=livro.quantidade,
            resumo=livro.resumo
        )

        flash("Empréstimo registrado com sucesso!", "success")
        return redirect(url_for("emprestimo.listar_emprestimos"))
    return render_template("emprestimos/adicionar_emprestimo.html", usuarios=usuarios, livros=livros, hoje=hoje)

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
        data_prevista = request.form.get("data_prevista") or "Sem Dados"
        data_real = request.form.get("data_real") or "Sem Dados"
        status = request.form.get("status") or "pendente"

        emprestimo.usuario_id = usuario_id
        emprestimo.livro_id = livro_id
        emprestimo.data_prevista = data_prevista
        emprestimo.data_real = data_real
        emprestimo.status = status

        # Atualiza no banco
        emprestimo.update(
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_prevista=data_prevista,
            data_real=data_real,
            status=status
        )

        flash("Empréstimo atualizado com sucesso!", "success")
        return redirect(url_for("emprestimo.listar_emprestimos"))

    return render_template("emprestimos/editar_emprestimo.html", emprestimo=emprestimo, usuarios=usuarios, livros=livros)

@emprestimo_bp.route("/devolver/<int:id>", methods=["POST"])
def devolver_emprestimo(id):
    emprestimo = Emprestimo.get(id)
    if not emprestimo:
        flash("Empréstimo não encontrado!", "error")
        return redirect(url_for("emprestimo.listar_emprestimos"))

    data_real = date.today().isoformat()

    # Verifica se a devolução está atrasada
    if emprestimo.data_prevista and data_real > str(emprestimo.data_prevista):
        status = "devolvido com atraso"
    else:
        status = "devolvido"

    # Atualiza apenas data_real e status
    emprestimo.update(data_real=data_real, status=status)

    # Aumenta a quantidade disponível do livro
    livro = Livro.get(int(emprestimo.livro_id))
    livro.quantidade += 1
    livro.update(
        titulo=livro.titulo,
        isbn=livro.isbn,
        ano_publicacao=livro.ano_publicacao,
        autor_id=livro.autor_id,
        genero_id=livro.genero_id,
        editora_id=livro.editora_id,
        quantidade=livro.quantidade,
        resumo=livro.resumo
    )

    flash("Devolução registrada com sucesso!", "success")
    return redirect(url_for("emprestimo.listar_emprestimos"))

@emprestimo_bp.route("/remover/<int:id>", methods=["POST"])
def remover_emprestimo(id):
    emprestimo = Emprestimo.get(id)
    if emprestimo:
        Emprestimo.delete(id)
        flash("Empréstimo removido com sucesso!", "success")
    else:
        flash("Empréstimo não encontrado!", "error")
    return redirect(url_for("emprestimo.listar_emprestimos"))