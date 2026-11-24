import textwrap 
import time
from datetime import datetime
from pathlib import Path
from archivos import (
    ARCHIVOS_POR_TIPO,
    DATA_DIR,
    actualizar_registro,
    agregar_registro,
    asegurar_archivos,
    cargar_usuarios,
    leer_registros_archivo,
    obtener_todos_los_registros,
)
from reportes import exportar_reporte_txt, generar_estadisticas, generar_graficos
from validaciones import (
    CAMPUS_UDEA,
    CANALES_RECEPCION,
    ESTADOS_VALIDOS,
    PERFILES_SOLICITANTE,
    TIPOS_MASCOTA,
    TIPOS_SOLICITUD,
    calcular_fecha_maxima,
    validar_asunto,
    validar_correo,
    validar_descripcion,
    validar_direccion,
    validar_fecha_radicacion,
    validar_nombre,
    validar_numero_documento,
    validar_opcion_lista,
    validar_perfil_solicitante,
    validar_telefono,
    validar_tipo_documento,
    validar_tipo_telefono,
    validar_transicion_estado,
)

NOMBRE_SISTEMA = "HUELLAACTIVA UDEA - GESTOR DE PQRS"
ANCHO_RADICADO = 120
SEGUNDOS_BLOQUEO = 15


def _linea_borde(izq: str, relleno: str, der: str) -> str:
    return f"{izq}{relleno * (ANCHO_RADICADO - 2)}{der}"


def _lineas_texto(texto: str, centrar: bool = False) -> list[str]:
    """Formatea una o varias líneas garantizando exactamente 120 caracteres sin cortar palabras."""
    contenido_max = ANCHO_RADICADO - 4
    fragmentos = textwrap.wrap(str(texto), width=contenido_max) or [""]
    resultado = []
    for frag in fragmentos:
        relleno = frag.center(contenido_max) if centrar else frag.ljust(contenido_max)
        linea = f"| {relleno} |"
        assert len(linea) == ANCHO_RADICADO, f"Error de ancho: {len(linea)}"
        resultado.append(linea)
    return resultado


def generar_comprobante_ascii(registro: dict) -> str:
    """
    Comprobante de radicación en formato ASCII de ancho fijo exacto de 120 caracteres.
    Excluye la descripción detallada y muestra N/A cuando la dirección no fue ingresada.
    """
    direccion = registro.get("direccion") or "N/A"
    if not str(direccion).strip():
        direccion = "N/A"

    lineas = [_linea_borde("+", "-", "+")]
    lineas.extend(_lineas_texto(NOMBRE_SISTEMA, centrar=True))
    lineas.extend(_lineas_texto("UNIVERSIDAD DE ANTIOQUIA - COMPROBANTE OFICIAL DE RADICACIÓN PQRS", centrar=True))
    lineas.append(_linea_borde("+", "=", "+"))
    lineas.extend(_lineas_texto("1. DATOS DEL RADICADO"))
    lineas.extend(
        _lineas_texto(
            f"ID Radicado: {int(registro['id']):05d} | "
            f"Fecha/Hora: {registro['fecha_radicacion']} | "
            f"Estado: {registro['estado_peticion']} | "
            f"Fecha Máx. Respuesta: {registro['fecha_maxima_respuesta']}"
        )
    )
    lineas.append(_linea_borde("+", "-", "+"))
    lineas.extend(_lineas_texto("2. DATOS DEL SOLICITANTE"))
    lineas.extend(
        _lineas_texto(
            f"Nombre Completo: {registro['nombre_completo']} | "
            f"Documento: {registro['tipo_documento']} {registro['numero_documento']}"
        )
    )
    lineas.extend(
        _lineas_texto(
            f"Teléfono: {registro['telefono_contacto']} ({registro['tipo_telefono']}) | "
            f"Correo: {registro['correo_electronico']}"
        )
    )
    lineas.extend(_lineas_texto(f"Dirección: {direccion}"))
    lineas.append(_linea_borde("+", "-", "+"))
    lineas.extend(_lineas_texto("3. CLASIFICACIÓN Y RESUMEN DE LA SOLICITUD"))
    lineas.extend(
        _lineas_texto(
            f"Tipo: {registro['tipo_solicitud']} | "
            f"Canal: {registro['canal_recepcion']} | "
            f"Mascota: {registro['tipo_mascota']}"
        )
    )
    lineas.extend(_lineas_texto(f"Campus Relacionado: {registro['campus_relacionado']}"))
    lineas.extend(_lineas_texto(f"Asunto: {registro['asunto_titulo']}"))
    lineas.extend(_lineas_texto(f"Funcionario Registrador: {registro.get('usuario_registro', 'N/A')}"))
    lineas.append(_linea_borde("+", "-", "+"))
    return "\n".join(lineas)


