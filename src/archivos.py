import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

ARCHIVOS_POR_TIPO = {
    "Petición": DATA_DIR / "Peticion.txt",
    "Queja": DATA_DIR / "Queja.txt",
    "Reclamo": DATA_DIR / "Reclamo.txt",
    "Sugerencia": DATA_DIR / "Sugerencia.txt",
}

USUARIOS_FILE = DATA_DIR / "usuarios.txt"


def asegurar_archivos() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for ruta in ARCHIVOS_POR_TIPO.values():
        if not ruta.exists():
            ruta.write_text("", encoding="utf-8")
    if not USUARIOS_FILE.exists():
        usuarios_defecto = [
            "admin_udea|admin@udea.edu.co|Udea2026*|Administrador|Administrador General UdeA",
            "kelly.martinez|kelly.martinezc@udea.edu.co|Kelly2026*|Operador|Kelly Ester Martínez Cuadrado",
            "angela.calle|angela.calle@udea.edu.co|Angela2026*|Operador|Angela Maria Calle Loaiza",
            "leidy.torres|leidy.torres@udea.edu.co|Leidy2026*|Operador|Leidy Camila Torres Henao",
            "karen.ochoa|karen.ochoa@udea.edu.co|Karen2026*|Operador|Karen Darian Ochoa Pertuz",
        ]
        USUARIOS_FILE.write_text("\n".join(usuarios_defecto) + "\n", encoding="utf-8")


def cargar_usuarios() -> list[dict]:
    asegurar_archivos()
    usuarios = []
    for linea in USUARIOS_FILE.read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.startswith("#"):
            continue
        partes = linea.strip().split("|")
        if len(partes) >= 4:
            usuarios.append(
                {
                    "usuario": partes[0].strip(),
                    "correo": partes[1].strip(),
                    "password": partes[2].strip(),
                    "rol": partes[3].strip(),
                    "nombre": partes[4].strip() if len(partes) > 4 else partes[0].strip(),
                }
            )
    return usuarios


def leer_registros_archivo(ruta: Path) -> list[dict]:
    asegurar_archivos()
    registros = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        registros.append(json.loads(linea))
    return registros


def guardar_registros_archivo(ruta: Path, registros: list[dict]) -> None:
    asegurar_archivos()
    contenido = "\n".join(json.dumps(reg, ensure_ascii=False) for reg in registros)
    if contenido:
        contenido += "\n"
    ruta.write_text(contenido, encoding="utf-8")


def obtener_siguiente_id(tipo_solicitud: str) -> int:
    ruta = ARCHIVOS_POR_TIPO[tipo_solicitud]
    registros = leer_registros_archivo(ruta)
    if not registros:
        return 1
    return max(int(r.get("id", 0)) for r in registros) + 1


def agregar_registro(registro: dict) -> dict:
    tipo = registro["tipo_solicitud"]
    ruta = ARCHIVOS_POR_TIPO[tipo]
    registros = leer_registros_archivo(ruta)
    registro["id"] = obtener_siguiente_id(tipo)
    registros.append(registro)
    guardar_registros_archivo(ruta, registros)
    return registro


def obtener_todos_los_registros() -> list[dict]:
    todos = []
    for tipo, ruta in ARCHIVOS_POR_TIPO.items():
        for reg in leer_registros_archivo(ruta):
            copia = dict(reg)
            copia.setdefault("tipo_solicitud", tipo)
            copia.setdefault("perfil_solicitante", "No especificado")
            todos.append(copia)
    return todos


def actualizar_registro(tipo_solicitud: str, id_registro: int, nuevos_campos: dict) -> bool:
    ruta = ARCHIVOS_POR_TIPO[tipo_solicitud]
    registros = leer_registros_archivo(ruta)
    for reg in registros:
        if int(reg["id"]) == int(id_registro):
            reg.update(nuevos_campos)
            guardar_registros_archivo(ruta, registros)
            return True
    return False


class c_archivos:
    """Clase modular, persistente y reutilizable para administrar archivos planos."""
    asegurar = staticmethod(asegurar_archivos)
    cargar_usuarios = staticmethod(cargar_usuarios)
    leer = staticmethod(leer_registros_archivo)
    guardar = staticmethod(guardar_registros_archivo)
    agregar = staticmethod(agregar_registro)
    consultar_todos = staticmethod(obtener_todos_los_registros)
    actualizar = staticmethod(actualizar_registro)

# Instancia principal para operaciones organizadas de almacenamiento.
repositorio = c_archivos()
