import re
from datetime import datetime, timedelta

TIPOS_DOCUMENTO = {"CC", "TI", "CE", "PP", "NIT"}
TIPOS_TELEFONO = {"Celular", "Fijo", "Corporativo", "Otro"}
TIPOS_SOLICITUD = {"Petición", "Queja", "Reclamo", "Sugerencia"}
CANALES_RECEPCION = {
    "Presencial",
    "Correo electrónico",
    "Página web",
    "Teléfono",
    "Redes sociales",
    "Otro",
}
TIPOS_MASCOTA = {"Perro", "Gato", "Otro"}
PERFILES_SOLICITANTE = {"Estudiante", "Docente", "Administrativo", "Ciudadano"}
CAMPUS_UDEA = {
    "Campus Medellín - Ciudad Universitaria",
    "Campus Medellín - Ciudadela Robledo",
    "Campus en el Área de la salud",
    "Campus Medellín - Sede de Posgrado",
    "Campus Medellín - Edificio San Ignacio",
    "Campus Medellín - Antigua Escuela de Derecho",
    "Campus Medellín - Edificio Antioquia",
    "Campus Medellín - Casas Patrimoniales",
    "Campus Medellín - Edificio de Extensión",
}
ESTADOS_VALIDOS = ("Registrada", "En proceso", "Solucionada")
PLAZO_MAXIMO_DIAS = 30


def validar_nombre(nombre: str) -> tuple[bool, str]:
    if not isinstance(nombre, str):
        return False, "El nombre debe ser texto."
    nombre_limpio = nombre.strip()
    if not (3 <= len(nombre_limpio) <= 100):
        return False, "El nombre debe tener entre 3 y 100 caracteres."
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñüÜ'\- ]+", nombre_limpio):
        return False, "El nombre solo permite letras, espacios, tildes, apóstrofes (') o guiones (-). No permite números."
    if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñüÜ]", nombre_limpio):
        return False, "El nombre debe incluir letras."
    return True, nombre_limpio


def validar_perfil_solicitante(perfil: str) -> tuple[bool, str]:
    """Valida el perfil institucional claro, obligatorio y categórico del solicitante."""
    return validar_opcion_lista(perfil, PERFILES_SOLICITANTE, "Perfil del solicitante")


def validar_tipo_documento(tipo_doc: str) -> tuple[bool, str]:
    valor = tipo_doc.strip().upper()
    if valor not in TIPOS_DOCUMENTO:
        return False, f"Tipo de documento inválido. Permitidos: {', '.join(sorted(TIPOS_DOCUMENTO))}."
    return True, valor


def validar_numero_documento(num_doc: str) -> tuple[bool, str]:
    valor = num_doc.strip()
    if not valor.isdigit() or not (3 <= len(valor) <= 15):
        return False, "El número de documento debe contener únicamente entre 3 y 15 dígitos."
    return True, valor


def validar_tipo_telefono(tipo_tel: str) -> tuple[bool, str]:
    mapa = {t.lower(): t for t in TIPOS_TELEFONO}
    valor = mapa.get(tipo_tel.strip().lower())
    if not valor:
        return False, f"Tipo de teléfono inválido. Permitidos: {', '.join(sorted(TIPOS_TELEFONO))}."
    return True, valor


def validar_telefono(telefono: str) -> tuple[bool, str]:
    valor = telefono.strip()
    if not valor.isdigit() or len(valor) != 10:
        return False, "El teléfono de contacto debe tener exactamente 10 dígitos numéricos."
    return True, valor


def validar_correo(correo: str) -> tuple[bool, str]:
    valor = correo.strip()
    if not valor or len(valor) > 254:
        return False, "El correo es obligatorio y no puede superar 254 caracteres."
    if valor.count("@") != 1:
        return False, "El correo debe contener un único símbolo '@'."
    local, dominio = valor.split("@")
    if not local or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        return False, "El correo debe cumplir la estructura correo@dominio.com."
    if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", valor):
        return False, "El formato del correo electrónico no es válido."
    return True, valor