def guardar_radicado_txt(registro: dict) -> Path:
    carpeta_radicados = DATA_DIR / "radicados"
    carpeta_radicados.mkdir(parents=True, exist_ok=True)
    tipo_sin_tilde = registro["tipo_solicitud"].lower().replace("ó", "o")
    nombre_archivo = f"radicado_{tipo_sin_tilde}_{int(registro['id']):05d}.txt"
    ruta = carpeta_radicados / nombre_archivo
    comprobante = generar_comprobante_ascii(registro)
    ruta.write_text(comprobante + "\n", encoding="utf-8")
    return ruta


def solicitar_validado(prompt: str, validador):
    while True:
        valor = input(prompt)
        ok, resultado = validador(valor)
        if ok:
            return resultado
        print(f"  [Error de validación] {resultado}")


def autenticar_usuario() -> dict | None:
    usuarios = cargar_usuarios()
    intentos_fallidos = 0

    while True:
        print("\n" + "=" * 60)
        print(f"  {NOMBRE_SISTEMA}")
        print("  MÓDULO DE AUTENTICACIÓN (LOGIN)")
        print("=" * 60)
        credencial = input("1. Ingrese Usuario o Correo institucional (o 'salir'): ").strip()
        if credencial.lower() == "salir":
            return None
        clave = input("2. Ingrese Clave: ").strip()

        for u in usuarios:
            if (
                credencial.lower() in (u["usuario"].lower(), u["correo"].lower())
                and clave == u["password"]
            ):
                print(f"\n[Acceso concedido] Bienvenido/a, {u['nombre']} ({u['rol']}).")
                return u

        intentos_fallidos += 1
        restantes = 3 - intentos_fallidos
        if restantes > 0:
            print(f"[Acceso denegado] Credenciales incorrectas. Intentos restantes: {restantes}.")
        else:
            print(
                f"\n[BLOQUEO TEMPORAL] Ha superado el máximo de 3 intentos fallidos. "
                f"El sistema permanecerá bloqueado durante {SEGUNDOS_BLOQUEO} segundos..."
            )
            for seg in range(SEGUNDOS_BLOQUEO, 0, -1):
                print(f"  Tiempo restante de bloqueo: {seg:02d}s", end="\r")
                time.sleep(1)
            print(" " * 45, end="\r")
            intentos_fallidos = 0


