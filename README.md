# Sistema de Gestión de PQRS — HuellaActiva UdeA

!\[Logo del Proyecto HuellaActiva UdeA](images/logo\_proyecto.png)

## 1\. Integrantes

Proyecto integrador desarrollado para el curso **Algoritmia y Programación** de la **Facultad de Ingeniería — Departamento de Ingeniería Industrial** de la **Universidad de Antioquia**:

* **Kelly Ester Martínez Cuadrado**
* **Angela Maria Calle Loaiza**
* **Leidy Camila Torres Henao**
* **Karen Darian Ochoa Pertuz**

\---

## 2\. Vínculos académicos y descripción

Todas las integrantes pertenecen al programa de **Ingeniería Industrial (Modalidad Virtual)** de la **Universidad de Antioquia**:

* **Kelly Ester Martínez Cuadrado:** Desarrollo de algoritmos en Python, diseño modular, implementación de validaciones con expresiones regulares, gestión de archivos planos y arquitectura del repositorio.
* **Angela Maria Calle Loaiza:** Levantamiento y análisis de requisitos funcionales/no funcionales, estructuración de flujos operativos y control de calidad documental.
* **Leidy Camila Torres Henao:** Gestión de cronograma, documentación del manual de usuario, validación de casos de prueba y seguimiento de entregas.
* **Karen Darian Ochoa Pertuz:** Diseño de reportes estadísticos, generación de visualizaciones gráficas en Python, control de indicadores y apoyo en diseño visual.

\---

## 3\. Nombre del proyecto y detalles

**Nombre del software:** **HuellaActiva UdeA** *(renovación de identidad del nombre temporal MEPEGA)*.

**Descripción:** Aplicación de consola desarrollada en Python que permite autenticar administradores/operadores y gestionar el ciclo de vida completo de las Peticiones, Quejas, Reclamos y Sugerencias (PQRS) relacionadas con la atención veterinaria y el bienestar de perros, gatos y otros animales en los campus de la Universidad de Antioquia. La información se persiste de manera independiente en cuatro archivos planos (`Peticion.txt`, `Queja.txt`, `Reclamo.txt`, `Sugerencia.txt`), emite comprobantes de radicación en formato ASCII de **120 caracteres exactos de ancho**, calcula estadísticas descriptivas (incluyendo el promedio entero de días de respuesta) y genera siete gráficos estadísticos en formato PNG.

\---

## 4\. Licencia del software

