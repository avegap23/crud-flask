"""Utilidades de seguridad para la APP en Flask:
    - Protección CSRF con patrón synchronizer token
    - Cabeceras HTTP de seguridad
    - Validación de credenciales de administrador"""

# IMPORTS -----------------------------------------------------------------------------------------
from __future__ import annotations # https://docs.python.org/3/library/__future__.html#future__.annotations

import secrets # https://docs.python.org/3/library/secrets.html
from typing import Any # https://docs.python.org/3/library/typing.html
from urllib.parse import urlsplit # https://docs.python.org/3/library/urllib.parse.html

from flask import abort, current_app, redirect, request, session, url_for
from werkzeug.security import check_password_hash # https://werkzeug.palletsprojects.com/en/stable/

# SECURIZACIÓN ------------------------------------------------------------------------------------
SAFE_METHODS = {"GET", "HEAD", "OPTONS", "TRACE"} # métodos SÓLO de lectura, no modificables
CSRF_SESSION_KEY = "_csrf_token" # guardado del token dentro de la sesión
AUTH_SESSION_KEY = "is_authenticated" # indica que el usuario está autenticado

# FUNCTIONS ---------------------------------------------------------------------------------------
# a.- Creación de token CSRF unido a la sesión de usuario
def generate_csrf_token() -> str:
    """Creación de token CSRF unido a la sesión de usuario"""

    token = session.get(CSRF_SESSION_KEY)

    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
    
    return str(token)

# b.- Lectura de token (cabecera HTTP o formulario)
def _get_submitted_csrf_token() -> str:
    """Lectura de token (cabecera HTTP o formulario)"""
    return request.form.get("csrf_token", "") or request.headers.get("X-CSRF_Token", "")

# c.- Comprobación de token: ¿Lo tuyo es igual que lo mío?
def validate_csrf_token() -> bool:
    """Comprueba el token que envía el cliente"""
    expected = session.get(CSRF_SESSION_KEY)
    submitted = _get_submitted_csrf_token()

    # si no hay expected o submitted
    if not expected or not submitted:
        return False
    
    # compara los valores de forma segura en poco tiempo
    return secrets.compare_digest(str(expected), str(submitted))

# d.- Validación de credenciales
def validate_admin_credentials(username:str, password:str) -> bool:
    """Valida el usuario y contraseña de administrador"""

    # Validar el usuario
    expected_username = current_app.config.get("ADMIN_USERNAME", "admin")

    if not secrets.compare_digest(username or "", expected_username):
        return False
    
    # validar la contraseña
    password_hash = current_app.config.get("ADMIN_PASSWORD_HASH")
    if password_hash:
        return check_password_hash(password_hash, password or "")

    expected_password = current_app.config.get("ADMIN_PASSWORD")
    if not expected_password:
        return False
    
    # compara los valores de forma segura en poco tiempo
    return secrets.compare_digest(password or "", expected_password)

# e.- Validación de redirecciones: evitar redicrecciones a dominio externo
def is_safe_redirect_target(target: str | None) -> bool:
    """Evita redirecciones abiertas a dominios externos"""

    if not target:
        return False
    
    parsed = urlsplit(target) # me revisa cada uno de los parámetros de la URL
    return parsed.scheme == "" and parsed.netloc == "" and target.startswith("/") and not target.startswith("//")
    # scheme: protocolo https, http
    # netloc: dominio
    # startwith ("/"): exige que la dirección comience por /... (/admin)
    # startwith ("//"): evita URLs de tipo //sitiomalo.com

def safe_redirect(target: str | None, fallback_endpoint:str = "products.index", **values: Any):
    """Redirección SÓLO a rutas locales seguras"""

    # Si la ruta interna es válida
    if is_safe_redirect_target(target):
        return redirect(target) # redirecciones a /products?id=123
    # si la URL no es segura, p.e. /user/54
    return redirect(url_for(fallback_endpoint, **values))
    # **values me permite pasar parámetros adicionales a url_for

# SECURE ROUTES -----------------------------------------------------------------------------------
# f.- Registro de CSRF, cabeceras seguras y helpers Jinja
def register_security(app):
    """Registra CSRF, cabeceras de seguridad y los helpers de Jinja"""
    
    # helper = una función global que Jinja "cree" que es un filtro
    app.jinja_env.globals["csrf_token"] = generate_csrf_token()
    # <input type="hidden" name"csrf_token" value="{{ csrf_token }}">
    # generate_csrf_token jinja ejecuta csrf_token(). Si escribes generate_csrf_token(),
    # guardas el resultado generado en ese momento

    # 1.- Protección antes del proceso de la petición HTTP
    @app.before_request
    def csrf_protect():
        # ¿CSRF activado?
        if not app.config.get("CSRF_ENABLED", True):
            return None
        
        # ¿Métodos de seguridad activados? Entonces no compruebo el token...
        if request.method in SAFE_METHODS:
            return None
        
        # Momento de modificar... ¡¡Validado el token!!
        if not validate_csrf_token():
            # mensaje de bloqueo de la ruta (logs)
            current_app.logger.warning("Petición bloqueada por CSRF inválido: %s", request.path)
            # error 400
            abort(400, description="¡¡Token inválido o ausente!!")
    
    # 2.- Protección después de procesar la ruta, antes de enviar la respuesta al navegador
    @app.after_request
    def set_security_headers(response):
        # comprobando que las cabeceras de seguridad están activadas
        if not app.config.get("SECURITY_HEADERS_ENABLED", True):
            return response
        
        # definición de CABECERAS DE SEGURIDAD
        response.headers.setdefault("X-Content-Type_Options", "nosniff") # evita ejecución de JS o "adivinación"
        response.headers.setdefault("X-Frame-Options", "DENY") # evita el clickjaking, impide que la página se muestre en un iframe
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin") # para navegar en el dominio original
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()") # podemos desactivar cierto hardware (por ejemplo)

        # definición de CABECERAS CSP (Content Security Policy)
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self';" # sólo permite recursos del mismo dominio
            "base-uri 'self';" # restringimos la tag <base> al mismo origen
            "form-action 'self';" # los formularios sólamente se envían dentro del mismo dominio
            "frame_ancestors 'none';" # impedimos que otros sitios inserten esta APP en un iframe
            "object-src 'none';" # bloquea elementos como <object> y <embed>
            "img-src 'self', data:;" # permite utilizar imágenes del propio dominio o las que se incluyan con data:
            "style-src 'self' https://cdn.jsdelivr.net;" # permite CSS local o de jsDelivr
            "script-src 'self' https://cdn.jsdelivr.net;" # permite JS local o de jsDelivr
            "connect-src 'self;", # las conexiones a APIs sólo pueden dirigirse al mismo origen
        )
        return response
        # setdefault actúa si no hay políticas definidas, poniendo "por defecto" las mismas. Si ya las tenemos, no se sobreescriben