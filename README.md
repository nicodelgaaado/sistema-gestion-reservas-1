# Sistema de Gestion de Reservas de Laboratorios

Aplicacion web desarrollada con Django para administrar reservas de laboratorios academicos. El sistema contempla autenticacion, gestion por roles, validaciones de conflicto horario, cambio de estados, filtrado de reservas y exportacion a CSV.

## Objetivo

Centralizar el flujo de solicitudes de reserva de laboratorio para dos perfiles principales:

- `Docente`: crea, consulta, edita y elimina sus propias reservas mientras esten en estado pendiente.
- `Administrador`: visualiza todas las reservas y actualiza su estado a aprobada o rechazada.

## Caracteristicas principales

- Inicio con `home/index` que centraliza accesos y resume el estado del sistema.
- Inicio y cierre de sesion con vistas basadas en autenticacion de Django.
- Creacion de reservas con formulario validado.
- Edicion y eliminacion restringidas a reservas pendientes y al autor de la reserva.
- Cambio de estado de reservas para administradores.
- Filtros por fecha y laboratorio.
- Resumen visual con conteos por estado y por laboratorio.
- Exportacion de reservas a archivo CSV.
- Creacion automatica de grupos `Docente` y `Administrador` despues de migraciones.
- Comando de gestion para generar usuarios demo.
- Interfaz visual renovada con layout responsive y navegacion global.

## Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML con Django Templates
- CSS personalizado

## Estructura general del proyecto

```text
sistema-gestion-reservas-1/
├── manage.py
├── README.md
├── css/
│   └── styles.css
├── gestion_reservas_admin/
│   ├── db.sqlite3
│   └── gestion_reservas_admin/
│       ├── settings.py
│       ├── urls.py
│       ├── asgi.py
│       └── wsgi.py
├── reservas_admin/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── management/
│       └── commands/
│           └── crear_usuarios_demo.py
└── templates/
    ├── base.html
    ├── home.html
    ├── registration/
    │   └── login.html
    └── reservas_admin/
        ├── reserva_list.html
        ├── reserva_form.html
        ├── reserva_estado_form.html
        └── reserva_confirm_delete.html
```

## Modelo de datos

La entidad principal es `Reserva`, definida en [reservas_admin/models.py](reservas_admin/models.py).

### Campos del modelo `Reserva`

- `usuario`: usuario que crea la reserva.
- `laboratorio`: nombre del laboratorio.
- `fecha`: dia de la reserva.
- `hora_inicio`: hora inicial.
- `hora_fin`: hora final.
- `estado`: `pendiente`, `aprobada` o `rechazada`.
- `motivo`: descripcion de la solicitud.
- `fecha_creacion`: fecha y hora de registro.

### Reglas de negocio implementadas

- La hora de inicio debe ser menor que la hora de fin.
- No puede existir conflicto de horario en el mismo laboratorio y misma fecha.
- Las reservas rechazadas no bloquean horarios.
- Solo una reserva pendiente puede ser editada o eliminada por su creador.

## Roles y permisos

### Docente

- Puede iniciar sesion.
- Puede ver unicamente sus propias reservas.
- Puede crear reservas nuevas.
- Puede editar o eliminar sus reservas si siguen en estado `pendiente`.

### Administrador

- Puede iniciar sesion.
- Puede ver todas las reservas del sistema.
- Puede cambiar el estado de cualquier reserva.
- Puede usar el panel como backoffice de seguimiento.

## Rutas principales

Las rutas estan definidas en [reservas_admin/urls.py](reservas_admin/urls.py).

| Ruta | Nombre | Descripcion |
|---|---|---|
| `/` | `inicio` | Pagina principal con resumen e indice del sistema |
| `/login/` | `login` | Inicio de sesion |
| `/logout/` | `logout` | Cierre de sesion |
| `/reservas/` | `reserva_lista` | Listado de reservas |
| `/reservas/nueva/` | `reserva_crear` | Crear reserva |
| `/reservas/<id>/editar/` | `reserva_editar` | Editar reserva |
| `/reservas/<id>/eliminar/` | `reserva_eliminar` | Eliminar reserva |
| `/reservas/<id>/estado/` | `reserva_estado` | Cambiar estado de reserva |
| `/reservas/exportar/csv/` | `reserva_exportar_csv` | Exportar reservas filtradas a CSV |

## Vistas implementadas

Definidas en [reservas_admin/views.py](reservas_admin/views.py).

- `InicioView`: muestra el `home` con metricas generales.
- `InicioSesionView`: autentica usuarios.
- `CierreSesionView`: cierra la sesion.
- `ReservaListView`: lista reservas y construye estadisticas de apoyo.
- `ReservaCreateView`: crea reservas asociandolas al usuario autenticado.
- `ReservaUpdateView`: actualiza reservas bajo restricciones de negocio.
- `ReservaDeleteView`: elimina reservas pendientes del usuario autor.
- `CambiarEstadoReservaView`: permite aprobar o rechazar reservas.
- `ExportarReservasCSVView`: exporta reservas visibles a CSV.

