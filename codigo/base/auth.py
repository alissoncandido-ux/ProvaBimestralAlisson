from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha nome, e-mail e senha.")
            return redirect(url_for("auth.registro"))

        if database.buscar_usuario_por_email(email):
            flash("E-mail já cadastrado.")
            return redirect(url_for("auth.registro"))

        senha_hash = generate_password_hash(senha)
        usuario = database.criar_usuario(nome, email, senha_hash)

        if usuario:
            flash("Cadastro realizado com sucesso.")
            return redirect(url_for("auth.login"))

        flash("Não foi possível concluir o cadastro.")
        return redirect(url_for("auth.registro"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")

        if not email or not senha:
            flash("Informe e-mail e senha.")
            return redirect(url_for("auth.login"))

        usuario = database.buscar_usuario_por_email(email)
        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash("Credenciais inválidas.")
            return redirect(url_for("auth.login"))

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        flash(f"Bem-vindo, {usuario.nome}!")
        return redirect(url_for("leituras.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso.")
    return redirect(url_for("auth.login"))