def registrar_pqrs(usuario_activo: dict) -> None:
    print("\n--- 1. REGISTRAR PQRS ---")
    nombre_completo = solicitar_validado("Nombre completo: ", validar_nombre)
    tipo_documento = solicitar_validado(
        "Tipo de documento (CC, TI, CE, PP, NIT): ", validar_tipo_documento
    )
    numero_documento = solicitar_validado("Número de documento: ", validar_numero_documento)
    tipo_telefono = solicitar_validado(
        "Tipo de teléfono (Celular, Fijo, Corporativo, Otro): ", validar_tipo_telefono
    )
    telefono_contacto = solicitar_validado("Teléfono de contacto (10 dígitos): ", validar_telefono)
    correo_electronico = solicitar_validado("Correo electrónico: ", validar_correo)
    perfil_solicitante = solicitar_validado(
        "Perfil del solicitante (Estudiante, Docente, Administrativo, Ciudadano): ",
        validar_perfil_solicitante,
    )
    direccion = solicitar_validado("Dirección (opcional, Enter para N/A): ", validar_direccion)

    tipo_solicitud = solicitar_validado(
        "Tipo de solicitud (Petición, Queja, Reclamo, Sugerencia): ",
        lambda v: validar_opcion_lista(v, TIPOS_SOLICITUD, "Tipo de solicitud"),
    )
    fecha_rad_dt = solicitar_validado(
        "Fecha de radicación (AAAA-MM-DD HH:MM:SS o AAAA-MM-DD, Enter para actual): ",
        lambda v: validar_fecha_radicacion(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S") if not v.strip() else v
        ),
    )
    canal_recepcion = solicitar_validado(
        "Canal de recepción (Presencial, Correo electrónico, Página web, Teléfono, Redes sociales, Otro): ",
        lambda v: validar_opcion_lista(v, CANALES_RECEPCION, "Canal de recepción"),
    )
    asunto_titulo = solicitar_validado("Asunto o título (5-150 caracteres): ", validar_asunto)
    descripcion_detallada = solicitar_validado(
        "Descripción detallada (20-2000 caracteres): ", validar_descripcion
    )
    tipo_mascota = solicitar_validado(
        "Tipo de mascota (Perro, Gato, Otro): ",
        lambda v: validar_opcion_lista(v, TIPOS_MASCOTA, "Tipo de mascota"),
    )

    campus_ordenados = sorted(CAMPUS_UDEA)
    print("Campus UdeA disponibles:")
    for idx, c in enumerate(campus_ordenados, start=1):
        print(f"  {idx}. {c}")

    def _validar_campus(entrada: str) -> tuple[bool, str]:
        if entrada.strip().isdigit():
            indice = int(entrada.strip()) - 1
            if 0 <= indice < len(campus_ordenados):
                return True, campus_ordenados[indice]
        return validar_opcion_lista(entrada, CAMPUS_UDEA, "Campus relacionado")

    campus_relacionado = solicitar_validado(
        "Seleccione el número o escriba el nombre del campus: ", _validar_campus
    )
    fecha_max_dt = calcular_fecha_maxima(fecha_rad_dt)

    registro = {
        "nombre_completo": nombre_completo,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "tipo_telefono": tipo_telefono,
        "telefono_contacto": telefono_contacto,
        "correo_electronico": correo_electronico,
        "perfil_solicitante": perfil_solicitante,
        "direccion": direccion,
        "tipo_solicitud": tipo_solicitud,
        "fecha_radicacion": fecha_rad_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "canal_recepcion": canal_recepcion,
        "asunto_titulo": asunto_titulo,
        "descripcion_detallada": descripcion_detallada,
        "tipo_mascota": tipo_mascota,
        "campus_relacionado": campus_relacionado,
        "fecha_maxima_respuesta": fecha_max_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "estado_peticion": "Registrada",
        "usuario_registro": usuario_activo["usuario"],
        "fecha_solucion": "",
    }

    guardado = agregar_registro(registro)
    ruta_radicado = guardar_radicado_txt(guardado)
    print("\n[Éxito] PQRS registrada correctamente.")
    print(f"Archivo de comprobante ASCII (120 columnas) guardado en: {ruta_radicado}\n")
    print(generar_comprobante_ascii(guardado))


def consultar_pqrs() -> None:
    print("\n--- 2. CONSULTAR PQRS ---")
    registros = obtener_todos_los_registros()
    if not registros:
        print("No existen PQRS registradas en el sistema.")
        return

    for r in registros:
        print(
            f"[{r['tipo_solicitud']} | ID {int(r['id']):05d}] "
            f"Solicitante: {r['nombre_completo']} | Estado: {r['estado_peticion']} | "
            f"Mascota: {r['tipo_mascota']} | Vence: {r['fecha_maxima_respuesta']}"
        )

    ver = input("\n¿Desea visualizar el comprobante ASCII de algún registro? (s/n): ").strip().lower()
    if ver == "s":
        tipo = solicitar_validado(
            "Tipo de solicitud (Petición, Queja, Reclamo, Sugerencia): ",
            lambda v: validar_opcion_lista(v, TIPOS_SOLICITUD, "Tipo de solicitud"),
        )
        try:
            id_buscado = int(input("Ingrese el ID numérico del radicado: ").strip())
        except ValueError:
            print("ID inválido.")
            return
        encontrado = next(
            (r for r in leer_registros_archivo(ARCHIVOS_POR_TIPO[tipo]) if int(r["id"]) == id_buscado),
            None,
        )
        if not encontrado:
            print("No se encontró ninguna PQRS con ese tipo e ID.")
        else:
            print("\n" + generar_comprobante_ascii(encontrado))


