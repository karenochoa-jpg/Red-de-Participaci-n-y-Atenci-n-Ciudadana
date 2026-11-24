# Manual de Usuario — HuellaActiva UdeA (Gestor de PQRS)

## 1. Introducción
**HuellaActiva UdeA** es una aplicación de consola en Python diseñada para registrar, consultar, actualizar y analizar las PQRS (Peticiones, Quejas, Reclamos y Sugerencias) relacionadas con la atención de perros, gatos y otros animales en la Universidad de Antioquia.

---

## 2. Requisitos del Sistema
* **Sistema operativo:** Windows, Linux o macOS.
* **Intérprete:** Python 3.10 o superior.
* **Librería adicional para gráficos:** `matplotlib` (`pip install matplotlib`).

---

## 3. Ejecución del Programa
Abra una terminal en la carpeta raíz del proyecto y ejecute:

```bash
python src/main.py
```

---

## 4. Guía Paso a Paso

### 4.1. Inicio de Sesión (Login)
Al iniciar el programa se solicitarán sus credenciales autorizadas (registradas en `data/usuarios.txt`):
1. Ingrese su **Usuario** o **Correo institucional** (ejemplo: `admin_udea` o `kelly.martinez`).
2. Ingrese su **Clave** (ejemplo: `Udea2026*` o `Kelly2026*`).

> **Control de seguridad:** Si ingresa credenciales incorrectas **3 veces consecutivas**, el sistema bloqueará temporalmente el acceso durante **15 segundos** mostrando un contador regresivo en pantalla.

---

### 4.2. Menú Principal
Una vez autenticado, visualizará las siguientes 5 opciones:
1. **Registrar PQRS**
2. **Consultar PQRS**
3. **Registrar Cambio en PQRS**
4. **Estadísticas**
5. **Salir**

---

### 4.3. Opción 1: Registrar PQRS
El sistema solicitará y validará uno a uno los siguientes datos:

#### Datos del Solicitante
* **Nombre completo:** Obligatorio, entre 3 y 100 caracteres (solo letras, tildes, espacios, apóstrofes o guiones; sin números).
* **Tipo de documento:** Obligatorio (`CC`, `TI`, `CE`, `PP`, `NIT`).
* **Número de documento:** Obligatorio, entre 3 y 15 dígitos numéricos.
* **Tipo de teléfono:** Obligatorio (`Celular`, `Fijo`, `Corporativo`, `Otro`).
* **Teléfono de contacto:** Obligatorio, exactamente 10 dígitos numéricos.
* **Correo electrónico:** Obligatorio, formato válido `correo@dominio.com` (máx. 254 caracteres).
* **Perfil del solicitante:** Obligatorio: `Estudiante`, `Docente`, `Administrativo` o `Ciudadano`.
* **Dirección:** Opcional (entre 5 y 200 caracteres). Si se deja vacío, el sistema registra automáticamente `N/A`.

#### Información de la PQRS e Información Relacionada
* **Tipo de solicitud:** `Petición`, `Queja`, `Reclamo` o `Sugerencia`. Determina en qué archivo plano (`data/Peticion.txt`, `data/Queja.txt`, `data/Reclamo.txt` o `data/Sugerencia.txt`) se almacenará el registro con su propio ID consecutivo.
* **Fecha de radicación:** Formato `AAAA-MM-DD HH:MM:SS` o `AAAA-MM-DD` (si presiona `Enter`, toma la fecha y hora actual). No permite fechas futuras.
* **Canal de recepción:** `Presencial`, `Correo electrónico`, `Página web`, `Teléfono`, `Redes sociales` u `Otro`.
* **Asunto o título:** Obligatorio, entre 5 y 150 caracteres.
* **Descripción detallada:** Obligatorio, entre 20 y 2000 caracteres.
* **Tipo de mascota:** `Perro`, `Gato` u `Otro`.
* **Campus relacionado:** Selección por número o nombre entre los 9 campus oficiales de la Universidad de Antioquia.

#### Resultado del Registro
* El sistema calcula automáticamente la **Fecha máxima de respuesta** sumando **30 días calendario** a la fecha de radicación.
* Asigna el estado inicial `Registrada` y vincula al usuario activo en la sesión.
* Muestra en consola y guarda en `data/radicados/` un **comprobante ASCII de exactamente 120 caracteres por línea**.

---

### 4.4. Opción 2: Consultar PQRS
* Lista todas las PQRS registradas en los cuatro archivos planos mostrando tipo, ID, solicitante, estado, mascota y fecha máxima de respuesta.
* Permite ingresar el tipo de solicitud y el ID para imprimir en pantalla su **comprobante ASCII de 120 columnas**.

---

### 4.5. Opción 3: Registrar Cambio en PQRS
Permite actualizar el estado de una solicitud ingresando su **Tipo de solicitud** e **ID numérico**.
* El sistema exige cumplir estrictamente el flujo secuencial:
  `Registrada -> En proceso -> Solucionada`
* Cuando pasa a `Solucionada`, se guarda automáticamente la `fecha_solucion` para calcular el indicador de días de respuesta.

---

### 4.6. Opción 4: Estadísticas
Calcula y muestra en consola:
* **Promedio de días de respuesta en valor entero** (indicador obligatorio).
* Cantidad total de registros y distribución por tipo de solicitud, tipo de documento, tipo de mascota (`Perro`, `Gato`, `Otro`), canal, campus, estado, perfil del solicitante y usuario registrador; también calcula porcentaje de resolución.
* Listado de documentos más antiguos y conteo de PQRS próximas a vencer (<= 5 días) o vencidas.
* Permite exportar el resumen a `data/reporte_estadisticas.txt` y generar siete gráficos estadísticos `.png` en `images/`.

---

### 4.7. Opción 5: Salir
Cierra la sesión activa y finaliza la ejecución de manera segura.


