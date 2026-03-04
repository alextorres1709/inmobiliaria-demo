from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, jsonify
from models import db, Conversation, Property, Client, Appointment
from routes.auth import login_required

stats_bp = Blueprint("stats", __name__)

INQUIRY_KEYWORDS = [
    'precio', 'cuanto', 'cuánto', 'disponible', 'visita', 'ver',
    'alquiler', 'comprar', 'venta', 'habitacion', 'habitación',
    'zona', 'barrio', 'metro', 'garaje', 'terraza', 'piscina',
    'hipoteca', 'financiación', 'financiacion', 'entrada',
    'cooperativa', 'obra nueva', 'piso piloto', 'personalización',
]


@stats_bp.route("/estadisticas")
@login_required
def index():
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    # User retention
    total_users = (
        db.session.query(db.func.count(db.func.distinct(Conversation.user_id)))
        .filter(Conversation.role == "user")
        .scalar()
    ) or 0

    returning_users = (
        db.session.query(db.func.count())
        .select_from(
            db.session.query(Conversation.user_id)
            .filter(Conversation.role == "user")
            .group_by(Conversation.user_id)
            .having(db.func.count(Conversation.id) > 1)
            .subquery()
        )
    ).scalar() or 0

    retention_rate = round((returning_users / total_users) * 100, 1) if total_users else 0
    new_users = total_users - returning_users

    # Appointments stats
    total_appointments = Appointment.query.count()
    completed_appointments = Appointment.query.filter_by(status="completed").count()
    cancelled_appointments = Appointment.query.filter_by(status="cancelled").count()
    confirmed_appointments = Appointment.query.filter_by(status="confirmed").count()
    pending_appointments = Appointment.query.filter_by(status="pending").count()
    conversion_rate = round((completed_appointments / total_appointments) * 100, 1) if total_appointments else 0

    # Appointment statuses for doughnut
    appointment_statuses = {
        'confirmed': confirmed_appointments,
        'pending': pending_appointments,
        'completed': completed_appointments,
        'cancelled': cancelled_appointments,
    }
    # Remove zeros
    appointment_statuses = {k: v for k, v in appointment_statuses.items() if v > 0}

    # Properties stats
    total_properties = Property.query.count()
    active_properties = Property.query.filter_by(active=True).count()
    avg_price_sale = db.session.query(db.func.avg(Property.price)).filter(
        Property.active == True, Property.listing_type == "Venta", Property.price > 0
    ).scalar() or 0
    avg_price_rent = db.session.query(db.func.avg(Property.price)).filter(
        Property.active == True, Property.listing_type == "Alquiler", Property.price > 0
    ).scalar() or 0

    # Client sources for doughnut
    source_counts = (
        db.session.query(Client.source, db.func.count(Client.id))
        .group_by(Client.source)
        .all()
    )
    client_sources = {r[0]: r[1] for r in source_counts}

    # Properties by city for doughnut
    city_counts = (
        db.session.query(Property.city, db.func.count(Property.id))
        .filter(Property.active == True)
        .group_by(Property.city)
        .all()
    )
    property_cities = {r[0]: r[1] for r in city_counts}

    # Property types for doughnut
    type_counts = (
        db.session.query(Property.property_type, db.func.count(Property.id))
        .filter(Property.active == True)
        .group_by(Property.property_type)
        .all()
    )
    property_types = {r[0]: r[1] for r in type_counts}

    return render_template(
        "estadisticas.html",
        total_users=total_users,
        returning_users=returning_users,
        new_users=new_users,
        retention_rate=retention_rate,
        total_appointments=total_appointments,
        completed_appointments=completed_appointments,
        cancelled_appointments=cancelled_appointments,
        conversion_rate=conversion_rate,
        total_properties=total_properties,
        active_properties=active_properties,
        avg_price_sale=avg_price_sale,
        avg_price_rent=avg_price_rent,
        appointment_statuses=appointment_statuses,
        client_sources=client_sources,
        property_cities=property_cities,
        property_types=property_types,
    )


@stats_bp.route("/api/stats/insights")
@login_required
def ai_insights():
    total_convos = Conversation.query.filter_by(role="user").count()
    if total_convos == 0:
        return jsonify({"topics": []})

    # Topic analysis
    topics = {}
    for kw in INQUIRY_KEYWORDS:
        count = Conversation.query.filter(
            Conversation.role == "user",
            Conversation.content.ilike(f"%{kw}%"),
        ).count()
        if count > 0:
            topics[kw] = count

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10]
    labels = [t[0].capitalize() for t in sorted_topics]
    values = [t[1] for t in sorted_topics]

    return jsonify({"labels": labels, "values": values})