def registrar_cambio_pqrs() -> None:
    print("\n--- 3. REGISTRAR CAMBIO EN PQRS ---")
    tipo = solicitar_validado(
        "Tipo de solicitud (Petición, Queja, Reclamo, Sugerencia): ",
        lambda v: validar_opcion_lista(v, TIPOS_SOLICITUD, "Tipo de solicitud"),
    )
    try:
        id_buscado = int(input("Ingrese el ID numérico de la PQRS a actualizar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    registros = leer_registros_archivo(ARCHIVOS_POR_TIPO[tipo])
    actual = next((r for r in registros if int(r["id"]) == id_buscado), None)
    if not actual:
        print("Registro no encontrado.")
        return

    print(f"Estado actual: {actual['estado_peticion']} (Flujo permitido: {' -> '.join(ESTADOS_VALIDOS)})")
    nuevo_estado = input("Ingrese el nuevo estado (En proceso / Solucionada): ").strip()
    ok, resultado = validar_transicion_estado(actual["estado_peticion"], nuevo_estado)
    if not ok:
        print(f"[Error] {resultado}")
        return

    cambios = {"estado_peticion": resultado}
    if resultado == "Solucionada":
        cambios["fecha_solucion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if actualizar_registro(tipo, id_buscado, cambios):
        actualizado = {**actual, **cambios}
        guardar_radicado_txt(actualizado)
        print(f"[Éxito] Estado actualizado a '{resultado}' y comprobante regenerado.")


def mostrar_estadisticas() -> None:
    print("\n--- 4. ESTADÍSTICAS Y GRÁFICOS ---")
    stats = generar_estadisticas()
    print(f"Total de PQRS registradas: {stats['total_registros']}")
    print(f"Promedio de días de respuesta (entero obligatorio): {stats['promedio_dias_respuesta_entero']} días")
    print(f"Por tipo de solicitud: {stats['por_tipo_solicitud']}")
    print(f"Por tipo de documento: {stats['por_tipo_documento']}")
    print(f"Por perfil del solicitante: {stats['por_perfil_solicitante']}")
    print(f"Por tipo de mascota: {stats['por_mascota']}")
    print(f"Por canal de recepción: {stats['por_canal']}")
    print(f"Por campus UdeA: {stats['por_campus']}")
    print(f"Por estado: {stats['por_estado']}")
    print(f"Por usuario registrador: {stats['por_usuario_registro']}")
    print(f"Efectividad de resolución: {stats['porcentaje_resolucion']}%")
    print(f"Documentos más antiguos mostrados: {len(stats['documentos_mas_antiguos'])}")
    print(f"Próximos a vencer (<=5 días): {len(stats['por_vencer'])} | Vencidos: {len(stats['vencidos'])}")

    exportar = input("\n¿Exportar resumen estadístico a archivo plano TXT? (s/n): ").strip().lower()
    if exportar == "s":
        ruta = exportar_reporte_txt()
        print(f"[Éxito] Reporte exportado en: {ruta}")

    graficar = input("¿Generar gráficos estadísticos en la carpeta images/? (s/n): ").strip().lower()
    if graficar == "s":
        try:
            rutas_img = generar_graficos()
            print("[Éxito] Gráficos generados:")
            for r in rutas_img:
                print(f"  - {r}")
        except RuntimeError as err:
            print(f"[Aviso] {err}")


def menu_principal(usuario_activo: dict) -> None:
    while True:
        print("\n" + "=" * 60)
        print(f"  {NOMBRE_SISTEMA}")
        print(f"  Usuario activo: {usuario_activo['usuario']} | Rol: {usuario_activo['rol']}")
        print("=" * 60)
        print("1. Registrar PQRS")
        print("2. Consultar PQRS")
        print("3. Registrar Cambio en PQRS")
        print("4. Estadísticas")
        print("5. Salir")

        opcion = input("Seleccione una opción (1-5): ").strip()
        if opcion == "1":
            registrar_pqrs(usuario_activo)
        elif opcion == "2":
            consultar_pqrs()
        elif opcion == "3":
            registrar_cambio_pqrs()
        elif opcion == "4":
            mostrar_estadisticas()
        elif opcion == "5":
            print("Sesión finalizada. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Por favor seleccione un número entre 1 y 5.")


class c_main:
    """Clase coordinadora, principal y ejecutable de la aplicación de consola."""
    autenticar = staticmethod(autenticar_usuario)
    registrar = staticmethod(registrar_pqrs)
    consultar = staticmethod(consultar_pqrs)
    actualizar = staticmethod(registrar_cambio_pqrs)
    estadisticas = staticmethod(mostrar_estadisticas)
    menu = staticmethod(menu_principal)


aplicacion = c_main()

if __name__ == "__main__":
    asegurar_archivos()
    sesion = autenticar_usuario()
    if sesion:
        menu_principal(sesion)
