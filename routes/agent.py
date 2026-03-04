from flask import Blueprint, render_template
from models import db, CompanyInfo, Conversation, Property, Client
from routes.auth import login_required

agent_bp = Blueprint("agent", __name__)


@agent_bp.route("/agente")
@login_required
def index():
    company = CompanyInfo.query.first()
    messages_total = Conversation.query.filter_by(role="user").count()

    recent_messages = (
        Conversation.query.order_by(Conversation.created_at.desc())
        .limit(40)
        .all()
    )
    recent_messages = list(reversed(recent_messages))

    active_properties = Property.query.filter_by(active=True).order_by(Property.created_at.desc()).all()
    total_clients = Client.query.count()
    unique_users = db.session.query(
        db.func.count(db.func.distinct(Conversation.user_id))
    ).scalar() or 0

    return render_template(
        "agente.html",
        company=company,
        messages_total=messages_total,
        recent_messages=recent_messages,
        active_properties=active_properties,
        total_clients=total_clients,
        unique_users=unique_users,
    )