## Formularios

Definidos en [reservas_admin/forms.py](reservas_admin/forms.py).

- `ReservaForm`: formulario principal de creacion y edicion.
- `EstadoReservaForm`: formulario corto para cambio de estado.
- `FiltroReservaForm`: filtra por fecha y laboratorio.

El proyecto usa widgets HTML5 para fecha y hora:

- `DateInput`
- `TimeInput`

## Interfaz

La interfaz usa plantillas Django y una hoja de estilos central en [css/styles.css](css/styles.css).

### Plantillas principales

- [templates/base.html](templates/base.html): layout global y navegacion.
- [templates/home.html](templates/home.html): pagina de inicio e indice del sistema.
- [templates/registration/login.html](templates/registration/login.html): acceso al sistema.
- [templates/reservas_admin/reserva_list.html](templates/reservas_admin/reserva_list.html): panel de reservas.
- [templates/reservas_admin/reserva_form.html](templates/reservas_admin/reserva_form.html): formulario de reserva.
- [templates/reservas_admin/reserva_estado_form.html](templates/reservas_admin/reserva_estado_form.html): actualizacion de estado.
- [templates/reservas_admin/reserva_confirm_delete.html](templates/reservas_admin/reserva_confirm_delete.html): confirmacion de eliminacion.

## Configuracion local

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd sistema-gestion-reservas-1
```

### 2. Crear y activar un entorno virtual

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar Django

Si no tienes un archivo `requirements.txt`, puedes instalar Django manualmente:

```bash
pip install django
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear usuarios demo

El proyecto incluye el comando:

```bash
python manage.py crear_usuarios_demo
```

Este comando crea:

- `docente_demo` / `Docente123.`
- `admin_demo` / `Admin123.`

### 6. Levantar el servidor

```bash
python manage.py runserver
```

Tambien puedes indicar un puerto especifico:

```bash
python manage.py runserver 127.0.0.1:8001
```

## Usuarios y credenciales existentes

Al momento de esta documentacion, la base local contiene estos usuarios:

### Docente

- Usuario: `docente_demo`
- Contrasena: `Docente123.`
- Grupo: `Docente`
- `is_staff`: `False`
- `is_superuser`: `False`

### Administrador del sistema

- Usuario: `admin_demo`
- Contrasena: `Admin123.`
- Grupo: `Administrador`
- `is_staff`: `True`
- `is_superuser`: `False`

### Nota importante sobre `/admin/`

`admin_demo` es un usuario administrador funcional dentro del sistema de reservas y tiene acceso de tipo `staff`, pero no es un superusuario de Django.

Si se necesita acceso total al panel nativo de Django en `/admin/`, se debe crear un superusuario con:

```bash
python manage.py createsuperuser
```

## Señales y configuracion automatica

En [reservas_admin/signals.py](reservas_admin/signals.py) se usa `post_migrate` para crear automaticamente los grupos:

- `Docente`
- `Administrador`

Esto evita tener que crear esos roles manualmente en cada base de datos nueva.

## Panel administrativo de Django

En [reservas_admin/admin.py](reservas_admin/admin.py), el modelo `Reserva` esta registrado con:

- `list_display`
- `list_filter`
- `search_fields`

Esto permite gestionar reservas desde `/admin/` si se crea un superusuario.

## Exportacion a CSV

El sistema permite exportar el conjunto visible de reservas desde:

```text
/reservas/exportar/csv/
```

La exportacion incluye:

- Usuario
- Laboratorio
- Fecha
- Hora inicio
- Hora fin
- Estado
- Motivo

## Pruebas

Existen pruebas automatizadas en [reservas_admin/tests.py](reservas_admin/tests.py).

Actualmente se validan al menos estos escenarios:

- deteccion de conflicto horario en el modelo
- creacion exitosa de una reserva por parte de un docente

Ejecutar pruebas:

```bash
python manage.py test
```

## Comandos utiles

### Crear superusuario

```bash
python manage.py createsuperuser
```

### Verificar configuracion del proyecto

```bash
python manage.py check
```

### Crear usuarios demo

```bash
python manage.py crear_usuarios_demo
```

## Estado actual del proyecto

El sistema ya cuenta con:

- backend funcional con reglas de negocio
- autenticacion con roles
- panel de reservas con filtros y exportacion
- interfaz visual mejorada
- pagina de inicio con indice de navegacion
- pruebas basicas automatizadas

## Posibles mejoras futuras

- agregar `requirements.txt`
- internacionalizar mensajes y textos del sistema
- incorporar paginacion en el listado de reservas
- agregar auditoria de cambios por reserva
- mejorar cobertura de pruebas
- separar configuraciones por entorno
- añadir despliegue y documentacion de produccion

## Autor y contexto academico

Este proyecto corresponde a un sistema de gestion de reservas de laboratorios orientado a contexto academico y puede ser usado como base para practicas, entregas o ampliaciones de un proyecto universitario.
