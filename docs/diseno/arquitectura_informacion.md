# Reto 11 — Árbol de navegación, arquitectura de información y prototipos

Proyecto: Pawly (Red Social de Mascotas) · ATI 2026-1

Funcionalidad núcleo elegida por el equipo: **Adopciones**. De las tres funcionalidades parecidas del enunciado (adopción, pareja y socialización), el MVP del equipo cubre solo adopción. El árbol de navegación, las pantallas y el modelo quedan acotados a ese alcance.

## 1. Árbol de navegación

Ver `mapa_navegacion.puml` / `mapa_navegacion.png` / `mapa_navegacion.svg`. Construido a partir de los actores (Visitante, Usuario registrado/Dueño, Administrador) y de los casos de uso del Product Backlog registrados como issues de este repositorio, dejando fuera los de socialización (UC-19, UC-20 y UC-21).

## 2. Tipos de página identificados

| Página | Actor(es) | Tipo |
|---|---|---|
| Landing / Iniciar sesión | Visitante | Formulario |
| Registro | Visitante | Formulario (wizard 2 pasos: cuenta + perfil humano) |
| Recuperar contraseña | Visitante | Formulario |
| Feed / Muro (Inicio) | Usuario | Índice (listado homogéneo de publicaciones) |
| Detalle de publicación | Usuario | Detalle + índice anidado (comentarios) |
| Crear publicación | Usuario | Formulario (compositor en el feed) |
| Buscar / Resultados | Usuario | Consulta + índice segmentado (usuarios / mascotas / publicaciones) |
| Feed de Adopción | Usuario | Índice filtrable por especie, edad y cercanía |
| Detalle mascota en adopción | Usuario | Detalle + CTA (visita guiada hacia Chat) |
| Postulación | Usuario | Formulario corto (bottom sheet en mobile, modal en desktop) |
| Mensajes (peticiones + lista) | Usuario | Índice |
| Conversación | Usuario | Detalle conversacional |
| Notificaciones | Usuario | Índice cronológico |
| Mi perfil (Humano) | Usuario | Detalle + índices anidados (mascotas, publicaciones, postulaciones) |
| Editar perfil humano | Usuario | Formulario |
| Perfil de mascota | Usuario | Detalle |
| Crear/editar mascota | Usuario | Formulario (incluye el bloque "Poner en adopción") |
| Perfil de otro usuario | Usuario | Detalle (solo lectura + acciones: seguir, chat) |
| Panel de administración | Administrador | Dashboard (indicadores + reportes pendientes) |
| Gestión de usuarios | Administrador | Índice + CRUD |
| Moderación (publicaciones/comentarios) | Administrador | Índice filtrable + acción de bloqueo |
| Reportes y veto | Administrador | Índice + detalle de reporte |

## 3. Unidades visuales por tipo de página

- **Barra superior** (autenticado): logo, buscador global, íconos de Notificaciones y Mensajes con contador, avatar.
- **Barra superior pública** (visitante): logo y enlace a Iniciar sesión / Crear cuenta.
- **Navegación principal**: barra inferior en mobile con 5 accesos (Inicio, Buscar, Adopción destacado al centro, Mensajes, Perfil); barra lateral fija en desktop con los mismos accesos más Notificaciones y el botón Publicar.
- **Card de publicación**: avatar, nombre, usuario, ubicación y fecha; texto; imagen opcional; acciones (me gusta, comentar); etiqueta "En adopción" cuando corresponde.
- **Card de mascota** (feed de adopción, perfil): foto 4:3, distancia, nombre, especie, edad y sexo.
- **Card de usuario** (resultados de búsqueda, sugerencias): avatar, nombre, usuario, ciudad y botón Seguir.
- **Formulario**: campos agrupados con etiquetas, texto de ayuda, selectores segmentados (especie, sexo), chips (temperamento), campo de fecha, interruptor (poner en adopción).
- **Bandeja de chat**: bloque de peticiones (aceptar / rechazar) y lista de conversaciones con último mensaje, hora y contador; en desktop, panel dividido con la conversación al lado.
- **Conversación**: mensaje de sistema que indica que el chat se abrió por una postulación, burbujas propias y ajenas con hora, campo de envío.
- **Lista de notificaciones**: ícono por tipo (adopción, comentario, petición, seguidor), texto, tiempo y acción rápida.
- **Tablas y tarjetas de administración**: indicadores, tabla de usuarios con estado y acciones (editar, vetar, eliminar), tarjetas de reportes con acción de bloqueo o veto.

## 4. Elementos individuales recurrentes

Botón primario (terracota), secundario (contorno), oscuro y de peligro; enlace de texto; íconos lineales (casa, lupa, huella, burbuja, campana, persona, corazón, pin, filtro, calendario, cámara, escudo, bandera); títulos en Bricolage Grotesque; texto en Figtree; campo de texto, área de texto, campo de fecha, selector segmentado, chip, interruptor; avatar circular; etiqueta de estado (En adopción, Activa, Reportes, Vetada); contador numérico; barra de progreso del registro.

