import csv
import io
import json
import socket
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from frontend.database import (
    obtener_paciente,
    obtener_evaluaciones,
    obtener_config,
)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def hay_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def _build_csv(paciente, evaluaciones):
    buf = io.StringIO()
    writer = csv.writer(buf)

    writer.writerow(["PACIENTE"])
    writer.writerow(["Expediente", paciente["expediente"]])
    writer.writerow(["Edad", paciente["edad"]])
    writer.writerow(["Sexo", "Masculino" if paciente["sexo"] == "M" else "Femenino"])
    writer.writerow([])

    writer.writerow(["EVALUACIONES"])
    writer.writerow(["Fecha", "Escala", "Puntaje", "Respuestas"])

    for ev in evaluaciones:
        resp_str = json.dumps(ev["respuestas"], ensure_ascii=False)
        writer.writerow([ev["fecha"], ev["tipo_escala"], ev["puntaje"], resp_str])

    return buf.getvalue().encode("utf-8")


def _build_json(paciente, evaluaciones):
    data = {
        "paciente": {
            "expediente": paciente["expediente"],
            "edad": paciente["edad"],
            "sexo": paciente["sexo"],
        },
        "evaluaciones": evaluaciones,
    }
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")


def enviar_correo(paciente_id, callback=None):
    def _task():
        try:
            paciente = obtener_paciente(paciente_id)
            if not paciente:
                if callback:
                    callback(False, "Paciente no encontrado")
                return

            evaluaciones = obtener_evaluaciones(paciente_id)
            if not evaluaciones:
                if callback:
                    callback(False, "No hay evaluaciones para enviar")
                return

            if not hay_internet():
                if callback:
                    callback(False, "Sin conexion a internet")
                return

            smtp_usuario = obtener_config("smtp_usuario") or ""
            smtp_clave = obtener_config("smtp_clave") or ""
            correo_fijo = obtener_config("correo_fijo") or ""
            correo_config = obtener_config("correo_configurable") or ""

            if not smtp_usuario or not smtp_clave:
                if callback:
                    callback(False, "Credenciales SMTP no configuradas")
                return

            destinatarios = [correo_fijo]
            if correo_config:
                destinatarios.append(correo_config)

            msg = MIMEMultipart()
            msg["From"] = smtp_usuario
            msg["To"] = ", ".join(destinatarios)
            msg["Subject"] = f"MedScale-ORL - Paciente {paciente['expediente']}"

            body = (
                f"Adjunto se encuentran los datos del paciente expediente "
                f"{paciente['expediente']} ({paciente['edad']} anios, "
                f"{'Masculino' if paciente['sexo'] == 'M' else 'Femenino'}).\n\n"
                f"Total de evaluaciones: {len(evaluaciones)}\n"
                f"Generado por MedScale-ORL"
            )
            msg.attach(MIMEText(body, "plain"))

            csv_data = _build_csv(paciente, evaluaciones)
            part_csv = MIMEBase("application", "octet-stream")
            part_csv.set_payload(csv_data)
            encoders.encode_base64(part_csv)
            part_csv.add_header(
                "Content-Disposition",
                f"attachment; filename=paciente_{paciente['expediente']}.csv",
            )
            msg.attach(part_csv)

            json_data = _build_json(paciente, evaluaciones)
            part_json = MIMEBase("application", "octet-stream")
            part_json.set_payload(json_data)
            encoders.encode_base64(part_json)
            part_json.add_header(
                "Content-Disposition",
                f"attachment; filename=paciente_{paciente['expediente']}.json",
            )
            msg.attach(part_json)

            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(smtp_usuario, smtp_clave)
            server.sendmail(smtp_usuario, destinatarios, msg.as_string())
            server.quit()

            if callback:
                callback(True, "Correo enviado exitosamente")

        except smtplib.SMTPAuthenticationError:
            if callback:
                callback(False, "Error de autenticacion SMTP. Verifica usuario/clave.")
        except Exception as e:
            if callback:
                callback(False, f"Error: {str(e)}")

    thread = threading.Thread(target=_task, daemon=True)
    thread.start()
    return thread
