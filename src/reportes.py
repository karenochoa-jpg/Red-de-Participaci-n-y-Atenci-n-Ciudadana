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