def validar_direccion(direccion: str) -> tuple[bool, str]:
    valor = direccion.strip()
    if valor == "" or valor.upper() == "N/A":
        return True, "N/A"
    if not (5 <= len(valor) <= 200):
        return False, "La dirección debe tener entre 5 y 200 caracteres (o dejarse vacía para N/A)."
    if not re.fullmatch(r"[A-Za-z0-9ÁÉÍÓÚáéíóúÑñüÜ#\-./ ]+", valor):
        return False, "La dirección solo permite letras, números y caracteres comunes (#, -, ., /)."
    return True, valor


def validar_opcion_lista(valor: str, permitidos: set[str], etiqueta: str) -> tuple[bool, str]:
    limpio = valor.strip()
    for item in permitidos:
        if limpio.lower() == item.lower():
            return True, item
    return False, f"{etiqueta} inválido. Valores permitidos: {', '.join(sorted(permitidos))}."


def validar_fecha_radicacion(fecha_str: str) -> tuple[bool, datetime | str]:
    limpio = fecha_str.strip()
    formatos = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d")
    fecha_dt = None
    for fmt in formatos:
        try:
            fecha_dt = datetime.strptime(limpio, fmt)
            if fmt == "%Y-%m-%d":
                ahora = datetime.now()
                fecha_dt = fecha_dt.replace(hour=ahora.hour, minute=ahora.minute, second=ahora.second)
            break
        except ValueError:
            continue

    if fecha_dt is None:
        return False, "Formato de fecha inválido. Use AAAA-MM-DD HH:MM:SS o AAAA-MM-DD."
    if fecha_dt > datetime.now():
        return False, "La fecha de radicación no puede ser una fecha futura."
    return True, fecha_dt


def calcular_fecha_maxima(fecha_radicacion: datetime, dias: int = PLAZO_MAXIMO_DIAS) -> datetime:
    return fecha_radicacion + timedelta(days=dias)


def validar_asunto(asunto: str) -> tuple[bool, str]:
    limpio = asunto.strip()
    if not (5 <= len(limpio) <= 150):
        return False, "El asunto o título debe tener entre 5 y 150 caracteres."
    if not re.fullmatch(r"[A-Za-z0-9ÁÉÍÓÚáéíóúÑñüÜ.,;:!?¿¡()\-/ ]+", limpio):
        return False, "El asunto contiene caracteres no permitidos."
    return True, limpio


def validar_descripcion(descripcion: str) -> tuple[bool, str]:
    if not isinstance(descripcion, str) or not descripcion.strip():
        return False, "La descripción detallada es obligatoria y no puede contener únicamente espacios."
    limpio = descripcion.strip()
    if not (20 <= len(limpio) <= 2000):
        return False, "La descripción detallada debe tener entre 20 y 2000 caracteres."
    return True, limpio


def validar_transicion_estado(estado_actual: str, nuevo_estado: str) -> tuple[bool, str]:
    if estado_actual not in ESTADOS_VALIDOS:
        return False, "Estado actual no reconocido."
    mapa = {e.lower(): e for e in ESTADOS_VALIDOS}
    nuevo_norm = mapa.get(nuevo_estado.strip().lower())
    if not nuevo_norm:
        return False, f"Estado inválido. Permitidos: {', '.join(ESTADOS_VALIDOS)}."
    idx_actual = ESTADOS_VALIDOS.index(estado_actual)
    idx_nuevo = ESTADOS_VALIDOS.index(nuevo_norm)
    if idx_nuevo != idx_actual + 1:
        return (
            False,
            f"Transición inválida: el flujo obligatorio es Registrada -> En proceso -> Solucionada (actual: {estado_actual}).",
        )
    return True, nuevo_norm


class c_validaciones:
    """Clase central, modular y reutilizable para las validaciones del sistema."""
    validar_nombre = staticmethod(validar_nombre)
    validar_tipo_documento = staticmethod(validar_tipo_documento)
    validar_numero_documento = staticmethod(validar_numero_documento)
    validar_tipo_telefono = staticmethod(validar_tipo_telefono)
    validar_telefono = staticmethod(validar_telefono)
    validar_correo = staticmethod(validar_correo)
    validar_direccion = staticmethod(validar_direccion)
    validar_fecha_radicacion = staticmethod(validar_fecha_radicacion)
    validar_perfil_solicitante = staticmethod(validar_perfil_solicitante)
    calcular_fecha_maxima = staticmethod(calcular_fecha_maxima)

# Objeto compartido para acceso organizado a las reglas de validación.
validador = c_validaciones()