## 5. Patrones de navegación

- **Índice**: feed principal, feed de adopción, resultados de búsqueda, lista de chats, notificaciones, mascotas propias, tabla de usuarios y tarjetas de reportes.
- **Menú**: barra inferior (mobile) o lateral (desktop) con accesos fijos para el Usuario; menú lateral propio del Administrador (Panel, Usuarios, Publicaciones, Comentarios, Reportes). Sin submenús: navegación plana con un máximo de tres niveles de profundidad.
- **Visita guiada**: registro en dos pasos (cuenta, luego perfil humano) y postulación a adopción (ver mascota, confirmar postulación con un mensaje, redirección automática al chat abierto con el dueño), que refleja el `<<include>>` de `UC_initchat` en el diagrama de casos de uso.
- **Consulta**: buscador único en la barra superior, visible en todas las páginas autenticadas, con resultados por pestañas (Usuarios, Mascotas, Publicaciones). En el feed de adopción hay además filtros por especie, edad y distancia.

## 6. Preguntas de arquitectura de información

- **Áreas de contenido y servicio**: Muro social (publicaciones y comentarios), Mascotas (perfiles y feed de adopción), Mensajería, Notificaciones, Administración y moderación.
- **Zona de navegación**: barra superior más barra inferior en mobile; barra superior más lateral fija en desktop. Persistente en todas las páginas autenticadas.
- **Sistemas de ayuda**: textos de ayuda bajo los campos de formulario, mensajes de sistema dentro del chat y avisos contextuales (por ejemplo "Se abrirá un chat con Carlos"). No se contempla un centro de ayuda separado en el MVP.
- **Formularios vs. listados**: formularios en Cuenta y acceso, Editar perfil, Crear/editar mascota, Postulación; listados en todo lo demás.

## 7. Diseño de interacción, navegación e interfaz

- **Interacción**: postularse a una adopción toma tres toques desde el feed de adopción (abrir mascota, postularme, enviar). La apertura automática del chat evita un paso manual. La postulación se puede cancelar desde el mismo chat.
- **Navegación**: sin enlaces externos en el MVP; las notificaciones enlazan directo al chat, comentario o mascota referida; nombres en lenguaje cercano ("Postularme para adoptar", "Ver a Toby", "Personas que quizá conoces").
- **Interfaz**: huella como ícono de Adopción y del logo; corazón para guardar; burbuja para mensajes; campana para notificaciones. Cards para publicaciones y mascotas; galería de miniaturas en el detalle de la mascota; bottom sheet en mobile y modal en desktop para la postulación.

## 8. Sistema visual del prototipo

- **Tipografía**: Bricolage Grotesque (titulares, 600 a 800) y Figtree (texto, 400 a 700). Ambas en Google Fonts y disponibles en Figma.
- **Color**: lila de marca `#AE95C7` (tomado del logotipo de Pawly) para acciones principales, con `#7E62A0` para enlaces y estados activos sobre fondo claro y `#EFE9F5` como versión suave; fondo crema `#FBF7F2`, superficie `#FFFDFA`, texto `#1F1A17`, texto secundario `#7A6F68`; verde `#3F7D5A` para "En adopción" y estados positivos, ámbar y rojo para moderación.
- **Logotipo**: el de `Media de pawly/` (corazón con perro, gato y ave más la palabra "pawly"). En las barras se usa el isotipo más la palabra en horizontal; en Iniciar sesión, el logotipo completo en vertical.
- **Radios**: 8, 14 y 20 px, más píldora para botones y chips.
- **Retícula**: mobile a una columna sobre 360 px con márgenes de 16 px; desktop sobre 12 columnas en 1440 px, con barra lateral de 240 px, contenido central de 680 px y columna auxiliar de 320 px. En mobile la columna auxiliar se oculta y la barra lateral se convierte en barra inferior.

## 9. Datos del modelo en pantalla

Las pantallas muestran los atributos del `modelo_dominio.puml`: `Usuario` (username, email), `PerfilHumano` (nombre, foto, ci, fechaNacimiento, genero, descripcion, ciudad), `PerfilMascota` (nombre, especie, sexo, temperamento, fechaNacimiento, descripcion, foto, enAdopcion), `Publicacion`, `Comentario`, `Solicitud` (tipo adopción, estado, caracteristicasBuscadas), `Chat`, `Mensaje`, `Notificacion` y `Administrador`. Las fechas se presentan como fechas (campo con calendario en formularios, formato corto en listados) y no como texto libre.

## 10. Internacionalización

Los textos de interfaz (etiquetas, botones, mensajes de ayuda y de sistema) no provienen del modelo de dominio y quedan sujetos a i18n. Se externalizan en archivos planos JSON por idioma (`es.json` por defecto, `en.json` a futuro) en lugar de guardarlos en base de datos, porque no varían por usuario. Los valores enumerados del dominio (`especie`, `sexo`, `estado` de la postulación, `motivo` del reporte) se traducen con un diccionario de etiquetas asociado a cada enum. El idioma y el tema elegidos por cada persona sí se guardan en el modelo, en `Usuario`.

