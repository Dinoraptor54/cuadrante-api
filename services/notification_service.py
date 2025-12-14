# -*- coding: utf-8 -*-
"""
Servicio de notificaciones
Manejo de envío de correos electrónicos
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from utils.logging_config import log_info, log_error

def send_email(to_email: str, subject: str, body: str):
    """
    Envía un correo electrónico
    Si no hay configuración SMTP, solo loguea el mensaje
    """
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        log_info(f"📧 [MOCK EMAIL] To: {to_email} | Subject: {subject}")
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SMTP_USER, to_email, text)
        server.quit()
        
        log_info(f"📧 Email enviado a {to_email}")
        return True
    except Exception as e:
        log_error(f"Error enviando email a {to_email}", error=e)
        return False

def notify_permuta_request(solicitante_email: str, receptor_email: str, fecha_origen: str, fecha_destino: str):
    """Notifica al receptor sobre una nueva solicitud de permuta"""
    subject = "Nueva Solicitud de Permuta de Turno"
    body = f"""
    Hola,
    
    El usuario {solicitante_email} te ha solicitado un cambio de turno.
    
    Tu turno del día: {fecha_destino}
    Por su turno del día: {fecha_origen}
    
    Por favor, accede a la aplicación para aceptar o rechazar la solicitud.
    """
    send_email(receptor_email, subject, body)

def notify_vacacion_created(solicitante_email: str, fecha_inicio: str, fecha_fin: str):
    """Notifica al admin (o al usuario) sobre creación de solicitud"""
    # En un caso real, notificaríamos a RRHH o al Coordinador
    # Por ahora, confirmamos al usuario
    subject = "Solicitud de Vacaciones Registrada"
    body = f"""
    Hola,
    
    Hemos registrado tu solicitud de vacaciones.
    
    Desde: {fecha_inicio}
    Hasta: {fecha_fin}
    
    Te notificaremos cuando sea aprobada o rechazada.
    """
    send_email(solicitante_email, subject, body)
