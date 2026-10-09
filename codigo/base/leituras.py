from flask import Blueprint, flash, redirect, render_template, request, session, url_for

import database
from seguranca import exigir_login


leituras_bp = Blueprint("leituras", __name__)


@leituras_bp.route("/leituras")
def index():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    leituras = database.listar_leituras(session["usuario_id"])
    return render_template("leituras.html", leituras=leituras)


@leituras_bp.route("/leituras/nova", methods=["GET", "POST"])
def nova_leitura():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        titulo = request.form.get("titulo", "")
        autor = request.form.get("autor", "")
        paginas_texto = request.form.get("paginas", "")

        if not titulo or not autor or not paginas_texto:
            flash("Preencha título, autor e páginas.")
            return redirect(url_for("leituras.nova_leitura"))

        try:
            paginas = int(paginas_texto)
        except (TypeError, ValueError):
            flash("Número de páginas inválido.")
            return redirect(url_for("leituras.nova_leitura"))

        database.criar_leitura(session["usuario_id"], titulo, autor, paginas)
        flash("Leitura cadastrada.")
        return redirect(url_for("leituras.index"))

    return render_template("nova_leitura.html")


@leituras_bp.route("/leituras/<int:leitura_id>/editar", methods=["GET", "POST"])
def editar_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    leitura = database.buscar_leitura(leitura_id, session["usuario_id"])
    if leitura is None:
        flash("Leitura não encontrada ou não pertence a você.")
        return redirect(url_for("leituras.index"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "")
        autor = request.form.get("autor", "")
        paginas_texto = request.form.get("paginas", "")

        if not titulo or not autor or not paginas_texto:
            flash("Preencha título, autor e páginas.")
            return redirect(url_for("leituras.editar_leitura", leitura_id=leitura_id))

        try:
            paginas = int(paginas_texto)
        except (TypeError, ValueError):
            flash("Número de páginas inválido.")
            return redirect(url_for("leituras.editar_leitura", leitura_id=leitura_id))

        database.atualizar_leitura(leitura_id, titulo, autor, paginas, session["usuario_id"])
        flash("Leitura atualizada.")
        return redirect(url_for("leituras.index"))

    return render_template("editar_leitura.html", leitura=leitura)


@leituras_bp.post("/leituras/<int:leitura_id>/concluir")
def concluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    if not database.alternar_concluida(leitura_id, session["usuario_id"]):
        flash("Leitura não encontrada ou não pertence a você.")
        return redirect(url_for("leituras.index"))

    flash("Status da leitura atualizado.")
    return redirect(url_for("leituras.index"))


@leituras_bp.post("/leituras/<int:leitura_id>/excluir")
def excluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    if not database.excluir_leitura(leitura_id, session["usuario_id"]):
        flash("Leitura não encontrada ou não pertence a você.")
        return redirect(url_for("leituras.index"))

    flash("Leitura excluída.")
    return redirect(url_for("leituras.index"))