## 10.1 Cambios al modelo de dominio

Al revisar las pantallas contra el modelo de la Entrega 1 aparecieron datos que no estaban modelados. El modelo actualizado está en `modelo_dominio.puml` / `.png` / `.svg`.

| Cambio | Motivo (pantalla) |
|---|---|
| `Usuario` agrega `requiereCambioClave`, `idioma`, `tema`, `notificarPorCorreo` | Ajustes: usuarios migrados que entran con su cédula, idioma, tema claro/oscuro y aviso por correo (UC-02, UC-26, NFR-01) |
| `PerfilMascota` quita `buscaPareja` y `buscaSocializar`; agrega `ubicacion` y `caracteristicasBuscadas` | Alcance solo Adopciones; Editar mascota y feed por cercanía (UC-16, UC-17) |
| `Solicitud` se reemplaza por `Postulacion` (`mensaje`, `estado` con `cancelada`) | Postulación con mensaje y opción de cancelarla desde el chat (UC-18) |
| Nueva `PeticionChat` | Peticiones de chat que se aceptan o rechazan en Mensajes (UC-22) |
| Nueva `Multimedia` (foto, video, audio, enlace) | Crear publicación (UC-10) |
| Etiquetas de `Publicacion` a personas y mascotas | Crear publicación (UC-11) |
| `Comentario` responde a otro `Comentario` | Respuestas anidadas (UC-13) |
| Nuevo `Reporte` (objeto, motivo, detalle, estado) | Reportar contenido y panel de reportes del Admin (UC-27, UC-28) |
| `Notificacion.tipo` con valores definidos | Íconos y acciones por tipo en Notificaciones (UC-25) |

## 11. Prototipos

Carpeta `prototipo/`: `mobile.html` (Android 360×640, 20 pantallas) y `desktop.html` (1440×1024, 19 pantallas), construidos con `estilos.css` como sistema de diseño compartido. Las imágenes exportadas de cada pantalla están en `prototipo/export/`.

## 12. Trazabilidad: casos de uso del Product Backlog → pantallas

Los códigos son los de los issues del repositorio `Pawly-ATI-UCV/pawly` (Reto 9). UC-19, UC-20 y UC-21 (socialización) quedan fuera del MVP del equipo.

| Caso de uso | Pantalla mobile | Pantalla desktop |
|---|---|---|
| UC-01 Registrarse | 02 Registro paso 1, 16 Registro paso 2 | 02, 15 |
| UC-02 Iniciar sesión (incluye migrados con cédula) | 01 Iniciar sesión, 20 Ajustes (cambiar contraseña) | 01, 19 |
| UC-03 Recuperar contraseña | 15 Recuperar contraseña | 14 |
| UC-04 Cerrar sesión | 20 Ajustes | 03 barra lateral, 19 |
| UC-05 Editar perfil humano | 16 (mismo formulario del paso 2) | 15 |
| UC-06 Crear perfil de mascota | 12 Mi perfil (Agregar), 13 formulario | 11, 12 |
| UC-07 Editar perfil de mascota | 13 Editar mascota | 12 |
| UC-08 Eliminar perfil de mascota | 13 (menú de la mascota) | 12 Zona de peligro |
| UC-09 Publicar | 03 compositor, 17 Crear publicación | 03, 16 |
| UC-10 Adjuntar multimedia | 17 (foto, video, audio, enlace) | 16 |
| UC-11 Etiquetar | 17 (etiquetados) | 16 |
| UC-12 Comentar | 04 Publicación | 04 |
| UC-13 Responder comentario | 04 (enlace Responder) | 04 (respuesta anidada) |
| UC-14 Buscar | 05 Buscar | 05 |
| UC-15 Seguir usuario | 05, 18 Perfil de otro usuario | 05, 17 |
| UC-16 Marcar mascota en adopción | 13 bloque "Poner en adopción" | 12 |
| UC-17 Navegar feed de adopciones | 06 Adopción | 06 |
| UC-18 Postularse para adoptar | 07 Mascota, 08 Postulación | 07, 08 |
| UC-22 Enviar petición de chat | 18 (botón), 09 Mensajes (aceptar/rechazar) | 17, 09 |
| UC-23 Chatear | 10 Conversación | 09 |
| UC-24 Abrir chat | 10 (mensaje de sistema) | 09 |
| UC-25 Recibir notificación | 11 Notificaciones | 10 |
| UC-26 Enviar correo | 20 Ajustes (interruptor "También por correo") | 19 |
| UC-27 Reportar contenido | 19 Reportar | 18 |
| UC-28 Vetar cuenta | 14 Admin | 13 |
| UC-29 Bloquear comentario | 14 Admin (pestaña Reportes) | 13 |
| UC-30 Bloquear publicación | 14 Admin | 13 |
| UC-31 Gestionar usuarios | 14 Admin | 13 |
| NFR-01 adaptativo, idioma, tema | Todo el prototipo; 20 Ajustes (idioma y tema) | 19 |
