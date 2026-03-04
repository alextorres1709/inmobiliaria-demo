from flask import Flask, redirect, url_for, g
from config import Config
from models import db, CompanyInfo, User, Property, Client, Appointment, Conversation
from datetime import datetime, timedelta, timezone
import random


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()

            if not CompanyInfo.query.first():
                company = CompanyInfo(
                    name="Asentis — Grupo Promotor y Constructor",
                    description="Grupo empresarial promotor y constructor especializado en promociones inmobiliarias de obra nueva. Viviendas exclusivas: pisos, áticos y chalets en las mejores ubicaciones de Madrid.",
                    phone="+34 917 140 435",
                    email="info@asentis.es",
                    address="Avda. Europa 26, Edificio Ática 5, 3ª Planta, 28224 Pozuelo de Alarcón, Madrid",
                    hours="Lunes a Jueves: 10:00 - 14:00 y 16:00 - 19:00 | Viernes: 10:00 - 14:00",
                    extra_info=(
                        "SOBRE ASENTIS:\n"
                        "- Grupo empresarial promotor y constructor\n"
                        "- Especialistas en obra nueva de calidad en Madrid y alrededores\n"
                        "- Integración de todo el proceso inmobiliario\n\n"
                        "MISIÓN:\n"
                        "Crear inmuebles de calidad que respondan a las necesidades de nuestros clientes, "
                        "integrando todo el proceso inmobiliario, actuando con ética y generando valor "
                        "para clientes, equipo y sociedad.\n\n"
                        "VISIÓN:\n"
                        "Ser un grupo inmobiliario de referencia en España, reconocido por su profesionalidad, "
                        "calidad y ética.\n\n"
                        "PROMOCIONES EN COMERCIALIZACIÓN:\n"
                        "- Los Cerros Horizon (Madrid Este): 181 viviendas VPPB desde 250.500€+IVA\n"
                        "- Torrejón Class II (Torrejón de Ardoz): 45 viviendas desde 395.900€+IVA\n"
                        "- Entrenúcleos Class (Dos Hermanas, Sevilla): desde 235.900€+IVA\n"
                        "- Ciempozuelos Horizon: 44 viviendas adosadas desde 305.900€+IVA\n"
                        "- Boadilla Infinity: chalets exclusivos desde 1.225.000€+IVA\n"
                        "- Boadilla Infinity II: chalets desde 1.195.000€+IVA\n"
                        "- Cadmia Residencial II: desde 545.000€+IVA\n"
                        "- Ahijones Horizon II: últimas viviendas desde 263.800€+IVA\n\n"
                        "PERSONALIZACIÓN:\n"
                        "Ofrecemos un servicio de personalización de viviendas para que cada cliente "
                        "pueda adaptar su nuevo hogar a sus gustos y necesidades.\n\n"
                        "VISITAS A PISOS PILOTO:\n"
                        "Se pueden reservar citas para visitar nuestros pisos piloto a través de "
                        "asentis.appointlet.com o llamando al 91 714 04 35.\n\n"
                        "CONTACTO:\n"
                        "- Teléfono oficinas: 91 714 04 35\n"
                        "- Email comercial: info@asentis.es\n"
                        "- Recepción: recepcion@asentis.es\n"
                        "- Cita previa pisos piloto: 91 112 49 23\n"
                        "- Sede: Pozuelo de Alarcón, Madrid"
                    ),
                )
                db.session.add(company)
                db.session.commit()

            if not User.query.first():
                admin = User(
                    email=app.config["ADMIN_EMAIL"].lower(),
                    name="Admin Asentis",
                    role="admin",
                    active=True,
                )
                admin.set_password(app.config["ADMIN_PASSWORD"])
                db.session.add(admin)

                editor = User(email="comercial@asentis.es", name="Lucía Romero", role="editor", active=True)
                editor.set_password("editor123")
                db.session.add(editor)

                viewer = User(email="recepcion@asentis.es", name="Marta Delgado", role="viewer", active=True)
                viewer.set_password("viewer123")
                db.session.add(viewer)

                db.session.commit()

            # ── Seed rich demo data ──────────────────────
            if not Property.query.first():
                now = datetime.now(timezone.utc)
                props = [
                    # ── PROMOCIONES EN COMERCIALIZACIÓN ──
                    Property(title="Los Cerros Horizon — Piso 3 dormitorios Tipo A",
                             listing_type="Venta", property_type="Piso",
                             price=250500, address="Barrio de Los Cerros, Madrid Este", city="Madrid",
                             bedrooms=3, bathrooms=2, sqm=85,
                             description="Promoción de 181 viviendas VPPB en régimen de cooperativa en el nuevo barrio de Los Cerros, al este de Madrid. Incluye 1 plaza de garaje, trastero y plaza de bicicletas. Zonas comunes con piscina, áreas ajardinadas y sala comunitaria. Ubicación estratégica con excelentes conexiones.",
                             features="Garaje, Trastero, Piscina comunitaria, Zonas ajardinadas, Sala comunitaria, Plaza bicicletas",
                             active=True, created_at=now - timedelta(days=5)),

                    Property(title="Los Cerros Horizon — Piso 3 dormitorios Tipo B",
                             listing_type="Venta", property_type="Piso",
                             price=275000, address="Barrio de Los Cerros, Madrid Este", city="Madrid",
                             bedrooms=3, bathrooms=2, sqm=95,
                             description="Tipología B con mayor superficie. 2 plazas de garaje incluidas. 181 viviendas VPPB en cooperativa. Zonas comunes completas: piscina comunitaria, áreas ajardinadas y sala comunitaria.",
                             features="Garaje x2, Trastero, Piscina comunitaria, Zonas ajardinadas, Sala comunitaria",
                             active=True, created_at=now - timedelta(days=5)),

                    Property(title="Torrejón Class II — Piso 3 dormitorios",
                             listing_type="Venta", property_type="Piso",
                             price=395900, address="Barrio de Aldovea, Torrejón de Ardoz", city="Torrejón de Ardoz",
                             bedrooms=3, bathrooms=2, sqm=100,
                             description="45 exclusivas viviendas en zona privilegiada de nueva construcción en Aldovea. Diseño cuidado con espacios amplios y funcionales. Piscina con vestuarios, jardines y sala comunitaria. Colegios, supermercados y centros deportivos a pocos minutos.",
                             features="Garaje, Trastero, Piscina, Zonas ajardinadas, Sala comunitaria, Vestuarios",
                             active=True, created_at=now - timedelta(days=8)),

                    Property(title="Torrejón Class II — Bajo con patio privado",
                             listing_type="Venta", property_type="Piso",
                             price=425000, address="Barrio de Aldovea, Torrejón de Ardoz", city="Torrejón de Ardoz",
                             bedrooms=3, bathrooms=2, sqm=105,
                             description="Vivienda en planta baja con patio privado. 45 viviendas exclusivas en ubicación privilegiada. Zonas comunes completas con piscina, jardines y sala multifuncional. Entorno seguro y privado para toda la familia.",
                             features="Patio privado, Garaje, Trastero, Piscina comunitaria, Jardines",
                             active=True, created_at=now - timedelta(days=8)),

                    Property(title="Torrejón Class II — Ático con terraza",
                             listing_type="Venta", property_type="Piso",
                             price=460000, address="Barrio de Aldovea, Torrejón de Ardoz", city="Torrejón de Ardoz",
                             bedrooms=3, bathrooms=2, sqm=110,
                             description="Ático con amplias terrazas en la exclusiva promoción Torrejón Class II. Vistas despejadas, máxima luminosidad. 1-2 plazas de garaje según tipología y trastero incluido.",
                             features="Terraza amplia, Garaje, Trastero, Piscina, Vistas despejadas",
                             active=True, created_at=now - timedelta(days=8)),

                    Property(title="Entrenúcleos Class — Piso 2 dormitorios",
                             listing_type="Venta", property_type="Piso",
                             price=235900, address="Entrenúcleos, Dos Hermanas", city="Dos Hermanas (Sevilla)",
                             bedrooms=2, bathrooms=1, sqm=70,
                             description="Promoción con tipologías de 2, 3 y 4 dormitorios en la zona de Entrenúcleos. Obras iniciadas. Excelentes calidades y zonas comunes.",
                             features="Garaje, Trastero, Piscina comunitaria, Zonas ajardinadas",
                             active=True, created_at=now - timedelta(days=12)),

                    Property(title="Entrenúcleos Class — Piso 3 dormitorios",
                             listing_type="Venta", property_type="Piso",
                             price=275000, address="Entrenúcleos, Dos Hermanas", city="Dos Hermanas (Sevilla)",
                             bedrooms=3, bathrooms=2, sqm=90,
                             description="Tipología de 3 dormitorios en Entrenúcleos Class. Obras iniciadas. Distribución optimizada, acabados de calidad. Zonas comunes completas.",
                             features="Garaje, Trastero, Piscina comunitaria, Zonas ajardinadas, Sala comunitaria",
                             active=True, created_at=now - timedelta(days=12)),

                    Property(title="Ciempozuelos Horizon — Adosado 3 dormitorios",
                             listing_type="Venta", property_type="Chalet",
                             price=305900, address="Zona Sur, Ciempozuelos", city="Ciempozuelos",
                             bedrooms=3, bathrooms=2, sqm=129,
                             description="44 viviendas unifamiliares adosadas y pareadas en cooperativa. Salón-comedor con cocina integrada, 2 dormitorios en planta baja, dormitorio principal con vestidor y baño en planta superior, más estancia multidisciplinar. Amplio jardín privado. Conexión A-4 y Cercanías C3.",
                             features="Jardín privado, Garaje, Vestidor, Estancia multiusos, Cocina integrada",
                             active=True, created_at=now - timedelta(days=10)),

                    Property(title="Ciempozuelos Horizon — Pareado 3 dormitorios",
                             listing_type="Venta", property_type="Chalet",
                             price=335000, address="Zona Sur, Ciempozuelos", city="Ciempozuelos",
                             bedrooms=3, bathrooms=2, sqm=140,
                             description="Vivienda pareada con mayor superficie y jardín. Planta baja con salón-comedor y cocina integrada, 2 dormitorios y baño completo. Planta superior con suite principal y estancia multidisciplinar. Hospital Infanta Cristina a 15 min.",
                             features="Jardín privado amplio, Garaje, Vestidor, Suite principal, Cocina integrada",
                             active=True, created_at=now - timedelta(days=10)),

                    Property(title="Boadilla Infinity — Chalet independiente 4 dormitorios",
                             listing_type="Venta", property_type="Chalet",
                             price=1225000, address="Boadilla del Monte", city="Boadilla del Monte",
                             bedrooms=4, bathrooms=3, sqm=280,
                             description="Chalets exclusivos e independientes en Boadilla del Monte. Máxima calidad de construcción, diseño contemporáneo y amplias parcelas. Urbanización premium con las mejores zonas comunes.",
                             features="Jardín privado, Piscina, Garaje, Parcela amplia, Calidades premium",
                             active=True, created_at=now - timedelta(days=15)),

                    Property(title="Boadilla Infinity II — Chalet independiente 5 dormitorios",
                             listing_type="Venta", property_type="Chalet",
                             price=1195000, address="Boadilla del Monte", city="Boadilla del Monte",
                             bedrooms=5, bathrooms=4, sqm=320,
                             description="Segunda fase de Boadilla Infinity con chalets de 5 dormitorios. Diseño exclusivo, materiales de primera calidad. Parcelas generosas con jardín y posibilidad de piscina privada.",
                             features="Jardín privado, Parcela amplia, Garaje doble, 5 dormitorios, Calidades premium",
                             active=True, created_at=now - timedelta(days=15)),

                    Property(title="Cadmia Residencial II — Piso 2 dormitorios",
                             listing_type="Venta", property_type="Piso",
                             price=545000, address="Cadmia Residencial", city="Madrid",
                             bedrooms=2, bathrooms=2, sqm=85,
                             description="Promoción residencial con tipologías de 2, 3 y 4 dormitorios. Ubicación exclusiva con excelentes acabados y zonas comunes de primer nivel.",
                             features="Garaje, Trastero, Piscina, Gimnasio, Zonas ajardinadas",
                             active=True, created_at=now - timedelta(days=20)),

                    Property(title="Cadmia Residencial II — Piso 3 dormitorios",
                             listing_type="Venta", property_type="Piso",
                             price=620000, address="Cadmia Residencial", city="Madrid",
                             bedrooms=3, bathrooms=2, sqm=110,
                             description="Vivienda de 3 dormitorios en Cadmia Residencial II. Promoción exclusiva con calidades superiores, zonas comunes completas y garaje incluido.",
                             features="Garaje, Trastero, Piscina, Gimnasio, Zonas ajardinadas, Sala comunitaria",
                             active=True, created_at=now - timedelta(days=20)),

                    Property(title="Ahijones Horizon II — Piso 2 dormitorios (últimas unidades)",
                             listing_type="Venta", property_type="Piso",
                             price=263800, address="Barrio de Ahijones, Madrid Este", city="Madrid",
                             bedrooms=2, bathrooms=1, sqm=65,
                             description="Últimas viviendas disponibles en Ahijones Horizon II. Tipologías de 2 y 3 dormitorios en los nuevos desarrollos del este de Madrid. Garaje y trastero incluidos. ¡No te quedes sin la tuya!",
                             features="Garaje, Trastero, Piscina comunitaria, Zonas ajardinadas, Últimas unidades",
                             active=True, created_at=now - timedelta(days=25)),

                    # ── PROMOCIONES COMPLETADAS (para mostrar historial) ──
                    Property(title="Torrejón Class I (ENTREGADA)",
                             listing_type="Venta", property_type="Piso",
                             price=365000, address="Torrejón de Ardoz", city="Torrejón de Ardoz",
                             bedrooms=3, bathrooms=2, sqm=95,
                             description="Primera fase entregada con éxito. Todas las viviendas vendidas y entregadas a sus propietarios.",
                             active=False, created_at=now - timedelta(days=180)),

                    Property(title="Ahijones Horizon I (ENTREGADA)",
                             listing_type="Venta", property_type="Piso",
                             price=224300, address="Barrio de Ahijones, Madrid Este", city="Madrid",
                             bedrooms=2, bathrooms=1, sqm=60,
                             description="Promoción entregada. Viviendas adaptadas de 2 dormitorios. Todas vendidas.",
                             active=False, created_at=now - timedelta(days=240)),
                ]
                db.session.add_all(props)
                db.session.flush()

                # ── Rich client data (interesados en obra nueva) ──────────────
                clients = [
                    Client(name="María García López", phone="+34 611 222 333", email="maria.garcia@gmail.com",
                           source="WhatsApp", notes="Interesada en Los Cerros Horizon. Pareja joven, primer hijo en camino. Busca 3 dormitorios con garaje. Presupuesto hasta 280.000€. Ha pedido cita para piso piloto.",
                           created_at=now - timedelta(days=2)),

                    Client(name="Carlos Ruiz Martín", phone="+34 622 333 444", email="carlos.ruiz@outlook.com",
                           source="WhatsApp", notes="Interesado en Torrejón Class II. Familia con 2 hijos. Quiere bajo con patio o ático. Trabaja en zona aeropuerto. Presupuesto 400-460k.",
                           created_at=now - timedelta(days=5)),

                    Client(name="Ana Fernández Soto", phone="+34 633 444 555", email="ana.fernandez@email.com",
                           source="Referido", notes="Interesada en Ciempozuelos Horizon. Familia con 2 hijos (8 y 12 años). Les encanta la idea del jardín privado y la zona tranquila. Colegio Eloy Saavedra cerca.",
                           created_at=now - timedelta(days=10)),

                    Client(name="Pedro Jiménez Vega", phone="+34 644 555 666", email="pedro.jimenez@empresa.com",
                           source="Portal", notes="Inversor profesional. Interesado en Cadmia Residencial II y locales de Torrejón Singular. Busca rentabilidad a largo plazo. Tiene capital para 2-3 operaciones.",
                           created_at=now - timedelta(days=7)),

                    Client(name="Laura Martínez Díaz", phone="+34 655 666 777", email="laura.martinez@gmail.com",
                           source="WhatsApp", notes="Primera vivienda. Muy interesada en Ahijones Horizon II por precio. Tiene aprobación hipotecaria de CaixaBank. Quiere 2 hab con garaje. Urgente: últimas unidades.",
                           created_at=now - timedelta(days=1)),

                    Client(name="Roberto y Elena Sánchez", phone="+34 666 777 888", email="r.sanchez@gmail.com",
                           source="Web", notes="Interesados en Boadilla Infinity. Buscan chalet independiente de lujo. Venden su piso actual en Chamberí para financiar. Presupuesto alto sin problema.",
                           created_at=now - timedelta(days=8)),

                    Client(name="Sofía Moreno Ruiz", phone="+34 677 888 999", email="sofia.moreno@hotmail.com",
                           source="WhatsApp", notes="Interesada en Entrenúcleos Class. Es de Sevilla, busca piso de 3 hab cerca del trabajo en Dos Hermanas. Obras iniciadas le da confianza.",
                           created_at=now - timedelta(days=4)),

                    Client(name="Javier López Navarro", phone="+34 688 999 000", email="javier.lopez@email.es",
                           source="Referido", notes="Referido por Carlos Ruiz. También interesado en Torrejón Class II. Soltero, busca piso de 3 hab como inversión a largo plazo.",
                           created_at=now - timedelta(days=3)),

                    Client(name="Patricia González Ruiz", phone="+34 699 000 111", email="patricia.glez@gmail.com",
                           source="WhatsApp", notes="Interesada en Los Cerros Horizon. Cooperativa le parece buena opción. Pregunta mucho sobre zonas comunes y conexiones de transporte.",
                           created_at=now - timedelta(days=6)),

                    Client(name="Miguel Ángel Torres", phone="+34 600 111 222", email="ma.torres@empresa.com",
                           source="Web", notes="Interesado en Boadilla Infinity II. Presupuesto alto. Quiere chalet de 5 dormitorios. Familia numerosa con 4 hijos. Valor personalización muy importante.",
                           created_at=now - timedelta(days=1)),
                ]
                db.session.add_all(clients)
                db.session.flush()

                # ── Rich appointment data (visitas pisos piloto) ──────────────
                appointments = [
                    # Upcoming
                    Appointment(client_id=clients[0].id, property_id=props[0].id,
                                date=now + timedelta(hours=3), duration=30, status="confirmed",
                                notes="Visita piso piloto Los Cerros Horizon. María viene con su pareja. Muy interesados en la tipología A."),
                    Appointment(client_id=clients[1].id, property_id=props[3].id,
                                date=now + timedelta(days=1, hours=10), duration=30, status="confirmed",
                                notes="Visita piso piloto Torrejón Class II. Carlos quiere ver el bajo con patio. Viene con su mujer y los niños."),
                    Appointment(client_id=clients[2].id, property_id=props[7].id,
                                date=now + timedelta(days=1, hours=17), duration=45, status="pending",
                                notes="Visita promoción Ciempozuelos Horizon. Ana quiere ver los adosados y el entorno. Le interesa cercanía al colegio Eloy Saavedra."),
                    Appointment(client_id=clients[4].id, property_id=props[13].id,
                                date=now + timedelta(days=2, hours=11), duration=30, status="pending",
                                notes="Laura quiere ver Ahijones Horizon II. Últimas unidades disponibles. Tiene aprobación hipotecaria."),
                    Appointment(client_id=clients[5].id, property_id=props[9].id,
                                date=now + timedelta(days=3, hours=12), duration=60, status="pending",
                                notes="Roberto y Elena visitan Boadilla Infinity. Alto presupuesto. Quieren ver parcelas y calidades."),
                    Appointment(client_id=clients[9].id, property_id=props[10].id,
                                date=now + timedelta(days=2, hours=9), duration=60, status="confirmed",
                                notes="Miguel Ángel visita Boadilla Infinity II. Familia numerosa. Interesado en personalización."),

                    # Past - completed
                    Appointment(client_id=clients[0].id, property_id=props[1].id,
                                date=now - timedelta(days=2, hours=-10), duration=30, status="completed",
                                notes="Visitó la tipología B de Los Cerros. Le gustó más espacio pero prefiere precio tipología A."),
                    Appointment(client_id=clients[6].id, property_id=props[5].id,
                                date=now - timedelta(days=1, hours=-11), duration=30, status="completed",
                                notes="Sofía visitó Entrenúcleos Class. Le encantó la zona. Pidió planos de 3 dormitorios."),
                    Appointment(client_id=clients[3].id, property_id=props[11].id,
                                date=now - timedelta(days=3, hours=-16), duration=45, status="completed",
                                notes="Pedro visitó Cadmia Residencial II. Muy interesado como inversión. Pidió estudio de rentabilidad."),

                    # Cancelled
                    Appointment(client_id=clients[8].id, property_id=props[0].id,
                                date=now - timedelta(days=1, hours=-14), duration=30, status="cancelled",
                                notes="Patricia canceló por agenda. Reprogramar para la semana que viene. Sigue interesada en Los Cerros."),
                ]
                db.session.add_all(appointments)

                # ── Rich conversation data (simulating WhatsApp chatbot) ──
                convos = [
                    # Conversación 1: María García - Los Cerros Horizon
                    Conversation(user_id="wa_611222333", role="user",
                                 content="Hola, buenas tardes. He visto la promoción Los Cerros Horizon y me interesa mucho. ¿Qué tipologías tenéis disponibles? Somos una pareja joven y esperamos nuestro primer hijo.",
                                 created_at=now - timedelta(hours=48)),
                    Conversation(user_id="wa_611222333", role="assistant",
                                 content="¡Buenas tardes, María! Enhorabuena por la buena noticia 🎉 Los Cerros Horizon es una promoción perfecta para familias jóvenes.\n\nTenemos 181 viviendas VPPB de 3 dormitorios en cooperativa:\n\n🏠 **Tipología A** — desde 250.500€+IVA\n🛏 3 hab · 2 baños · ~85m²\n🚗 1 plaza de garaje + trastero\n\n🏠 **Tipología B** — desde 275.000€+IVA\n🛏 3 hab · 2 baños · ~95m²\n🚗 2 plazas de garaje + trastero\n\nAmbas incluyen plaza de bicicletas y acceso a zonas comunes: piscina, jardines y sala comunitaria.\n\n¿Te gustaría visitar nuestro piso piloto?",
                                 created_at=now - timedelta(hours=48, minutes=-2)),
                    Conversation(user_id="wa_611222333", role="user",
                                 content="¡Genial! El precio de la tipología A nos encaja perfecto. ¿Cómo funciona lo de la cooperativa? ¿Y podríamos ver el piso piloto esta semana?",
                                 created_at=now - timedelta(hours=47)),
                    Conversation(user_id="wa_611222333", role="assistant",
                                 content="¡La cooperativa es una ventaja! Os permite adquirir la vivienda a precio de coste, sin el margen de un promotor tradicional.\n\n📋 **Cómo funciona:**\n1. Os hacéis cooperativistas con una aportación inicial\n2. Se pagan cuotas durante la construcción\n3. Al finalizar, la vivienda es vuestra\n4. Asentis gestiona todo el proceso como gestor profesional\n\n📅 **Cita para piso piloto:**\nHe reservado para vosotros:\n- 📍 Piso piloto Los Cerros Horizon\n- 🗓 Mañana a las 10:00h\n- ⏱ 30 minutos\n- 📞 Confirmar en 91 112 49 23\n\n¿Os viene bien?",
                                 created_at=now - timedelta(hours=47, minutes=-1)),
                    Conversation(user_id="wa_611222333", role="user",
                                 content="Perfecto a las 10 mañana. ¿Qué zona del barrio es exactamente? ¿Hay buenas conexiones?",
                                 created_at=now - timedelta(hours=46)),
                    Conversation(user_id="wa_611222333", role="assistant",
                                 content="¡Confirmado! Os espero mañana.\n\nSobre la ubicación:\n\n📍 **Barrio de Los Cerros** — Nuevos desarrollos del este de Madrid\n- Ámbito urbanístico de +4,7 millones de m²\n- Mayor proporción de zonas verdes de su planeamiento\n- Excelentes conexiones con Madrid centro\n- Todos los servicios: colegios, comercios, transporte\n\n🚇 La zona contará con infraestructuras de transporte público en desarrollo\n🌳 Ideal para familias por la cantidad de zonas verdes\n\nMañana en la visita os daremos toda la documentación con planos y memoria de calidades. ¡Hasta mañana!",
                                 created_at=now - timedelta(hours=46, minutes=-1)),

                    # Conversación 2: Carlos Ruiz - Torrejón Class II
                    Conversation(user_id="wa_622333444", role="user",
                                 content="Buenos días. Estoy interesado en Torrejón Class II. Tengo una familia con 2 hijos y busco algo con espacio exterior. ¿Tenéis bajos con patio?",
                                 created_at=now - timedelta(hours=24)),
                    Conversation(user_id="wa_622333444", role="assistant",
                                 content="¡Buenos días Carlos! Torrejón Class II tiene exactamente lo que buscas:\n\n🏠 **Bajo con patio privado** — desde 425.000€+IVA\n🛏 3 dormitorios · 2 baños · ~105m²\n🌿 Patio privado\n🚗 1-2 plazas garaje + trastero\n\nTambién tenemos:\n🏠 **Ático con terraza** — desde 460.000€+IVA\nCon amplias terrazas y vistas despejadas\n\n📍 Ubicación en Aldovea, Torrejón de Ardoz:\n- Zona nueva de alta calidad\n- Colegios e institutos a minutos\n- Centro deportivo y supermercados cerca\n- Piscina con vestuarios en la urbanización\n\n¿Quieres reservar cita para ver el piso piloto?",
                                 created_at=now - timedelta(hours=24, minutes=-2)),
                    Conversation(user_id="wa_622333444", role="user",
                                 content="El bajo con patio me interesa mucho. ¿Se puede personalizar para los niños? Como elegir materiales o distribución.",
                                 created_at=now - timedelta(hours=23)),
                    Conversation(user_id="wa_622333444", role="assistant",
                                 content="¡Por supuesto! Asentis ofrece un servicio de **personalización** muy completo:\n\n✨ **Opciones de personalización:**\n- Elección de acabados (suelos, azulejos, encimeras)\n- Modificaciones de distribución\n- Opciones de cocina y baños\n- Domótica e instalaciones extra\n\nNuestros interioristas os asesoran para adaptar la vivienda a vuestras necesidades.\n\n📅 **Te propongo:**\n1. Primero, visita al piso piloto en Torrejón\n2. Después, reunión con el equipo de personalización\n\n¿Te viene bien el viernes a las 11:00 para ver el piso piloto? Está con cita previa en el 91 112 49 23.",
                                 created_at=now - timedelta(hours=23, minutes=-1)),

                    # Conversación 3: Pedro Jiménez - Inversión
                    Conversation(user_id="wa_644555666", role="user",
                                 content="Buenas, soy inversor y me interesa Cadmia Residencial II. ¿Qué rentabilidad puedo esperar? También me interesan los locales de Torrejón Singular.",
                                 created_at=now - timedelta(hours=36)),
                    Conversation(user_id="wa_644555666", role="assistant",
                                 content="Buenos días Pedro. Tenemos dos opciones interesantes para inversión:\n\n🏢 **Cadmia Residencial II** — desde 545.000€+IVA\n📐 2-4 dormitorios disponibles\n📊 Zona con alta demanda de alquiler\n✨ Calidades premium, zonas comunes completas\n\n🏪 **Torrejón Singular — Locales comerciales**\n📐 2 locales disponibles desde 225.000€+IVA\n📍 Zona comercial consolidada\n\n📊 **Análisis de rentabilidad:**\n- Cadmia: zona con alquileres de 1.200-1.800€/mes → rent. ~3,5-4%\n- Locales Torrejón: potencial de alquiler comercial con rentabilidades superiores\n\n¿Quieres que preparemos un informe detallado de inversión?",
                                 created_at=now - timedelta(hours=36, minutes=-2)),

                    # Conversación 4: Laura Martínez - Primera vivienda Ahijones
                    Conversation(user_id="wa_655666777", role="user",
                                 content="Hola! He visto que quedan las últimas unidades en Ahijones Horizon II. Tengo aprobación hipotecaria de CaixaBank por 280.000€. ¿Puedo llegar?",
                                 created_at=now - timedelta(hours=6)),
                    Conversation(user_id="wa_655666777", role="assistant",
                                 content="¡Hola Laura! Sí, estás a tiempo pero date prisa porque quedan las **últimas viviendas disponibles** 🏃‍♀️\n\n🏠 **Ahijones Horizon II** — desde 263.800€+IVA\n🛏 2 dormitorios · 1 baño · ~65m²\n🚗 Garaje + trastero incluidos\n🏊 Piscina comunitaria + jardines\n\n💰 Con tu aprobación de 280.000€ de CaixaBank, ¡encaja perfectamente!\n\nEl precio es desde 263.800€+IVA, así que con IVA (10% al ser obra nueva) estarías en ~290.200€.\n\n⚠️ **Importante:** También hay tipología de 3 dormitorios disponible, pero a precio ligeramente superior.\n\n¿Quieres que veamos las unidades que quedan? Puedo agendarte una visita urgente.",
                                 created_at=now - timedelta(hours=6, minutes=-2)),
                    Conversation(user_id="wa_655666777", role="user",
                                 content="¡Sí por favor! ¿Qué día puedo ir? Y una duda, al ser obra nueva el IVA es el 10% no? No hay ITP?",
                                 created_at=now - timedelta(hours=5)),
                    Conversation(user_id="wa_655666777", role="assistant",
                                 content="¡Exacto! Al ser **obra nueva** se aplica IVA al 10%, no ITP. Es una ventaja porque es un tipo fijo y conocido.\n\n📋 **Costes de compra obra nueva:**\n- IVA: 10% sobre el precio\n- AJD (Actos Jurídicos): 0,75% en Madrid\n- Notaría + Registro: ~2.000-3.000€\n\n📅 **Visita urgente programada:**\n- 📍 Ahijones Horizon II, Madrid Este\n- 🗓 Pasado mañana (primer hueco disponible)\n- ⏱ 30 minutos\n- 📞 Confirma llamando al 91 112 49 23\n\n⚡ Te recomiendo no esperar mucho — las últimas unidades en Ahijones siempre vuelan. ¿Confirmo la cita?",
                                 created_at=now - timedelta(hours=5, minutes=-1)),

                    # Conversación 5: Roberto y Elena - Boadilla Infinity
                    Conversation(user_id="wa_666777888", role="user",
                                 content="Hola, estamos interesados en un chalet en Boadilla Infinity. Actualmente vivimos en un piso en Chamberí pero necesitamos más espacio. ¿Qué opciones hay?",
                                 created_at=now - timedelta(hours=12)),
                    Conversation(user_id="wa_666777888", role="assistant",
                                 content="¡Hola Roberto! Boadilla Infinity es nuestra promoción más exclusiva:\n\n🏡 **Boadilla Infinity** — desde 1.225.000€+IVA\n🛏 4 dormitorios · 3 baños · ~280m²\n🌳 Chalets independientes con parcela amplia\n🏊 Posibilidad de piscina privada\n🚗 Garaje\n✨ Calidades premium\n\n🏡 **Boadilla Infinity II** — desde 1.195.000€+IVA\n🛏 5 dormitorios · 4 baños · ~320m²\nIncluso más espacio para familias grandes\n\n📍 Boadilla del Monte:\n- Municipio con la mayor renta per cápita de España\n- Entorno natural excepcional\n- Excelentes colegios internacionales\n- A 20 min de Madrid centro\n\n¿Vendéis vuestro piso de Chamberí? Podemos asesoraros también en eso.",
                                 created_at=now - timedelta(hours=12, minutes=-2)),

                    # Conversación 6: Consultas generales
                    Conversation(user_id="wa_677888999", role="user",
                                 content="Hola, ¿cuál es el horario de atención de Asentis? ¿Y dónde están las oficinas?",
                                 created_at=now - timedelta(hours=8)),
                    Conversation(user_id="wa_677888999", role="assistant",
                                 content="¡Hola! Aquí tienes toda la información:\n\n🕐 **Horario de atención comercial:**\n• Lunes a Jueves: 10:00 - 14:00 y 16:00 - 19:00\n• Viernes: 10:00 - 14:00\n\n📍 **Sede central:**\nAvda. Europa 26, Edificio Ática 5, 3ª Planta\n28224 Pozuelo de Alarcón, Madrid\n\n📞 **Teléfonos:**\n• Oficinas centrales: 91 714 04 35\n• Cita pisos piloto: 91 112 49 23\n\n📧 **Email:**\n• info@asentis.es\n• recepcion@asentis.es\n\n🏠 **¿Quieres visitar un piso piloto?**\nPuedes reservar tu cita online en nuestra web o llamándonos.\n\n¿En qué promoción estás interesada?",
                                 created_at=now - timedelta(hours=8, minutes=-1)),
                ]
                db.session.add_all(convos)
                db.session.commit()
                print("[DEMO] Mock data created: 16 properties, 10 clients, 10 appointments, 20 messages")

        except Exception as e:
            print(f"[WARNING] Database init skipped: {e}")

    @app.before_request
    def before_request():
        from routes.auth import _load_current_user
        _load_current_user()

    @app.context_processor
    def inject_user():
        return {"current_user": g.get("user")}

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.properties import properties_bp
    from routes.appointments import appointments_bp
    from routes.clients import clients_bp
    from routes.conversations import conversations_bp
    from routes.stats import stats_bp
    from routes.agent import agent_bp
    from routes.settings import settings_bp
    from routes.users import users_bp
    from routes.activity import activity_bp
    from routes.api import api_bp
    from routes.whatsapp_demo import whatsapp_demo_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(conversations_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(whatsapp_demo_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5002)
