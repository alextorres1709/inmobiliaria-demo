from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

ROLE_ADMIN = "admin"
ROLE_EDITOR = "editor"
ROLE_VIEWER = "viewer"
ROLES = [ROLE_ADMIN, ROLE_EDITOR, ROLE_VIEWER]

PROPERTY_TYPES = ["Piso", "Casa", "Chalet", "Local", "Oficina", "Terreno", "Garaje", "Otro"]
LISTING_TYPES = ["Venta", "Alquiler"]
APPOINTMENT_STATUSES = ["pending", "confirmed", "cancelled", "completed"]
CLIENT_SOURCES = ["Web", "Telegram", "WhatsApp", "Referido", "Portal", "Otro"]


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(200), default="")
    role = db.Column(db.String(20), nullable=False, default=ROLE_VIEWER)
    active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def can_manage_properties(self):
        return self.role in (ROLE_ADMIN, ROLE_EDITOR)

    @property
    def can_manage_settings(self):
        return self.role == ROLE_ADMIN

    @property
    def can_manage_users(self):
        return self.role == ROLE_ADMIN

    def to_dict(self):
        return {
            "id": self.id, "email": self.email, "name": self.name,
            "role": self.role, "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    listing_type = db.Column(db.String(20), nullable=False, default="Venta")
    property_type = db.Column(db.String(50), nullable=False, default="Piso")
    price = db.Column(db.Float, default=0)
    address = db.Column(db.String(500), default="")
    city = db.Column(db.String(100), default="")
    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Integer, default=0)
    sqm = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, default="")
    features = db.Column(db.Text, default="")
    image_url = db.Column(db.String(500), default="")
    contact_phone = db.Column(db.String(50), default="")
    active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    appointments = db.relationship("Appointment", backref="property", lazy="dynamic")

    @property
    def price_formatted(self):
        if self.price:
            return f"{self.price:,.0f}".replace(",", ".")
        return "Consultar"

    def to_dict(self):
        return {
            "id": self.id, "title": self.title,
            "listing_type": self.listing_type, "property_type": self.property_type,
            "price": self.price, "address": self.address, "city": self.city,
            "bedrooms": self.bedrooms, "bathrooms": self.bathrooms, "sqm": self.sqm,
            "description": self.description, "features": self.features,
            "image_url": self.image_url, "contact_phone": self.contact_phone,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), default="")
    email = db.Column(db.String(200), default="")
    source = db.Column(db.String(50), default="Web")
    notes = db.Column(db.Text, default="")
    telegram_id = db.Column(db.String(100), default="", index=True)
    active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    appointments = db.relationship("Appointment", backref="client", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "phone": self.phone,
            "email": self.email, "source": self.source, "notes": self.notes,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=True, index=True)
    date = db.Column(db.DateTime, nullable=False, index=True)
    duration = db.Column(db.Integer, default=30)  # minutes
    status = db.Column(db.String(20), default="pending", index=True)
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id, "client_id": self.client_id,
            "property_id": self.property_id,
            "date": self.date.isoformat() if self.date else None,
            "duration": self.duration, "status": self.status, "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def to_dict(self):
        return {
            "id": self.id, "user_id": self.user_id, "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class CompanyInfo(db.Model):
    __tablename__ = "company_info"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), default="Mi Inmobiliaria")
    description = db.Column(db.Text, default="Agencia inmobiliaria")
    phone = db.Column(db.String(50), default="")
    email = db.Column(db.String(200), default="")
    address = db.Column(db.String(300), default="")
    hours = db.Column(db.String(200), default="")
    extra_info = db.Column(db.Text, default="")

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "description": self.description,
            "phone": self.phone, "email": self.email, "address": self.address,
            "hours": self.hours, "extra_info": self.extra_info,
        }


class ActivityLog(db.Model):
    __tablename__ = "activity_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    action = db.Column(db.String(50), nullable=False, index=True)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    user = db.relationship("User", backref=db.backref("activity_logs", lazy="dynamic"))
