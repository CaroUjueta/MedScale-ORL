import sqlite3
import json
import os
from datetime import datetime

_DB_NAME = "medscale.db"


def _db_path():
    if os.environ.get("ANDROID_PRIVATE"):
        return os.path.join(os.environ["ANDROID_PRIVATE"], _DB_NAME)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), _DB_NAME)


def get_conn():
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            expediente  TEXT UNIQUE NOT NULL,
            edad        INTEGER NOT NULL,
            sexo        TEXT NOT NULL CHECK(sexo IN ('M','F')),
            fecha_registro TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS evaluaciones (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id     INTEGER NOT NULL,
            tipo_escala     TEXT NOT NULL,
            respuestas      TEXT NOT NULL,
            puntaje         REAL NOT NULL,
            fecha           TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS configuracion (
            clave  TEXT PRIMARY KEY,
            valor  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS favoritos (
            escala  TEXT PRIMARY KEY,
            fecha   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS recientes (
            escala  TEXT PRIMARY KEY,
            fecha   TEXT NOT NULL
        );
    """)
    _ensure_default_config(conn)
    conn.commit()
    conn.close()


def _ensure_default_config(conn):
    defaults = {
        "correo_fijo": "francysujueta@gmail.com",
        "correo_configurable": "carouju1014@gmail.com",
        "smtp_usuario": "",
        "smtp_clave": "",
    }
    for clave, valor in defaults.items():
        conn.execute(
            "INSERT OR IGNORE INTO configuracion (clave, valor) VALUES (?, ?)",
            (clave, valor),
        )


def crear_paciente(expediente, edad, sexo):
    conn = get_conn()
    conn.execute(
        "INSERT INTO pacientes (expediente, edad, sexo, fecha_registro) VALUES (?, ?, ?, ?)",
        (expediente.strip(), int(edad), sexo, datetime.now().isoformat()),
    )
    conn.commit()
    pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return pid


def editar_paciente(paciente_id, expediente, edad, sexo):
    conn = get_conn()
    conn.execute(
        "UPDATE pacientes SET expediente=?, edad=?, sexo=? WHERE id=?",
        (expediente.strip(), int(edad), sexo, paciente_id),
    )
    conn.commit()
    conn.close()


def eliminar_paciente(paciente_id):
    conn = get_conn()
    conn.execute("DELETE FROM pacientes WHERE id=?", (paciente_id,))
    conn.commit()
    conn.close()


def obtener_pacientes(busqueda=None):
    conn = get_conn()
    if busqueda:
        rows = conn.execute(
            "SELECT * FROM pacientes WHERE expediente LIKE ? ORDER BY fecha_registro DESC",
            (f"%{busqueda}%",),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM pacientes ORDER BY fecha_registro DESC"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def obtener_paciente(paciente_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM pacientes WHERE id=?", (paciente_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def guardar_evaluacion(paciente_id, tipo_escala, respuestas, puntaje):
    conn = get_conn()
    conn.execute(
        "INSERT INTO evaluaciones (paciente_id, tipo_escala, respuestas, puntaje, fecha) VALUES (?, ?, ?, ?, ?)",
        (paciente_id, tipo_escala, json.dumps(respuestas, ensure_ascii=False), float(puntaje), datetime.now().isoformat()),
    )
    conn.commit()
    eid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return eid


def obtener_evaluaciones(paciente_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM evaluaciones WHERE paciente_id=? ORDER BY fecha DESC",
        (paciente_id,),
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["respuestas"] = json.loads(d["respuestas"])
        result.append(d)
    return result


def eliminar_evaluacion(evaluacion_id):
    conn = get_conn()
    conn.execute("DELETE FROM evaluaciones WHERE id=?", (evaluacion_id,))
    conn.commit()
    conn.close()


def obtener_config(clave):
    conn = get_conn()
    row = conn.execute("SELECT valor FROM configuracion WHERE clave=?", (clave,)).fetchone()
    conn.close()
    return row["valor"] if row else None


def obtener_toda_config():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM configuracion").fetchall()
    conn.close()
    return {r["clave"]: r["valor"] for r in rows}


def actualizar_config(clave, valor):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)",
        (clave, valor),
    )
    conn.commit()
    conn.close()


def es_favorita(escala):
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM favoritos WHERE escala=?", (escala,)
    ).fetchone()
    conn.close()
    return row is not None


def agregar_favorita(escala):
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO favoritos (escala, fecha) VALUES (?, ?)",
        (escala, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def quitar_favorita(escala):
    conn = get_conn()
    conn.execute("DELETE FROM favoritos WHERE escala=?", (escala,))
    conn.commit()
    conn.close()


def obtener_favoritas():
    conn = get_conn()
    rows = conn.execute("SELECT escala FROM favoritos ORDER BY fecha DESC").fetchall()
    conn.close()
    return [r["escala"] for r in rows]


def registrar_uso_escala(escala):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO recientes (escala, fecha) VALUES (?, ?)",
        (escala, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def obtener_recientes():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM recientes ORDER BY fecha DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
