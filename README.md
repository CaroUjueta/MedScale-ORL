# MedScale-ORL

Calculadora de escalas clínicas para **otorrinolaringología**. App móvil standalone construida con Kivy.

## Escalas disponibles

### Apnea Obstructiva del Sueño
- **ESS** (Epworth Sleepiness Scale) — puntaje 0-24
- **STOP-BANG** — puntaje 0-8
- **IMC** (Índice de Masa Corporal) — kg/m²

### Rinosinusitis
- **SNOT-22** — puntaje 0-110
- **Lund Mackay** — puntaje 0-24 (bilateral)

### Otología
- **THI** (Tinnitus Handicap Inventory) — puntaje 0-100
- **ETDQ-7** — puntaje 7-49

## Ejecutar

```bash
# Crear entorno virtual (si no existe)
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python3 -m frontend
```

## Dependencias

- Python 3.10+
- Kivy >= 2.2.0
