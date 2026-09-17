# Política de control de versiones

Política de manejo de ramas del proyecto Pawly, según lo establecido en el
Laboratorio #9 de Aplicaciones con Tecnología Internet.

## Ramas

| Rama | Propósito | Ambiente |
|---|---|---|
| `feature/*` | Trabajo por funcionalidad o por programador. Se crea desde `develop` y se integra de vuelta a `develop`. | — |
| `develop` | Integra las ramas previas por funcionalidad o programador. Permite realizar las pruebas de control de calidad y certificación. | DEV |
| `release` | Candidato de versión. Se crea desde `develop` una vez que la funcionalidad está completa. | UAT/PRE |
| `master` | Todos los cambios y correcciones listos para ser mandados a un ambiente de producción, es decir, ya probados. Desde aquí se hace la integración continua para el despliegue. | PRO |

El laboratorio establece como mínimo el manejo de `develop` y `master`. Este
proyecto implementa además `release` y las ramas de funcionalidad, siguiendo el
esquema completo del diagrama del laboratorio.

## Flujo de trabajo

```
feature/*  ->  develop  ->  release  ->  master
                  |            |            |
                 DEV        UAT/PRE        PRO
```

1. Cada funcionalidad se desarrolla en su propia rama `feature/*` creada desde `develop`.
2. Al terminar, la rama se integra a `develop`, donde se ejecutan las pruebas de control de calidad.
3. Cuando `develop` está estable, se lleva a `release` para la certificación.
4. Una vez certificado, `release` se integra a `master`, que es la rama de producción.

## Nomenclatura de ramas

El laboratorio indica que se pueden usar referencias de los IDs de issues
(requisitos) o de correcciones de errores. Sobre esa base, el equipo adopta:

| Tipo | Formato | Ejemplo |
|---|---|---|
| Funcionalidad | `feature/<id-issue>-<descripcion-corta>` | `feature/12-registro-mascota` |
| Corrección | `fix/<id-issue>-<descripcion-corta>` | `fix/25-error-login` |

Cuando el trabajo no corresponde a un issue del backlog, se omite el número y se
deja una descripción en minúsculas separada por guiones.

## Integración

- Las integraciones hacia `develop`, `release` y `master` se realizan mediante Pull Request en GitHub, nunca con push directo a esas ramas.
- Cada push dispara el workflow de integración continua descrito en el README.
- No se integra a `master` código que no haya pasado por `develop` y `release`.
