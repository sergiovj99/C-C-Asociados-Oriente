"""
C&C Asociados Oriente S.A.S — Sitio web corporativo
Transporte de carga por carretera y logística de personal
"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Datos del sitio (centralizados aquí para fácil mantenimiento)
# ---------------------------------------------------------------------------

EMPRESA = {
    "nombre": "C&C Asociados Oriente S.A.S",
    "nombre_corto": "C&C",
    "tagline": "Transporte de carga por carretera y logística de personal",
    "anio_fundacion": 2017,
    "ubicacion": "Antioquia, Colombia",
}

SERVICIOS = [
    {
        "categoria": "Transporte",
        "items": [
            {
                "codigo": "01",
                "titulo": "Transporte de carga",
                "descripcion": "Movilización terrestre de materiales y productos a nivel nacional con flota propia rastreada por GPS.",
                "tags": ["Carretera", "Nacional", "GPS"],
            },
            {
                "codigo": "02",
                "titulo": "Logística de personal",
                "descripcion": "Traslado seguro de personal para operaciones en minería y proyectos en carretera, con conductores certificados.",
                "tags": ["Minería", "Carretera", "RUC"],
            },
            {
                "codigo": "03",
                "titulo": "Paqueteo de alimentos",
                "descripcion": "Distribución y entrega de alimentos con cadena de custodia y trazabilidad operativa.",
                "tags": ["Distribución", "Trazabilidad"],
            },
        ],
    },
    {
        "categoria": "Materiales",
        "items": [
            {
                "codigo": "04",
                "titulo": "Materia prima y construcción",
                "descripcion": "Suministro de material para construcción a nivel nacional: agregados, recebo y materiales pétreos.",
                "tags": ["Agregados", "Obra"],
            },
            {
                "codigo": "05",
                "titulo": "Botada de escombros",
                "descripcion": "Cargue, transporte y disposición de escombros en escombreras autorizadas conforme a normativa ambiental.",
                "tags": ["Ambiental", "Disposición"],
            },
        ],
    },
    {
        "categoria": "Obras civiles",
        "items": [
            {
                "codigo": "06",
                "titulo": "Explanaciones y obras civiles",
                "descripcion": "Adecuación de terrenos, explanaciones, construcción de vías y obras civiles a nivel nacional.",
                "tags": ["Maquinaria", "Vías"],
            },
        ],
    },
]

SECTORES = [
    {
        "nombre": "Minería",
        "descripcion": "Logística de personal y carga en frentes mineros, con protocolos de seguridad reforzados.",
        "icono": "mining",
    },
    {
        "nombre": "Construcción",
        "descripcion": "Suministro continuo de agregados y materiales para constructoras y obras de gran escala.",
        "icono": "construction",
    },
    {
        "nombre": "Vías y obras civiles",
        "descripcion": "Maquinaria y carga para adecuación de terrenos, explanaciones y construcción de vías.",
        "icono": "road",
    },
    {
        "nombre": "Alimentos",
        "descripcion": "Distribución y paqueteo de alimentos con cadena de custodia y trazabilidad.",
        "icono": "food",
    },
]

VENTAJAS = [
    {
        "titulo": "Flota con GPS",
        "descripcion": "Cada vehículo cuenta con GPS y cámara de última tecnología. Visibilidad total de la ruta.",
        "icono": "gps",
    },
    {
        "titulo": "Trabajo en equipo",
        "descripcion": "Cada cliente hace parte del equipo. Cumplimos las metas con trabajo conjunto.",
        "icono": "team",
    },
    {
        "titulo": "Certificación RUC",
        "descripcion": "Impulsamos la sostenibilidad en la cadena de valor, identificamos riesgos y reducimos sanciones.",
        "icono": "shield",
    },
    {
        "titulo": "Puntualidad",
        "descripcion": "El tiempo de nuestros clientes es prioridad. Optimizamos al máximo este recurso.",
        "icono": "clock",
    },
    {
        "titulo": "Innovación operativa",
        "descripcion": "Tecnología y métodos al servicio de la seguridad y la eficiencia en cada ruta.",
        "icono": "spark",
    },
]

POLITICAS = [
    {
        "titulo": "Seguridad y salud en el trabajo",
        "color": "naranja",
        "puntos": [
            "Talento humano competente y comprometido",
            "Prevención de lesiones y enfermedades laborales",
            "Identificación y control de peligros con apoyo del COPASST",
            "Cumplimiento de la legislación SST aplicable",
        ],
    },
    {
        "titulo": "Política ambiental",
        "color": "verde",
        "puntos": [
            "Reducción en origen y valorización máxima de residuos",
            "Control del consumo de agua y vertidos al medio acuático",
            "Sistema de Gestión Ambiental ISO 14001",
            "Colaboración con autoridades en situaciones de crisis",
        ],
    },
    {
        "titulo": "Plan estratégico de seguridad vial",
        "color": "rojo",
        "puntos": [
            "Programa y gestión de auditorías en seguridad vial",
            "Seguimiento a infracciones de tránsito",
            "Centro de control de excesos de velocidad y rutas",
            "Seguimiento de mantenimiento de vehículos",
        ],
    },
]

CERTIFICACIONES = [
    {"sigla": "CCS", "nombre": "Consejo Colombiano de Seguridad"},
    {"sigla": "RUC", "nombre": "Registro Uniforme para Contratistas"},
    {"sigla": "ISO 14001", "nombre": "Sistema de Gestión Ambiental"},
]

FLOTA = [
    {
        "nombre": "Volqueta doble troque",
        "modelo": "Foton Auman C F-2940",
        "uso": "Materiales pétreos, escombros, recebo",
        "img": "camion-foton.png",
        "capacidad": "18 m³",
    },
    {
        "nombre": "Buldócer sobre orugas",
        "modelo": "Komatsu D65WX",
        "uso": "Explanaciones, adecuación de terrenos",
        "img": "bulldozer-komatsu.png",
        "capacidad": "20 ton",
    },
]


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------

@app.context_processor
def inject_globals():
    return {
        "empresa": EMPRESA,
        "anio_actual": datetime.now().year,
        "anios_operando": datetime.now().year - EMPRESA["anio_fundacion"],
    }


@app.route("/")
def home():
    # Lista plana de servicios para el dropdown del formulario
    servicios_flat = [item for cat in SERVICIOS for item in cat["items"]]
    return render_template(
        "index.html",
        servicios=SERVICIOS,
        servicios_flat=servicios_flat,
        sectores=SECTORES,
        ventajas=VENTAJAS,
        politicas=POLITICAS,
        certificaciones=CERTIFICACIONES,
        flota=FLOTA,
    )


@app.route("/api/cotizar", methods=["POST"])
def cotizar():
    """Recibe una solicitud de cotización desde el formulario del sitio."""
    data = request.get_json(silent=True) or request.form.to_dict()

    requeridos = ["nombre", "empresa", "contacto", "servicio"]
    faltan = [c for c in requeridos if not data.get(c)]
    if faltan:
        return jsonify({
            "ok": False,
            "error": f"Faltan campos: {', '.join(faltan)}"
        }), 400

    # Aquí se integraría el envío real (correo, CRM, base de datos).
    # Por ahora se devuelve una confirmación.
    return jsonify({
        "ok": True,
        "mensaje": "Solicitud recibida. Nos comunicamos en menos de 24 horas.",
        "radicado": f"CC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
