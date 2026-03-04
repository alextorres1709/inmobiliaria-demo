from datetime import datetime, timezone
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from models import db, Property, CompanyInfo, Conversation

api_bp = Blueprint("api", __name__, url_prefix="/api")


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key", "")
        if api_key != current_app.config["API_KEY"]:
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated


@api_bp.route("/properties", methods=["GET"])
@require_api_key
def get_properties():
    show_all = request.args.get("all", "false").lower() == "true"
    if show_all:
        props = Property.query.order_by(Property.created_at.desc()).all()
    else:
        props = Property.query.filter_by(active=True).order_by(Property.created_at.desc()).all()
    return jsonify([p.to_dict() for p in props])


@api_bp.route("/properties", methods=["POST"])
@require_api_key
def create_property():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        prop = Property(
            title=data.get("title", ""),
            listing_type=data.get("listing_type", "Venta"),
            property_type=data.get("property_type", "Piso"),
            price=float(data.get("price", 0)),
            address=data.get("address", ""),
            city=data.get("city", ""),
            bedrooms=int(data.get("bedrooms", 0)),
            bathrooms=int(data.get("bathrooms", 0)),
            sqm=int(data.get("sqm", 0)),
            description=data.get("description", ""),
            features=data.get("features", ""),
            image_url=data.get("image_url", ""),
            active=data.get("active", True),
        )
        db.session.add(prop)
        db.session.commit()
        return jsonify(prop.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@api_bp.route("/conversations", methods=["POST"])
@require_api_key
def log_conversation():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        convo = Conversation(
            user_id=data.get("user_id", "unknown"),
            role=data.get("role", "user"),
            content=data.get("content", ""),
        )
        db.session.add(convo)
        db.session.commit()
        return jsonify(convo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@api_bp.route("/company-info", methods=["GET"])
@require_api_key
def get_company_info():
    company = CompanyInfo.query.first()
    if not company:
        return jsonify({"error": "No company info found"}), 404
    return jsonify(company.to_dict())
