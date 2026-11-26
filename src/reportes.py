from collections import Counter
from datetime import datetime
from pathlib import Path
from archivos import DATA_DIR, obtener_todos_los_registros

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"


def _parse_fecha(valor: str) -> datetime | None:
    if not valor or not str(valor).strip():
        return None
    texto = str(valor).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            continue
    return None


def promedio_dias_respuesta_entero(registros: list[dict]) -> int:
    """
    Estadística obligatoria: promedio de días en valores enteros que toma dar respuesta a una PQRS.
    Usa los registros solucionados; si aún no existen, calcula el tiempo transcurrido en trámite.
    """
    dias_solucionados = []
    dias_tramite = []
    ahora = datetime.now()
    for r in registros:
        f_rad = _parse_fecha(r.get("fecha_radicacion", ""))
        if not f_rad:
            continue
        f_sol = _parse_fecha(r.get("fecha_solucion", ""))
        if f_sol and f_sol >= f_rad:
            dias_solucionados.append((f_sol - f_rad).days)
        elif ahora >= f_rad:
            dias_tramite.append((ahora - f_rad).days)

    muestra = dias_solucionados if dias_solucionados else dias_tramite
    if not muestra:
        return 0
    return int(round(sum(muestra) / len(muestra)))


def generar_estadisticas() -> dict:
    registros = obtener_todos_los_registros()
    total = len(registros)
    ahora = datetime.now()

    solucionadas = sum(1 for r in registros if r.get("estado_peticion") == "Solucionada")
    porcentaje_resolucion = round((solucionadas / total) * 100, 1) if total > 0 else 0.0

    por_vencer = []
    vencidos = []
    con_fecha = []

    for r in registros:
        f_rad = _parse_fecha(r.get("fecha_radicacion", ""))
        if f_rad:
            con_fecha.append((f_rad, r))
        if r.get("estado_peticion") != "Solucionada":
            f_max = _parse_fecha(r.get("fecha_maxima_respuesta", ""))
            if f_max:
                dias_restantes = (f_max - ahora).days
                if dias_restantes < 0:
                    vencidos.append(r)
                elif dias_restantes <= 5:
                    por_vencer.append(r)

    con_fecha.sort(key=lambda item: item[0])
    documentos_mas_antiguos = [item[1] for item in con_fecha[:5]]

    return {
        "total_registros": total,
        "promedio_dias_respuesta_entero": promedio_dias_respuesta_entero(registros),
        "por_tipo_solicitud": dict(Counter(r.get("tipo_solicitud", "N/A") for r in registros)),
        "por_tipo_documento": dict(Counter(r.get("tipo_documento", "N/A") for r in registros)),
        "por_perfil_solicitante": dict(Counter(r.get("perfil_solicitante", "N/A") for r in registros)),
        "por_mascota": dict(Counter(r.get("tipo_mascota", "N/A") for r in registros)),
        "por_canal": dict(Counter(r.get("canal_recepcion", "N/A") for r in registros)),
        "por_campus": dict(Counter(r.get("campus_relacionado", "N/A") for r in registros)),
        "por_estado": dict(Counter(r.get("estado_peticion", "N/A") for r in registros)),
        "por_usuario_registro": dict(Counter(r.get("usuario_registro", "N/A") for r in registros)),
        "porcentaje_resolucion": porcentaje_resolucion,
        "documentos_mas_antiguos": documentos_mas_antiguos,
        "por_vencer": por_vencer,
        "vencidos": vencidos,
    }


def exportar_reporte_txt() -> Path:
    stats = generar_estadisticas()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ruta = DATA_DIR / "reporte_estadisticas.txt"

    lineas = [
        "=" * 70,
        "HUELLAACTIVA UDEA - REPORTE ESTADÍSTICO DE PQRS",
        f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 70,
        f"Total de PQRS registradas: {stats['total_registros']}",
        f"Promedio de días de respuesta (entero): {stats['promedio_dias_respuesta_entero']} días",
        f"Efectividad de resolución: {stats['porcentaje_resolucion']}%",
        f"Próximos a vencer (<=5 días): {len(stats['por_vencer'])}",
        f"Vencidos: {len(stats['vencidos'])}",
        "-" * 70,
        f"Por tipo de solicitud: {stats['por_tipo_solicitud']}",
        f"Por estado: {stats['por_estado']}",
        f"Por tipo de mascota: {stats['por_mascota']}",
        f"Por campus UdeA: {stats['por_campus']}",
        f"Por perfil del solicitante: {stats['por_perfil_solicitante']}",
        f"Por canal de recepción: {stats['por_canal']}",
        "=" * 70,
    ]
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return ruta


def generar_graficos() -> list[Path]:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError(
            "La librería 'matplotlib' no está instalada. Ejecute: python -m pip install matplotlib"
        ) from exc

    stats = generar_estadisticas()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    rutas = []

    graficas = [
        ("pqrs_por_tipo.png", "PQRS por Tipo de Solicitud", stats["por_tipo_solicitud"], "#026937"),
        ("pqrs_por_estado.png", "PQRS por Estado", stats["por_estado"], "#1E8449"),
        ("pqrs_por_mascota.png", "PQRS por Tipo de Mascota", stats["por_mascota"], "#2E86C1"),
    ]

    for nombre_archivo, titulo, datos, color in graficas:
        ruta = IMAGES_DIR / nombre_archivo
        fig, ax = plt.subplots(figsize=(7, 4))
        etiquetas = list(datos.keys()) if datos else ["Sin datos"]
        valores = list(datos.values()) if datos else [0]
        ax.bar(etiquetas, valores, color=color)
        ax.set_title(titulo)
        ax.set_ylabel("Cantidad de PQRS")
        plt.xticks(rotation=15, ha="right")
        plt.tight_layout()
        fig.savefig(ruta, dpi=150)
        plt.close(fig)
        rutas.append(ruta)

    return rutas