Este proyecto se distribuye bajo la licencia **Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0)**, seleccionada mediante el asistente oficial [Creative Commons License Chooser](https://chooser-beta.creativecommons.org/).

* **Permisos:** Compartir (copiar y redistribuir el material en cualquier medio o formato) y adaptar (remezclar, transformar y construir a partir del material) con fines académicos.
* **Condiciones:** Reconocer adecuadamente la autoría del equipo de trabajo de la Universidad de Antioquia y no utilizar el software con fines comerciales.

\---

## 5\. Reporte de visión

### Descripción general

**HuellaActiva UdeA** digitaliza y estandariza la recepción, radicación, seguimiento y análisis de las PQRS recibidas por el colectivo estudiantil de apoyo a perros y gatos de la Universidad de Antioquia, sustituyendo el registro manual en papel por una solución estructurada, trazable y auditable en archivos planos.

### Objetivos

* **Centralizar y clasificar** cada solicitud en archivos planos independientes según su tipo (`Petición`, `Queja`, `Reclamo`, `Sugerencia`), manteniendo secuencias de identificación auto-incrementales propias por archivo.
* **Asegurar la calidad de los datos** mediante validaciones rigurosas en los datos del solicitante, información de la PQRS, fechas, campus universitarios y flujo de estados.
* **Emitir comprobantes estandarizados** en texto plano con marco ASCII de exactamente 120 columnas horizontales.
* **Facilitar el control de tiempos y la toma de decisiones** mediante el cálculo automático de fecha máxima de respuesta (+30 días calendario), alertas de vencimiento, reportes exportables en `.txt` y gráficos estadísticos.

### Beneficios

* Elimina la duplicidad de radicados y los errores frecuentes de captura manual.
* Garantiza trazabilidad al vincular automáticamente al usuario autenticado con cada registro creado.
* Permite identificar rápidamente solicitudes próximas a vencer o vencidas, así como los campus y canales con mayor demanda.

\---

## 6\. Especificación de requisitos

### Requisitos funcionales

* **RF-01 Control de acceso (Login):** Validar usuario o correo institucional y contraseña contra `data/usuarios.txt` antes de acceder al menú principal. Tras 3 intentos fallidos, bloquear la pantalla temporalmente mostrando el tiempo restante.
* **RF-02 Gestión de sesión:** Almacenar los datos del usuario autenticado para asociarlos automáticamente al campo `usuario\_registro` de cada PQRS.
* **RF-03 Secuencia auto-incremental independiente:** Generar un `id` entero consecutivo comenzando en `1` de forma independiente para cada uno de los 4 archivos planos.
* **RF-04 Validación integral de campos:** Validar longitud, formato y obligatoriedad de nombre completo, tipo y número de documento, tipo y teléfono de contacto (10 dígitos), correo electrónico, perfil del solicitante (Estudiante, Docente, Administrativo o Ciudadano), dirección opcional (`N/A` si se omite), tipo de solicitud, fecha de radicación (no futura), canal, asunto, descripción, tipo de mascota y campus UdeA.
* **RF-05 Almacenamiento en archivos planos:** Guardar y actualizar registros en `data/Peticion.txt`, `data/Queja.txt`, `data/Reclamo.txt` y `data/Sugerencia.txt` bajo una estructura homogénea.
* **RF-06 Impresión de radicado ASCII (120 caracteres):** Generar en pantalla y en archivo `.txt` un comprobante delimitado por marco ASCII donde cada línea tenga exactamente 120 caracteres, excluyendo la descripción detallada y mostrando `N/A` cuando no haya dirección.
* **RF-07 Consulta de PQRS:** Listar las PQRS registradas y permitir visualizar el comprobante ASCII de cualquier radicado específico.
* **RF-08 Actualización controlada de estado:** Permitir cambiar el estado respetando estrictamente la secuencia `Registrada -> En proceso -> Solucionada` y registrando la fecha de solución al finalizar.
* **RF-09 Estadísticas, exportación y gráficos:** Calcular primero el promedio entero de días reales de respuesta; distribuir PQRS por tipo de mascota, canal, campus, estado, perfil del solicitante y funcionario registrador; calcular porcentaje de resolución, antigüedad y alertas de vencimiento; exportar TXT y CSV y generar gráficos `.png`.

### Requisitos no funcionales

* **RNF-01 Usabilidad:** Interfaz de consola organizada, clara y con retroalimentación inmediata ante errores de digitación.
* **RNF-02 Modularidad y mantenibilidad:** Separación clara de responsabilidades en `src/validaciones.py`, `src/archivos.py`, `src/reportes.py` y `src/main.py`.
* **RNF-03 Integridad y persistencia:** Almacenamiento en codificación `UTF-8` sin pérdida de registros entre ejecuciones.
* **RNF-04 Seguridad básica:** Restricción de acceso mediante credenciales y bloqueo temporal ante fuerza bruta (3 intentos).
* **RNF-05 Portabilidad:** Compatible con Python 3.10+ en Windows, Linux y macOS usando rutas relativas (`pathlib`).

\---

## 7\. Plan de proyecto

### Actividades y Cronograma (Diagrama de Gantt)

|ID|Actividad|Sem 5-6|Sem 7-8|Sem 9 (Ent. 1)|Sem 10-12|Sem 13-14|Sem 15-16 (Ent. 2)|
|-|-|:-:|:-:|:-:|:-:|:-:|:-:|
|1|Reunión inicial, actas de entendimiento/colaboración/responsabilidad y logo|██||||||
|2|Configuración del repositorio GitHub y redacción de visión, requisitos y plan|██|██|||||
|3|Desarrollo de `validaciones.py`, `archivos.py` y módulo de Login||██|██||||
|4|Implementación de comprobante ASCII (120 cols), consulta y cambio de estado||||██|||
|5|Desarrollo de `reportes.py`, exportación `.txt` y generación de gráficos|||||██||
|6|Elaboración de `docs/manual\_usuario.md`, pruebas finales y sustentación||||||██|

### Presupuesto del proyecto

Conforme a las directrices del curso, la inversión se contabiliza en horas de práctica formativa del equipo de cuatro (4) integrantes:

* **Dedicación total del equipo:** **50 horas** distribuidas equitativamente entre las cuatro integrantes (12,5 horas por integrante).
* **Valor de referencia:** **1 SMLV** (Salario Mínimo Legal Mensual Vigente en Colombia) correspondiente a remuneración de práctica profesional.
* **Recursos tecnológicos:** $0 COP (Python estándar, biblioteca `matplotlib` y GitHub académico).

\---

## 8\. Plan de versionado

|Versión|Día|Descripción del avance realizado|
|-|-|-|
|`v0.1.0`|Día 1|Creación del repositorio en GitHub con credenciales institucionales UdeA y estructura oficial (`src/`, `docs/`, `images/`, `data/`).|
|`v0.2.0`|Día 8|Formalización de actas de equipo, identidad visual (`HuellaActiva UdeA`) y documentación base en `README.md`.|
|`v0.3.0`|Día 18|Implementación de `src/validaciones.py` con todas las reglas de longitud, formato, fechas y transiciones de estado.|
|`v0.4.0`|Día 26|Implementación de `src/archivos.py` para lectura/escritura independiente de los 4 archivos planos y base de usuarios.|
|`v0.5.0`|Día 35|Desarrollo de `src/main.py` con autenticación (bloqueo tras 3 intentos), registro de PQRS y comprobante ASCII de 120 caracteres.|
|`v0.6.0`|Día 44|Implementación de consulta de radicados y actualización secuencial de estados (`Registrada -> En proceso -> Solucionada`).|
|`v0.7.0`|Día 50|Implementación de `src/reportes.py` con promedio entero de días de respuesta, alertas de vencimiento, exportación `.txt` y gráficos `.png`.|
|`v1.0.0`|Día 56|Redacción de `docs/manual\_usuario.md`, pruebas integrales con datos de ejemplo y cierre listo para sustentación.|

\---

## Estructura del Repositorio y Ejecución

```text
proyecto-pqrs-udea/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py
│   ├── validaciones.py
│   ├── archivos.py
│   └── reportes.py
├── docs/
│   ├── manual\_usuario.md
│   ├── actas\_equipo.md
├── images/
│   ├── logo\_proyecto.png
│   ├── grafico\_mascotas.png
│   ├── grafico\_canales.png
│   ├── grafico\_estados.png
│   ├── grafico\_campus.png
│   └── grafico\_tipos\_solicitud.png
└── data/
    ├── usuarios.txt
    ├── Peticion.txt
    ├── Queja.txt
    ├── Reclamo.txt
    ├── Sugerencia.txt
    ├── reporte\_estadisticas.txt
    └── radicados/
```

### Cómo ejecutar el programa

1. Instalar la dependencia para gráficos (opcional si solo se usan estadísticas en consola):

```bash
   pip install -r requirements.txt
   ```

2. Ejecutar el programa principal desde la raíz del repositorio:

```bash
   python src/main.py
   ```

3. Credenciales de prueba incluidas en `data/usuarios.txt`:

   * **Usuario:** `admin\_udea` (o `admin@udea.edu.co`) | **Clave:** `Udea2026\*`
   * **Usuario:** `kelly.martinez` | **Clave:** `Kelly2026\*`

> Las credenciales incluidas son exclusivamente demostrativas y se almacenan en texto plano por tratarse de un ejercicio académico. Cámbienlas antes de usar datos reales; no carguen contraseñas personales al repositorio público.

### Clases y objetos

Los módulos implementan las clases `c\_validaciones`, `c\_archivos`, `c\_reportes` y `c\_main`, con instancias reutilizables para las reglas de validación, persistencia, análisis y coordinación de la aplicación.

### Visualizaciones gráficas

La aplicación genera siete gráficos estadísticos en formato PNG dentro de la carpeta `images/`. Estos gráficos permiten analizar la distribución de las PQRS por tipo de solicitud, estado, canal de recepción, campus, tipo de mascota, perfil del solicitante y funcionario registrador.

