# Pawly

Repositorio del proyecto **Pawly** (red social de mascotas) de la asignatura
Aplicaciones con Tecnología Internet — UCV.

Contiene el entorno de desarrollo construido en el Laboratorio #9: una aplicación
**Django** con base de datos **SQLite**, desplegada con **Docker Compose** y con el
servidor de aplicación separado del servidor de base de datos.

## Requisitos previos

| Requisito | Versión |
|---|---|
| WSL con Ubuntu | 22.04 LTS |
| Docker Desktop | con integración WSL activada |
| Python | 3.10 |
| Django | 4.2.7 |
| Visual Studio Code | extensiones Python y WSL |

## Estructura del proyecto

```
pawly/
├── .github/
│   ├── actions/docker-repeat/   # Acción propia de GitHub Actions (Docker)
│   └── workflows/               # Workflow de integración continua
├── configPawly/                 # Configuración del proyecto Django
├── PawlyApp/                    # Aplicación: modelos, vistas, rutas, plantillas
├── data/                        # Base de datos SQLite (volumen compartido)
├── Dockerfile                   # Imagen del servidor de aplicación
├── docker-compose.yml           # Orquestación: servidor web + servidor de BD
├── requirements.txt             # Dependencias de Python
└── manage.py
```

## Cómo levantar el entorno con Docker

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
```

La aplicación queda disponible en http://localhost:8000

Para detener los contenedores:

```bash
docker compose down
```

El volumen `bd_data` se conserva entre ejecuciones, por lo que la base de datos no
se pierde al apagar los contenedores.

## Cómo trabajar sin Docker (desarrollo local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Arquitectura

El laboratorio plantea separar el servidor de aplicaciones del servidor de base de
datos para mejorar la seguridad de acceso, optimizar el rendimiento y facilitar las
tareas de TI y desarrollo. Este repositorio implementa esa separación con dos
contenedores:

| Contenedor | Imagen | Rol |
|---|---|---|
| `pawly_web` | construida desde el `Dockerfile` | Servidor de aplicación (Django) |
| `pawly_db` | `alpine:3.21` | Servidor de base de datos: administra el volumen `bd_data` |

Ambos comparten el volumen `bd_data`, donde reside el archivo `db.sqlite3`. El
contenedor web no arranca hasta que el contenedor de base de datos pasa su
`healthcheck`.

Para comprobar que la base de datos reside en el servidor de base de datos:

```bash
docker compose exec db ls -l /data
```

## Política de control de versiones

Ver [docs/POLITICA_DE_VERSIONES.md](docs/POLITICA_DE_VERSIONES.md)

| Rama | Propósito |
|---|---|
| `master` | Código probado y listo para producción |
| `release` | Candidatos de versión para certificación |
| `develop` | Integración de las ramas de funcionalidad |
| `feature/*` | Trabajo por funcionalidad o programador |

## Diseño

Árbol de navegación, modelo de dominio y prototipos de alta fidelidad (Reto 11): ver [docs/diseno/](docs/diseno/README.md)

## Guía de estilo de código

Ver [docs/GUIA_DE_ESTILO.md](docs/GUIA_DE_ESTILO.md)

## Integración continua

El workflow `.github/workflows/action-workflow.yml` se ejecuta en cada `push` e
invoca una acción propia basada en Docker, ubicada en
`.github/actions/docker-repeat`. El resultado se consulta en la pestaña Actions del
repositorio.

## Diferencias respecto al laboratorio

| Punto del laboratorio | Qué se hizo aquí | Motivo |
|---|---|---|
| `docker-compose.yml` con un solo servicio `web` | Dos servicios: `web` y `db` con volumen compartido | Implementar la separación de servidores que describe el propio laboratorio |
| `'NAME': BASE_DIR / 'db.sqlite3'` | `'NAME': BASE_DIR / 'data' / 'db.sqlite3'` | Que la base de datos resida en el volumen compartido |
| `ROM python:3` en el Dockerfile de la acción | `FROM python:3` | Error tipográfico: `ROM` no es una instrucción de Docker |
| `::set-output` para devolver valores | Escritura en `GITHUB_OUTPUT` | GitHub deprecó esa sintaxis |
| `actions/checkout@v1` | `actions/checkout@v4` | La v1 corre sobre una versión de Node retirada de los runners |
| Ubuntu 18.04 en los prerrequisitos | Ubuntu 22.04 LTS | La 18.04 ya no está disponible; las capturas del propio laboratorio son de 22.04 |
| No menciona `.gitignore` ni `.dockerignore` | Se agregaron ambos | Evitar versionar el entorno virtual y reducir el tamaño de la imagen |

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `python3: The term 'python3' is not recognized` | Agregar Python a la ruta del sistema |
| `Python was not found` | Desactivar los alias de ejecución en "Manage App Execution Aliases" |
| `Couldn't import Django` | Activar el entorno virtual con `source .venv/bin/activate` |
| `The command 'docker' could not be found in this WSL 2 distro` | Activar la integración WSL en Docker Desktop |
