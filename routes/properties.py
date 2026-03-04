import csv
import io
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from models import db, Property, PROPERTY_TYPES, LISTING_TYPES
from routes.auth import login_required, editor_required
from services.activity import log_activity

properties_bp = Blueprint("properties", __name__)


@properties_bp.route("/propiedades")
@login_required
def index():
    search = request.args.get("search", "").strip()
    listing_filter = request.args.get("listing_type", "").strip()
    type_filter = request.args.get("property_type", "").strip()
    status = request.args.get("status", "").strip()

    query = Property.query

    if search:
        query = query.filter(
            db.or_(
                Property.title.ilike(f"%{search}%"),
                Property.address.ilike(f"%{search}%"),
                Property.city.ilike(f"%{search}%"),
            )
        )
    if listing_filter:
        query = query.filter_by(listing_type=listing_filter)
    if type_filter:
        query = query.filter_by(property_type=type_filter)
    if status == "active":
        query = query.filter_by(active=True)
    elif status == "inactive":
        query = query.filter_by(active=False)

    properties = query.order_by(Property.created_at.desc()).all()

    return render_template(
        "propiedades.html",
        properties=properties,
        property_types=PROPERTY_TYPES,
        listing_types=LISTING_TYPES,
        search=search,
        selected_listing=listing_filter,
        selected_type=type_filter,
        selected_status=status,
    )


@properties_bp.route("/propiedades/create", methods=["POST"])
@editor_required
def create():
    try:
        prop = Property(
            title=request.form.get("title", "").strip(),
            listing_type=request.form.get("listing_type", "Venta"),
            property_type=request.form.get("property_type", "Piso"),
            price=float(request.form.get("price", 0) or 0),
            address=request.form.get("address", "").strip(),
            city=request.form.get("city", "").strip(),
            bedrooms=int(request.form.get("bedrooms", 0) or 0),
            bathrooms=int(request.form.get("bathrooms", 0) or 0),
            sqm=int(request.form.get("sqm", 0) or 0),
            description=request.form.get("description", "").strip(),
            features=request.form.get("features", "").strip(),
            image_url=request.form.get("image_url", "").strip(),
            contact_phone=request.form.get("contact_phone", "").strip(),
            active=request.form.get("active") == "on",
        )
        db.session.add(prop)
        log_activity("create", "property", details=f"Created property: {prop.title}")
        db.session.commit()
        flash("Propiedad creada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear la propiedad: {str(e)}", "error")
    return redirect(url_for("properties.index"))


@properties_bp.route("/propiedades/<int:prop_id>/update", methods=["POST"])
@editor_required
def update(prop_id):
    prop = Property.query.get_or_404(prop_id)
    try:
        prop.title = request.form.get("title", prop.title).strip()
        prop.listing_type = request.form.get("listing_type", prop.listing_type)
        prop.property_type = request.form.get("property_type", prop.property_type)
        prop.price = float(request.form.get("price", prop.price) or 0)
        prop.address = request.form.get("address", prop.address).strip()
        prop.city = request.form.get("city", prop.city).strip()
        prop.bedrooms = int(request.form.get("bedrooms", prop.bedrooms) or 0)
        prop.bathrooms = int(request.form.get("bathrooms", prop.bathrooms) or 0)
        prop.sqm = int(request.form.get("sqm", prop.sqm) or 0)
        prop.description = request.form.get("description", prop.description).strip()
        prop.features = request.form.get("features", prop.features).strip()
        prop.image_url = request.form.get("image_url", prop.image_url).strip()
        prop.contact_phone = request.form.get("contact_phone", prop.contact_phone).strip()
        prop.active = request.form.get("active") == "on"
        log_activity("update", "property", prop.id, f"Updated property: {prop.title}")
        db.session.commit()
        flash("Propiedad actualizada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {str(e)}", "error")
    return redirect(url_for("properties.index"))


@properties_bp.route("/propiedades/<int:prop_id>/delete", methods=["POST"])
@editor_required
def delete(prop_id):
    prop = Property.query.get_or_404(prop_id)
    try:
        log_activity("delete", "property", prop_id, f"Deleted property: {prop.title}")
        db.session.delete(prop)
        db.session.commit()
        flash("Propiedad eliminada", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "error")
    return redirect(url_for("properties.index"))


@properties_bp.route("/propiedades/<int:prop_id>/toggle", methods=["POST"])
@editor_required
def toggle(prop_id):
    prop = Property.query.get_or_404(prop_id)
    prop.active = not prop.active
    log_activity("toggle", "property", prop.id, f"Toggled property: {prop.title}")
    db.session.commit()
    flash(f"Propiedad {'activada' if prop.active else 'desactivada'}", "success")
    return redirect(url_for("properties.index"))


@properties_bp.route("/propiedades/export/csv")
@login_required
def export_csv():
    props = Property.query.order_by(Property.created_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Título", "Tipo", "Operación", "Precio", "Ciudad", "Dirección", "Hab.", "Baños", "m²", "Estado"])
    for p in props:
        writer.writerow([
            p.title, p.property_type, p.listing_type, p.price,
            p.city, p.address, p.bedrooms, p.bathrooms, p.sqm,
            "Activa" if p.active else "Inactiva",
        ])
    output.seek(0)
    return Response(
        output.getvalue(), mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=propiedades_export.csv"},
    )
