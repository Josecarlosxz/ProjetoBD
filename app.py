from flask import Flask, render_template
from controllers.autores_controller import autor_bp
from controllers.genero_controller import genero_bp
from controllers.livros_controller import livro_bp
from controllers.editoras_controllers import editora_bp
from controllers.emprestimos_controller import emprestimo_bp
from controllers.users_controller import usuario_bp

app = Flask(__name__)

app.secret_key = "Chave Secreta Dms"

app.register_blueprint(autor_bp, url_prefix="/autores")
app.register_blueprint(genero_bp, url_prefix="/generos")
app.register_blueprint(livro_bp, url_prefix="/livros")
app.register_blueprint(editora_bp, url_prefix="/editoras")
app.register_blueprint(emprestimo_bp, url_prefix="/emprestimos")
app.register_blueprint(usuario_bp, url_prefix="/usuarios")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
