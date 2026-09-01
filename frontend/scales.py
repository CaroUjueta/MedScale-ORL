SCALES = [
    {
        "id": "ess",
        "nombre": "Epworth (ESS)",
        "area": "apnea",
        "desc": "Somnolencia diurna y riesgo de apnea",
        "chips": ["ESS"],
    },
    {
        "id": "stop_bang",
        "nombre": "STOP-BANG",
        "area": "apnea",
        "desc": "Tamizaje de apnea obstructiva del sueno",
        "chips": ["STOP-BANG"],
    },
    {
        "id": "imc",
        "nombre": "IMC",
        "area": "apnea",
        "desc": "Indice de masa corporal",
        "chips": ["IMC"],
    },
    {
        "id": "snot22",
        "nombre": "SNOT-22",
        "area": "rinosinusitis",
        "desc": "Sintomas y calidad de vida nasal",
        "chips": ["SNOT-22"],
    },
    {
        "id": "lund_mackay",
        "nombre": "Lund Mackay",
        "area": "rinosinusitis",
        "desc": "Extension radiologica de la sinusitis",
        "chips": ["Lund-Mackay"],
    },
    {
        "id": "thi",
        "nombre": "THI",
        "area": "otologia",
        "desc": "Impacto del acufeno en la vida diaria",
        "chips": ["THI"],
    },
    {
        "id": "etdq7",
        "nombre": "ETDQ-7",
        "area": "otologia",
        "desc": "Disfuncion de la trompa de Eustaquio",
        "chips": ["ETDQ-7"],
    },
    {
        "id": "vhi10",
        "nombre": "VHI-10",
        "area": "disfonia",
        "desc": "Impacto de la disfonia en la vida diaria",
        "chips": ["VHI-10"],
    },
    {
        "id": "grbas",
        "nombre": "GRBAS",
        "area": "disfonia",
        "desc": "Evaluacion perceptiva de la voz",
        "chips": ["GRBAS"],
    },
]

AREAS = {
    "apnea": {
        "titulo": "Apnea del Sueno",
        "desc": "Evaluacion y tamizaje",
    },
    "rinosinusitis": {
        "titulo": "Rinosinusitis",
        "desc": "Sintomas y evaluacion",
    },
    "otologia": {
        "titulo": "Otologia",
        "desc": "Audicion y funcion del oido",
    },
    "disfonia": {
        "titulo": "Disfonia",
        "desc": "Evaluacion de la voz",
    },
}

AREA_ORDEN = ["apnea", "rinosinusitis", "otologia", "disfonia"]


def escala_por_id(escala_id):
    for s in SCALES:
        if s["id"] == escala_id:
            return s
    return None


def escala_id_por_nombre(nombre):
    n = (nombre or "").strip().lower()
    for s in SCALES:
        if s["id"] == n or s["nombre"].strip().lower() == n:
            return s["id"]
    return None