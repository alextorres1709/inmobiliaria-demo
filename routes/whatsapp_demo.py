from flask import Blueprint, render_template
from routes.auth import login_required

whatsapp_demo_bp = Blueprint("whatsapp_demo", __name__)

# Demo conversations showing WhatsApp chatbot capabilities for Asentis
WHATSAPP_DEMOS = [
    {
        "title": "Búsqueda de vivienda — Los Cerros Horizon",
        "description": "Pareja joven busca su primera vivienda en obra nueva. El bot presenta la promoción Los Cerros Horizon y gestiona cita al piso piloto.",
        "icon": "search",
        "messages": [
            {"role": "user", "name": "María", "time": "10:30", "content": "Hola! Busco un piso de 3 habitaciones de obra nueva en Madrid. Presupuesto máximo 280.000€. ¿Qué promociones tenéis?"},
            {"role": "bot", "time": "10:30", "content": "¡Hola María! 👋 Tenemos la promoción perfecta para ti:\n\n🏠 **Los Cerros Horizon** — Madrid Este\n📐 181 viviendas VPPB en cooperativa\n🛏 3 dormitorios · 2 baños\n\n💰 **Tipología A:** desde 250.500€+IVA (~85m²)\n  · 1 garaje + trastero + plaza bici\n\n💰 **Tipología B:** desde 275.000€+IVA (~95m²)\n  · 2 garajes + trastero + plaza bici\n\n🏊 Zonas comunes: piscina, jardines, sala comunitaria\n🌳 Barrio con +4,7M m² y máxima proporción de zonas verdes\n\n¿Te gustaría visitar nuestro piso piloto?"},
            {"role": "user", "name": "María", "time": "10:32", "content": "La tipología A me encaja! ¿Cómo funciona lo de la cooperativa?"},
            {"role": "bot", "time": "10:32", "content": "¡La cooperativa es una ventaja! Compras a precio de coste:\n\n📋 **Cómo funciona:**\n1. Aportación inicial como cooperativista\n2. Cuotas durante la construcción\n3. Al finalizar, la vivienda es tuya\n4. Asentis gestiona todo como promotor profesional\n\n📅 **Cita piso piloto reservada:**\n📍 Piso piloto Los Cerros Horizon\n🗓 Mañana a las 10:00h\n📞 Confirma en 91 112 49 23\n\n¿Necesitas información sobre financiación?"},
            {"role": "user", "name": "María", "time": "10:33", "content": "Sí, ¿qué opciones de hipoteca hay para obra nueva?"},
            {"role": "bot", "time": "10:33", "content": "Al ser **obra nueva**, se aplica IVA del 10% (no ITP). Para la Tipología A:\n\n📊 **Coste estimado total:**\n• Precio: 250.500€ + IVA (10%) = ~275.550€\n• AJD (0,75%): ~2.066€\n• Notaría + Registro: ~2.500€\n\n🏦 **Hipoteca al 80%:**\n• Importe: ~220.440€\n• Variable (Euríbor+0,75%): ~850€/mes\n• Fijo (2,8%): ~990€/mes\n\nPodemos asesorarte con nuestros colaboradores bancarios. ¿Te lo preparo para después de la visita? 📋"},
        ]
    },
    {
        "title": "Familia con niños — Torrejón Class II",
        "description": "Familia con hijos busca vivienda con espacio exterior. El bot presenta opciones de bajos con patio y áticos en Torrejón Class II.",
        "icon": "home",
        "messages": [
            {"role": "user", "name": "Carlos", "time": "09:00", "content": "Buenos días. Tenemos 2 hijos y buscamos algo con espacio exterior en Torrejón de Ardoz. ¿Tenéis bajos con patio?"},
            {"role": "bot", "time": "09:00", "content": "¡Buenos días Carlos! Torrejón Class II es perfecto para familias:\n\n🏠 **Bajo con patio privado** — desde 425.000€+IVA\n🛏 3 hab · 2 baños · ~105m²\n🌿 Patio privado para los niños\n🚗 1-2 garajes + trastero\n\n🏠 **Ático con terraza** — desde 460.000€+IVA\n🛏 3 hab · 2 baños · ~110m²\n☀️ Amplias terrazas, vistas despejadas\n\n📍 Barrio de Aldovea:\n• Colegios e institutos a minutos\n• Supermercados y centro deportivo\n• Zona nueva y tranquila\n\n🏊 Zonas comunes: piscina, vestuarios, jardines, sala multiusos\n\n¿Reservamos cita para ver el piso piloto?"},
            {"role": "user", "name": "Carlos", "time": "09:02", "content": "El bajo con patio nos encanta. ¿Se puede personalizar la vivienda?"},
            {"role": "bot", "time": "09:02", "content": "¡Sí! Asentis ofrece un servicio de **personalización** muy completo:\n\n✨ **Qué puedes elegir:**\n• Acabados: suelos, azulejos, encimeras\n• Distribución interior\n• Cocina y baños a medida\n• Domótica e instalaciones extra\n\n👩‍🎨 Nuestros interioristas os asesoran para adaptarlo a vuestra familia.\n\n📅 **Te propongo:**\n1. Visita al piso piloto en Torrejón\n2. Reunión con el equipo de personalización\n\n📞 Reserva cita: 91 112 49 23\n📍 Piso piloto Torrejón Class II\n\nEl bajo con patio + garaje + personalización es la combinación ideal para familias 👨‍👩‍👧‍👦"},
        ]
    },
    {
        "title": "Inversor profesional — Cadmia y locales",
        "description": "Inversor busca oportunidades en promociones de Asentis. El bot proporciona análisis de inversión y rentabilidades.",
        "icon": "chart",
        "messages": [
            {"role": "user", "name": "Pedro", "time": "09:15", "content": "Buenos días. Busco invertir en vivienda nueva. ¿Qué opciones tiene Asentis con buena rentabilidad?"},
            {"role": "bot", "time": "09:15", "content": "Buenos días Pedro. Tenemos varias opciones de inversión:\n\n🏢 **Cadmia Residencial II** — desde 545.000€+IVA\n📐 2-4 dormitorios\n📊 Zona con alta demanda de alquiler\n💰 Alquileres zona: 1.200-1.800€/mes → rent. ~3,5-4%\n\n🏪 **Torrejón Singular — Locales comerciales**\n📐 2 locales desde 225.000€+IVA\n📍 Zona comercial consolidada\n📊 Rentabilidad comercial superior\n\n🏠 **Ahijones Horizon II** — desde 263.800€+IVA\n📐 2-3 hab, últimas unidades\n💰 Zona en auge, alta revalorización\n\n📋 ¿Quieres un informe comparativo de inversión con proyecciones?"},
            {"role": "user", "name": "Pedro", "time": "09:17", "content": "Los locales de Torrejón me interesan. ¿Qué rentabilidad tienen?"},
            {"role": "bot", "time": "09:17", "content": "Los locales de **Torrejón Singular** son una oportunidad sólida:\n\n🏪 **2 locales comerciales** — desde 225.000€+IVA\n📐 Superficies variadas\n📍 Zona comercial de Torrejón de Ardoz\n\n📊 **Análisis inversión:**\n• Precio entrada: ~250.000€ (con IVA)\n• Alquiler comercial zona: 800-1.500€/mes\n• Rentabilidad bruta estimada: 5-7%\n• Crecimiento zona: +15% en últimos 3 años\n• Ocupación comercial: >95%\n\n💡 Ventaja: al ser obra nueva, mantenimiento mínimo los primeros años.\n\n📅 ¿Agendamos visita para ver los locales y la zona? Puedo prepararte un dossier financiero completo."},
        ]
    },
    {
        "title": "Primera vivienda — Ahijones Horizon II",
        "description": "Compradora primeriza aprovecha las últimas unidades en Ahijones. El bot asesora sobre IVA de obra nueva y trámites.",
        "icon": "home",
        "messages": [
            {"role": "user", "name": "Laura", "time": "18:45", "content": "Hola! Busco mi primera vivienda. He visto que quedan últimas unidades en Ahijones Horizon II. ¿Llego con 280.000€ de hipoteca aprobada?"},
            {"role": "bot", "time": "18:45", "content": "¡Hola Laura! Estás a tiempo pero **date prisa** — últimas viviendas disponibles 🏃‍♀️\n\n🏠 **Ahijones Horizon II** — desde 263.800€+IVA\n🛏 2 dormitorios · ~65m²\n🚗 Garaje + trastero incluidos\n🏊 Piscina + jardines\n\n💰 **Cálculo con tu hipoteca:**\n• Precio: 263.800€ + IVA 10% = ~290.180€\n• AJD (0,75%): ~2.176€\n• Notaría + Registro: ~2.500€\n• **Total estimado: ~294.856€**\n\n✅ Con 280.000€ de hipoteca + entrada → ¡encaja perfecto!\n\n⚠️ Al ser obra nueva: IVA 10%, no ITP\n\n¿Reservo visita urgente?"},
            {"role": "user", "name": "Laura", "time": "18:47", "content": "Sí por favor urgente! ¿Hay de 3 dormitorios también?"},
            {"role": "bot", "time": "18:47", "content": "¡Agendamos ya! También hay tipología de 3 dormitorios a precio ligeramente superior.\n\n📅 **Visita programada:**\n📍 Ahijones Horizon II, Madrid Este\n🗓 Pasado mañana — primer hueco disponible\n📞 Confirma en 91 112 49 23\n\n📋 **Trae a la visita:**\n• DNI\n• Pre-aprobación de CaixaBank\n• Cualquier duda\n\n⚡ Te recomiendo decidir rápido — en la fase anterior (Ahijones Horizon I) se vendieron todas.\n\n✅ Te registro con alertas automáticas por si entran nuevas unidades.\n\n¿Necesitas algo más?"},
        ]
    },
    {
        "title": "Consultas generales y horarios",
        "description": "El bot responde preguntas frecuentes sobre horarios, oficinas, pisos piloto y servicios de Asentis.",
        "icon": "info",
        "messages": [
            {"role": "user", "name": "Elena", "time": "20:10", "content": "Hola, ¿cuál es el horario de Asentis? ¿Y dónde están las oficinas?"},
            {"role": "bot", "time": "20:10", "content": "¡Hola Elena!\n\n🕐 **Horario de atención comercial:**\n• Lunes a Jueves: 10:00 - 14:00 y 16:00 - 19:00\n• Viernes: 10:00 - 14:00\n\n📍 **Sede central:**\nAvda. Europa 26, Edif. Ática 5, 3ª Planta\n28224 Pozuelo de Alarcón, Madrid\n\n📞 **Teléfonos:**\n• Oficinas: 91 714 04 35\n• Pisos piloto (cita previa): 91 112 49 23\n\n📧 **Email:** info@asentis.es\n\n🏠 **Pisos piloto visitables:**\n• Los Cerros Horizon\n• Torrejón Class II\n• Ciempozuelos Horizon\n\n¿En qué promoción estás interesada?"},
            {"role": "user", "name": "Elena", "time": "20:12", "content": "Quiero ver las promociones que tenéis en comercialización. ¿Cuáles hay disponibles ahora?"},
            {"role": "bot", "time": "20:12", "content": "📊 **Promociones en comercialización:**\n\n🏠 **Los Cerros Horizon** — Madrid Este\n   3 hab desde 250.500€+IVA\n\n🏠 **Torrejón Class II** — Torrejón de Ardoz\n   3 hab desde 395.900€+IVA\n\n🏠 **Ciempozuelos Horizon** — Adosados\n   3 hab desde 305.900€+IVA\n\n🏡 **Boadilla Infinity** — Chalets lujo\n   4 hab desde 1.225.000€+IVA\n\n🏡 **Boadilla Infinity II** — Chalets\n   5 hab desde 1.195.000€+IVA\n\n🏢 **Cadmia Residencial II** — Madrid\n   2-4 hab desde 545.000€+IVA\n\n⚠️ **Ahijones Horizon II** — ¡Últimas unidades!\n   2-3 hab desde 263.800€+IVA\n\n📞 Reserva piso piloto: 91 112 49 23\n🌐 Más info: asentis.es"},
        ]
    },
    {
        "title": "Chalet de lujo — Boadilla Infinity",
        "description": "Familia que busca un chalet exclusivo en Boadilla del Monte. El bot presenta las dos fases y el servicio de personalización.",
        "icon": "calendar",
        "messages": [
            {"role": "user", "name": "Roberto", "time": "11:00", "content": "Hola, somos una familia de 6 y necesitamos un chalet grande. Hemos visto Boadilla Infinity. ¿Qué opciones hay?"},
            {"role": "bot", "time": "11:00", "content": "¡Hola Roberto! Para una familia numerosa, Boadilla es la elección perfecta:\n\n🏡 **Boadilla Infinity** — desde 1.225.000€+IVA\n🛏 4 dormitorios · 3 baños · ~280m²\n🌳 Chalets independientes, parcela amplia\n🏊 Piscina privada posible\n\n🏡 **Boadilla Infinity II** — desde 1.195.000€+IVA\n🛏 5 dormitorios · 4 baños · ~320m²\n¡Más espacio para familias grandes!\n\n✨ **¿Por qué Boadilla Infinity?**\n• Calidades premium de construcción\n• Personalización completa\n• Boadilla: máxima calidad de vida\n• Colegios internacionales cerca\n• A 20 min de Madrid centro\n\nPara 6 personas, la fase II con 5 dormitorios sería ideal. ¿Reservo visita?"},
            {"role": "user", "name": "Roberto", "time": "11:02", "content": "Nos interesa la fase II de 5 dormitorios. ¿Se puede personalizar todo? Nos gustaría adaptar la distribución."},
            {"role": "bot", "time": "11:02", "content": "¡La personalización es uno de nuestros puntos fuertes!\n\n✨ **Servicio de personalización Asentis:**\n• Distribución interior a medida\n• Elección completa de acabados\n• Cocina y baños personalizados\n• Domótica e instalaciones especiales\n• Nuestro equipo de interioristas os asesora\n\n📅 **Propuesta:**\n1. Visita a parcelas y entorno de Boadilla\n2. Reunión con equipo de personalización\n3. Presentación de opciones y presupuesto\n\n📍 Sede: Avda. Europa 26, Pozuelo\n📞 Reserva: 91 714 04 35\n\nCon 5 dormitorios + personalización completa tendréis un hogar diseñado 100% para vuestra familia. ¿Agendamos la primera visita? 🏡"},
        ]
    },
]


@whatsapp_demo_bp.route("/whatsapp-demo")
@login_required
def index():
    return render_template("whatsapp_demo.html", demos=WHATSAPP_DEMOS)
