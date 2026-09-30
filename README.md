# SOCIAP-SISTEMA-DE-ORIENTACIÓN-CIUDADANA-Y-ATENCIÓN-A-PERSONAS
Plataforma web para la gestión de solicitudes, peticiones y quejas ciudadanas
## 1 Integrantes:
**Karen Darian Ochoa Pertuz**- *Ingenieria Industrial*

**Kelly Ester Martínez Cuadrado**-*Ingenieria Industrial*

**Angela Maria Calle Loaiza**- *Ingeniería Industrial*

**Leidy Camila Torres Henao**- *Ingenieria Industrial*

## 2 Vínculos académicos y descripción 
**Karen Darian Ochoa Pertuz** |*Ingenieria Industrial* |Habilidades y Fortalezas:Lógica y razonamiento, creatividad para resolver problemas, comunicación clara y visión integral de proyectos.

**Kelly Ester Martinez Cuadrado** |*Ingenieria Industrial* |Habilidades y Fortalezas:Gran capacidad de organización, escucha activa, trabajo en equipo y atención al detalle.

**Angela Maria Calle Loaiza** |*Ingeniería Industrial* |Habilidades y Fortalezas: Pensamiento creativo, adaptabilidad al cambio, liderazgo cercano y facilidad para sintetizar información.

**Leidy Camila Torres Henao** |*Ingenieria Industrial* |Habilidades y Fortalezas: Comunicación efectiva, proactividad, pensamiento crítico y coordinación de tareas.

## 3. Nombre del proyecto y detalles.
**Nombre Oficial** SOCIAP (Sistema de Orientación Ciudadana y Atención a Personas)
**Descripción:** El presente proyecto implementa una aplicación en consola desarrollada en Python orientada a automatizar, validar y procesar eficientemente las Peticiones, Quejas, Reclamos y Sugerencias (PQRS). Su propósito principal es optimizar los tiempos de respuesta legales, garantizar la trazabilidad total de los requerimientos de los usuarios y administrar de forma segura los datos de un hospital veterinario o red institucional.
**Imagen del Proyecto** (Imagen proyecto)

## 4. Licencia  del software
Este proyecto está dedicado al dominio público mediante la licencia **Creative Commons CC0 1.0 Universal (CC0 1.0) Dedicación de Dominio Público**

## 5. Reporte de visión 

### 5.1 Descripción General 
SOCIAP es un software enfocado en centralizar, canalizar y agilizar los trámites, peticiones, quejas y solicitudes de la ciudadanía. La solución busca optimizar los procesos de atención pública, garantizando el cumplimiento de los tiempos de respuesta legales y la protección de datos personales.

### 5.2 Objetivos
***Objetivos Generales*** Desarrollar una plataforma web integral que optimice la atención trazabilidad y gestión de solicitudes ciudadanas

***Objetivos Específicos***
1.	Reducir los tiempos de respuesta a los requerimientos ciudadanos según los marcos legales vigentes
2.  Asegurar la integridad y confidencialidad de la información registrada por los usuarios
3.  Implementar un sistema de seguimiento transparente donde los usuarios puedan verificar el estado de su trámite en tiempo real

**5.3 Beneficios**

***Para los Usuarios*** Proceso accesible, transparente y con visibilidad completa del estado de sus trámites.

***Para la Organización*** Automatización de flujos de trabajo, control centralizado de datos y generación de métricas sobre la eficiencia operativa.

## 6 Especificaciones de requisitos

### Requisitos funcionales

**1. registro de Solicitudes**  Permitir a los ciudadanos registrar peticiones, quejas o reclamos adjuntando datos clave.

**2. asignación de Casos**  Derivar automáticamente cada solicitud al área competente para su gestión. 

**3. trazabilidad en Tiempo Real**  Permitir la consulta del estado de la solicitud mediante un número de radicado o código único. 

**4. notificaciones**  Enviar alertas automáticas por correo electrónico sobre actualizaciones en el caso.

**5. reportes de Gestión** Generar informes analíticos periódicos sobre el volumen de atención y tiempos de respuesta.

### Requisitos No Funcionales

**1. seguridad** Encriptación de contraseñas y cumplimiento de normas sobre protección de datos personales. 

**2. rendimiento** Consultas de estado y tiempos de carga de la interfaz en menos de 2 segundos. 

**3. usabilidad** Diseño intuitivo y accesible, adaptable a dispositivos móviles y escritorios.

**4. fiabilidad** Disponibilidad del sistema en un 99% durante el período operacional.

## 7 Plan de proyecto 

### 7.1 Presupuesto del Proyecto (Práctica de Formación)

El presupuesto de este proyecto no se liquida mediante transferencias monetarias directas, sino en **tiempo de práctica de formación profesional**, valorado con base en el **Salario Mínimo Legal Vigente (SMLV)**.

#### Cálculo de Horas Invertidas
* **Número de integrantes:** 4 estudiantes.
* **Horas por integrante:** 50 horas de práctica.
* **Total horas del proyecto:** 4 x 50 = **200 Horas Total**.
* **Valor Hora Práctica (SMLV base 210 hrs/mes):** $1.750.905 / 210 = **$8.338 COP / hora**.

#### Tabla de Valoración Financiera

| Fase / Actividad | Horas Invertidas | Valor Hora Práctica (SMLV) | Subtotal Equivalente |
| :--- | :---: | :---: | :---: |
| Levantamiento y Análisis de Requisitos | 30 h | $8.338 COP | $250.140 COP |
| Diseño de Sistema e Interfaz          | 40 h | $8.338 COP | $333.520 COP |
| Desarrollo e Integración del Software | 90 h | $8.338 COP | $750.420 COP |
| Pruebas (QA), Seguridad y Documentación | 40 h | $8.338 COP | $333.520 COP |
| **TOTAL INVERSIÓN (Práctica Profesional)** | **200 h** | **Valor Práctica** | **$1.667.600 COP** |


### 7.2 Cronograma de Actividades (Diagrama de Gantt)

```mermaid
gantt
    title Cronograma de Trabajo - Proyecto SOCIAP
    dateFormat  YYYY-MM-DD
    section 1. Planificación
    Establecimiento de Requisitos  :a1, 2026-09-30, 7d
    Análisis de Arquitectura      :a2, after a1, 5d
    section 2. Diseño
    Diseño de Interfaz (UI/UX)    :b1, after a2, 7d
    Modelo de Base de Datos      :b2, after a2, 5d
    section 3. Desarrollo
    Módulo de Radicación          :c1, after b1, 10d
    Módulo de Gestión Interna     :c2, after c1, 10d
    section 4. Cierre y Pruebas
    Pruebas QA y Seguridad       :d1, after c2, 6d
    Documentación y Despliegue   :d2, after d1, 5d



