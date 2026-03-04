from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Client, CLIENT_SOURCES
from routes.auth import login_required, editor_required
from services.activity import log_activity

clients_bp = Blueprint("clients", __name__)


@clients_bp.route("/clientes")
@login_required
def index():
    search = request.args.get("search", "").strip()
    source_filter = request.args.get("source", "").strip()

    query = Client.query

    if search:
        query = query.filter(
            db.or_(
                Client.name.ilike(f"%{search}%"),
                Client.email.ilike(f"%{search}%"),
                Client.phone.ilike(f"%{search}%"),
            )
        )
    if source_filter:
        query = query.filter_by(source=source_filter)

    clients = query.order_by(Client.created_at.desc()).all()

    return render_template(
        "clientes.html",
        clients=clients,
        sources=CLIENT_SOURCES,
        search=search,
        selected_source=source_filter,
    )


@clients_bp.route("/clientes/create", methods=["POST"])
@editor_required
def create():
    try:
        client = Client(
            name=request.form.get("name", "").strip(),
            phone=request.form.get("phone", "").strip(),
            email=request.form.get("email", "").strip(),
            source=request.form.get("source", "Web"),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(client)
        log_activity("create", "client", details=f"Created client: {client.name}")
        db.session.commit()
        flash("Cliente creado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear el cliente: {str(e)}", "error")
    return redirect(url_for("clients.index"))


@clients_bp.route("/clientes/<int:client_id>/update", methods=["POST"])
@editor_required
def update(client_id):
    client = Client.query.get_or_404(client_id)
    try:
        client.name = request.form.get("name", client.name).strip()
        client.phone = request.form.get("phone", client.phone).strip()
        client.email = request.form.get("email", client.email).strip()
        client.source = request.form.get("source", client.source)
        client.notes = request.form.get("notes", client.notes).strip()
        log_activity("update", "client", client.id, f"Updated client: {client.name}")
        db.session.commit()
        flash("Cliente actualizado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {str(e)}", "error")
    return redirect(url_for("clients.index"))


@clients_bp.route("/clientes/<int:client_id>/delete", methods=["POST"])
@editor_required
def delete(client_id):
    client = Client.query.get_or_404(client_id)
    try:
        log_activity("delete", "client", client_id, f"Deleted client: {client.name}")
        db.session.delete(client)
        db.session.commit()
        flash("Cliente eliminado", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "error")
    return redirect(url_for("clients.index"))
