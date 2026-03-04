from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template
from models import db, Property, Client, Appointment, Conversation
from routes.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=now.weekday())
    month_start = today_start.replace(day=1)
    thirty_days_ago = today_start - timedelta(days=30)

    # Property KPIs
    total_properties = Property.query.count()
    active_properties = Property.query.filter_by(active=True).count()
    sale_count = Property.query.filter_by(active=True, listing_type="Venta").count()
    rent_count = Property.query.filter_by(active=True, listing_type="Alquiler").count()

    # Client KPIs
    total_clients = Client.query.count()
    new_clients_month = Client.query.filter(Client.created_at >= month_start).count()

    # Appointment KPIs
    today_appointments = Appointment.query.filter(
        Appointment.date >= today_start,
        Appointment.date < today_start + timedelta(days=1),
    ).count()
    week_appointments = Appointment.query.filter(
        Appointment.date >= week_start,
        Appointment.date < week_start + timedelta(days=7),
    ).count()
    pending_appointments = Appointment.query.filter_by(status="pending").count()

    # Conversation KPIs
    messages_total = Conversation.query.filter_by(role="user").count()
    messages_today = Conversation.query.filter(
        Conversation.role == "user", Conversation.created_at >= today_start
    ).count()

    # Upcoming appointments (next 5)
    upcoming_appointments = (
        Appointment.query.filter(Appointment.date >= now, Appointment.status.in_(["pending", "confirmed"]))
        .order_by(Appointment.date.asc())
        .limit(5)
        .all()
    )

    # Daily messages chart (last 30 days)
    daily_rows = (
        db.session.query(
            db.func.date(Conversation.created_at).label("day"),
            db.func.count(Conversation.id),
        )
        .filter(Conversation.role == "user", Conversation.created_at >= thirty_days_ago)
        .group_by("day")
        .all()
    )
    daily_map = {str(r[0]): r[1] for r in daily_rows}
    daily_messages = []
    for i in range(30):
        day = thirty_days_ago + timedelta(days=i)
        key = day.strftime("%Y-%m-%d")
        daily_messages.append({"date": day.strftime("%d/%m"), "count": daily_map.get(key, 0)})

    # Appointments by status for doughnut
    status_counts = (
        db.session.query(Appointment.status, db.func.count(Appointment.id))
        .group_by(Appointment.status)
        .all()
    )
    appointment_statuses = {r[0]: r[1] for r in status_counts}

    # Client sources for doughnut
    source_counts = (
        db.session.query(Client.source, db.func.count(Client.id))
        .group_by(Client.source)
        .all()
    )
    client_sources = {r[0]: r[1] for r in source_counts}

    # Property types for doughnut
    type_counts = (
        db.session.query(Property.property_type, db.func.count(Property.id))
        .filter(Property.active == True)
        .group_by(Property.property_type)
        .all()
    )
    property_types = {r[0]: r[1] for r in type_counts}

    # Properties by city for doughnut
    city_counts = (
        db.session.query(Property.city, db.func.count(Property.id))
        .filter(Property.active == True)
        .group_by(Property.city)
        .all()
    )
    property_cities = {r[0]: r[1] for r in city_counts}

    return render_template(
        "dashboard.html",
        total_properties=total_properties,
        active_properties=active_properties,
        sale_count=sale_count,
        rent_count=rent_count,
        total_clients=total_clients,
        new_clients_month=new_clients_month,
        today_appointments=today_appointments,
        week_appointments=week_appointments,
        pending_appointments=pending_appointments,
        messages_total=messages_total,
        messages_today=messages_today,
        upcoming_appointments=upcoming_appointments,
        daily_messages=daily_messages,
        hourly_messages=[],
        appointment_statuses=appointment_statuses,
        client_sources=client_sources,
        property_types=property_types,
        property_cities=property_cities,
    )
