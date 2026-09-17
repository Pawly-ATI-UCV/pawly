# Guía de estilo de código

Convenciones que deben seguir los desarrolladores del proyecto Pawly. Se derivan
del código presentado en el Laboratorio #9 y coinciden con las convenciones
habituales de Python y Django.

## Idioma

- El código se escribe en inglés: nombres de clases, funciones, variables y campos de modelo.
- Los comentarios y la documentación se escriben en español.

## Python

| Elemento | Convención | Ejemplo del laboratorio |
|---|---|---|
| Indentación | 4 espacios, nunca tabulaciones | — |
| Clases | `PascalCase` | `class Post(models.Model)` |
| Funciones y métodos | `snake_case` | `def post_list(request)`, `def publish(self)` |
| Variables | `snake_case` | `posts`, `published_date` |
| Constantes y ajustes | `MAYUSCULAS_CON_GUION_BAJO` | `INSTALLED_APPS`, `DATABASES` |
| Campos de modelo | `snake_case` | `created_date`, `published_date` |

- Los imports van al inicio del archivo: primero los de Django, después los locales de la aplicación.
- Se deja una línea en blanco antes de cada comentario explicativo, y el comentario va sobre la línea que describe.

Ejemplo tomado de la vista del laboratorio:

```python
from django.shortcuts import render
from django.utils import timezone
from .models import Post


def post_list(request):
    # Filtramos solo los posts publicados y los ordenamos por fecha de publicación descendente
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'PawlyApp/post_list.html', {'posts': posts})
```

## Estructura de una aplicación Django

- El proyecto de configuración lleva el prefijo `config`: `configPawly`.
- Las aplicaciones llevan `PascalCase`: `PawlyApp`.
- Cada aplicación mantiene sus archivos en su propia carpeta: `models.py`, `views.py`, `urls.py`.
- Las plantillas van en `<aplicacion>/templates/<aplicacion>/`, de modo que la vista las referencie con el nombre de la aplicación por delante.
- Toda aplicación nueva debe registrarse en `INSTALLED_APPS` dentro de `settings.py`.

## Plantillas HTML

- Se declara `<!DOCTYPE html>` y el atributo `lang="es"`.
- Se incluye siempre `<meta charset="UTF-8">`.
- Indentación de 4 espacios.
- Las etiquetas de Django llevan un espacio interior: `{% for post in posts %}`, `{{ post.title }}`.
- Todo bucle que liste registros debe contemplar el caso vacío con `{% empty %}`.

## YAML (Docker Compose y GitHub Actions)

- Indentación de 2 espacios, nunca tabulaciones.
- Los valores de texto con espacios van entre comillas.
- Los nombres de servicios y contenedores van en minúsculas, separados con guion bajo: `pawly_web`, `pawly_db`.

## Dockerfile

- Las instrucciones se escriben en mayúsculas: `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`.
- Las imágenes base se fijan con una versión exacta: `python:3.12.4`, `alpine:3.21`.

## Dependencias

- `requirements.txt` fija las versiones de forma exacta: `Django==4.2.7`.
- No se versiona el entorno virtual `.venv`, que está excluido en `.gitignore`.
