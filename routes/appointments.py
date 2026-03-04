from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Appointment, Client, Property, APPOINTMENT_STATUSES
from routes.auth import login_required, editor_required
from services.activity import log_activity

appointments_bp = Blueprint("appointments", __name__)


@appointments_bp.route("/citas")
@login_required
def index():
    status_filter = request.args.get("status", "").strip()
    date_filter = request.args.get("date", "").strip()

    query = Appointment.query

    if status_filter:
        query = query.filter_by(status=status_filter)
    if date_filter:
        try:
            day = datetime.fromisoformat(date_filter)
            next_day = day.replace(hour=23, minute=59, second=59)
            query = query.filter(Appointment.date >= day, Appointment.date <= next_day)
        except ValueError:
            pass

    appointments = query.order_by(Appointment.date.desc()).all()
    clients = Client.query.filter_by(active=True).order_by(Client.name).all()
    properties = Property.query.filter_by(active=True).order_by(Property.title).all()

    return render_template(
        "citas.html",
        appointments=appointments,
        clients=clients,
        properties=properties,
        statuses=APPOINTMENT_STATUSES,
        selected_status=status_filter,
        selected_date=date_filter,
    )


@appointments_bp.route("/citas/create", methods=["POST"])
@editor_required
def create():
    try:
        appt = Appointment(
            client_id=int(request.form.get("client_id")),
            property_id=int(request.form.get("property_id")) if request.form.get("property_id") else None,
            date=datetime.fromisoformat(request.form.get("date", "")),
            duration=int(request.form.get("duration", 30) or 30),
            status=request.form.get("status", "pending"),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(appt)
        client = db.session.get(Client, appt.client_id)
        log_activity("create", "appointment", details=f"Cita con {client.name if client else 'cliente'}")
        db.session.commit()
        flash("Cita creada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear la cita: {str(e)}", "error")
    return redirect(url_for("appointments.index"))


@appointments_bp.route("/citas/<int:appt_id>/update", methods=["POST"])
@editor_required
def update(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    try:
        appt.client_id = int(request.form.get("client_id", appt.client_id))
        prop_id = request.form.get("property_id")
        appt.property_id = int(prop_id) if prop_id else None
        appt.date = datetime.fromisoformat(request.form.get("date", appt.date.isoformat()))
        appt.duration = int(request.form.get("duration", appt.duration) or 30)
        appt.status = request.form.get("status", appt.status)
        appt.notes = request.form.get("notes", appt.notes).strip()
        log_activity("update", "appointment", appt.id, f"Updated appointment #{appt.id}")
        db.session.commit()
        flash("Cita actualizada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {str(e)}", "error")
    return redirect(url_for("appointments.index"))


@appointments_bp.route("/citas/<int:appt_id>/status/<status>", methods=["POST"])
@editor_required
def change_status(appt_id, status):
    appt = Appointment.query.get_or_404(appt_id)
    if status in APPOINTMENT_STATUSES:
        appt.status = status
        log_activity("update", "appointment", appt.id, f"Status → {status}")
        db.session.commit()
        labels = {"pending": "pendiente", "confirmed": "confirmada", "cancelled": "cancelada", "completed": "completada"}
        flash(f"Cita {labels.get(status, status)}", "success")
    return redirect(url_for("appointments.index"))


@appointments_bp.route("/citas/<int:appt_id>/delete", methods=["POST"])
@editor_required
def delete(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    try:
        log_activity("delete", "appointment", appt_id, f"Deleted appointment #{appt_id}")
        db.session.delete(appt)
        db.session.commit()
        flash("Cita eliminada", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "error")
    return redirect(url_for("appointments.index"))
