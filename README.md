# MedScale-ORL

Calculadora de escalas clínicas para **otorrinolaringología**. App móvil standalone (sin backend) construida con Kivy, compilable a Android/iOS via Buildozer.

**Autores:** Carolina Ujueta & Francys Ujueta — 2026

## Escalas disponibles

### Apnea Obstructiva del Sueño

| Escala | Descripción | Rango | Preguntas |
|--------|-------------|-------|-----------|
| **ESS** (Epworth Sleepiness Scale) | Mide la probabilidad de quedarse dormido en 8 situaciones cotidianas | 0–24 | 8 (cada una con 4 opciones: 0–3 puntos) |
| **STOP-BANG** | Cuestionario de screening de apnea del sueño (8 ítems S-T-O-P-B-A-N-G) | 0–8 | 8 (Sí/No: 0 o 1 punto) |
| **IMC** (Índice de Masa Corporal) | Calcula peso / estatura² | — | 2 (peso en kg, estatura en cm) |

### Rinosinusitis

| Escala | Descripción | Rango | Preguntas |
|--------|-------------|-------|-----------|
| **SNOT-22** (Sino-Nasal Outcome Test) | Evaluación de calidad de vida en rinosinusitis crónica | 0–110 | 22 (cada una con 6 opciones: 0–5 puntos) |
| **Lund Mackay** | Puntuación de TAC de senos paranasales, bilateral (izquierdo + derecho) | 0–24 | 12 (6 estructuras × 2 lados, cada una con 3 opciones: 0–2 puntos) |

### Otología

| Escala | Descripción | Rango | Preguntas |
|--------|-------------|-------|-----------|
| **THI** (Tinnitus Handicap Inventory) | Impacto del tinnitus en la calidad de vida | 0–100 | 25 (cada una con 3 opciones: No=0, A veces=2, Sí=4) |
| **ETDQ-7** (Eustachian Tube Dysfunction Questionnaire) | Síntomas de disfunción de la trompa de Eustaquio | 7–49 | 7 (cada una con 7 opciones: 1–7 puntos) |

## Estructura del proyecto

```
MedScale-ORL/
├── buildozer.spec          # Configuración de Buildozer para Android/iOS
├── requirements.txt        # Dependencias (kivy>=2.2.0)
├── __main__.py             # Entry point alternativo
│
├── frontend/
│   ├── __init__.py
│   ├── __main__.py         # Entry point: python3 -m frontend
│   ├── main.py             # Clase principal MedScaleORLApp, crea ScreenManager
│   │
│   ├── screens/
│   │   ├── base.py         # ScaleScreen: clase base con UI reutilizable
│   │   │                     (header, cards, checkboxes, inputs, resultado)
│   │   ├── home.py         # HomeScreen: pantalla principal con 3 pestañas
│   │   │                     (Apnea, Rinosinusitis, Otología) y navegación
│   │   ├── ess_screen.py   # Epworth Sleepiness Scale (8 preguntas, 0-3)
│   │   ├── stop_bang_screen.py  # STOP-BANG (8 ítems Sí/No)
│   │   ├── imc_screen.py        # IMC: inputs de peso y estatura
│   │   ├── snot22_screen.py     # SNOT-22 (22 preguntas, 0-5)
│   │   ├── lund_mackay_screen.py # Lund Mackay bilateral (12 ítems, 0-2)
│   │   ├── thi_screen.py        # THI (25 preguntas, 0/2/4)
│   │   └── etdq7_screen.py      # ETDQ-7 (7 preguntas, 1-7)
│   │
│   ├── assets/
│   │   ├── icon.png        # Icono de la app (1024×1024)
│   │   └── presplash.png   # Pantalla de carga
│   ├── utils/
│   └── widgets/
│
└── tests/
    └── test_frontend.py    # Tests unitarios básicos
```

## Ejecutar en desktop

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python3 -m frontend
```

Requiere Python 3.10+ y Kivy 2.2.0+.

## Compilar APK para Android

```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt-get install -y build-essential git python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    zip unzip openjdk-17-jdk

# Instalar Buildozer
pip install buildozer

# Compilar (primera vez descarga SDK/NDK, puede tardar ~30 min)
buildozer android debug

# El APK se genera en bin/
```

### Notas de compilación

- Arquitectura: `arm64-v8a` (todos los celulares desde 2016)
- API mínima: Android 5.0 (API 21)
- API target: Android 12 (API 31)
- NDK: r25b
- Orientation: portrait only
- Hay un bug conocido en `libthorvg` con armeabi-v7a que se soluciona compilando solo para arm64

## Stack tecnológico

- **Python 3.10+** — lenguaje principal
- **Kivy 2.2.0+** — framework UI multiplataforma
- **Buildozer** — compilación a Android/iOS
- **python-for-android** — toolchain de cross-compilación

## Diseño UI

- Navegación por pestañas en la parte inferior (Apnea, Rinosinusitis, Otología)
- Cards blancas con sombra para cada pregunta
- Checkboxes dibujados con canvas de Kivy (sin dependencia de fuentes Unicode)
- Colores: azul `#1976D2` (header/navegación), teal `#26A69A` (selección), gris `#F0F2F5` (fondo)
- Sizing responsivo con `dp()`/`sp()` para diferentes densidades de pantalla

## Tests

```bash
python3 -m pytest tests/ -v
```
