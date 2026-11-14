# Revisión de seguridad y lógica de API_BACKEND

## Alcance y validación

Revisión estática de autenticación JWT, cookies, autorización, clave de API y flujo de usuarios, además de SQL, rutas y validaciones.

- Se analizaron 32 archivos Python: no se encontraron errores de sintaxis.
- No se encontró una suite de pruebas automatizadas.
- No se probó la conexión real a MySQL ni el envío de correo.

## Hallazgos de seguridad

| # | Severity | File | Lines | Vulnerability | Confidence |
|---|----------|------|-------|---------------|------------|
| 1 | 🟠 HIGH | [app.py](./app.py), [JWT.py](./source/JWT.py), [users.py](./source/services/users.py), [users.py](./source/routes/users.py) | 47; 4-11; 50-53; 77-87 | La clave JWT fija permite falsificar tokens y elevar el claim `rol` a `admin`; la autorización confía directamente en ese claim. | 9/10 |
| 2 | 🟠 HIGH | [auth.py](./source/auth.py), [config.py](./source/utils/config.py), [app.py](./app.py) | 7-11; 5-6; 61-62 | Si `API_KEY` falta o está vacía, el control global permite requests sin clave (comportamiento actual por defecto). | 9/10 |
| 3 | 🟡 MEDIUM | [app.py](./app.py), [JWT.py](./source/JWT.py), [users.py](./source/routes/users.py) | 49; 14-17; 59-87 | El JWT se guarda en una cookie con protección CSRF desactivada; una request autenticada podría ser forzada desde otro sitio si el navegador adjunta esa cookie. | 8/10 |
| 4 | 🟡 MEDIUM | [peliculas.py](./source/routes/peliculas.py), [funciones.py](./source/routes/funciones.py), [salas.py](./source/routes/salas.py), [sedes.py](./source/routes/sedes.py), [reservas.py](./source/routes/reservas.py) | 5-28; 5-7 | Las rutas de dominio no usan `@jwt_required` ni verifican roles: dependen únicamente del control global por API key. Cualquier implementación real de mutaciones quedaría sin autorización por usuario/rol. | 8/10 |

### Recomendaciones de seguridad

- Cargar `JWT_SECRET_KEY` de un secreto de despliegue robusto y rotarlo; no incluirlo en el repositorio.
- Rechazar el inicio de la aplicación cuando falte `API_KEY` en entornos que la requieran.
- Como se usan cookies JWT, habilitar CSRF y configurar cookies `Secure` y `SameSite` según el despliegue HTTPS.
- Proteger cada endpoint según su operación: autenticación JWT y autorización por rol/propietario, no solo una clave compartida. Evitar confiar exclusivamente en claims de rol con una clave expuesta; consultar el estado/rol vigente del usuario cuando corresponda.

## Fallos funcionales y de lógica

1. **El SQL inicial falla al crear `RESERVAS`.** `USUARIOS` define la PK `id_usuario`, pero la FK referencia `USUARIOS(id_usuarios)` ([init_db.sql](./db/init_db.sql:66)).
2. **El login con credenciales correctas termina en error 500.** La fila de usuario contiene `id_usuario`, pero la creación del token lee `registro["id_usuarios"]` ([JWT.py](./source/JWT.py:5)).
3. **Contraseña incorrecta o rol no permitido produce 500.** `ERROR_CLIENTE` es un diccionario, pero se invoca como función en las ramas de error ([users.py](./source/services/users.py:48), [users.py](./source/services/users.py:53)).
4. **Las operaciones principales todavía son respuestas simuladas.** Las rutas de películas, funciones, salas, sedes y reservas devuelven registros/mensajes fijos y no acceden a la base de datos; por ejemplo, [peliculas.py](./source/routes/peliculas.py:6) y [reservas.py](./source/routes/reservas.py:13). Si esto no es una etapa de scaffolding, esas operaciones no están implementadas.
5. **Registro parcialmente exitoso si falla el correo.** Primero se inserta el usuario y luego se envía el email; si el envío falla, la API informa error aunque la cuenta ya quedó creada ([users.py](./source/routes/users.py:29), [users.py](./source/routes/users.py:36)).
6. **Validación de registro incompleta.** Se usa `.strip()` sobre nombre/apellido sin comprobar antes que sean texto, y no se valida explícitamente el tipo del password antes de hashearlo ([users.py](./source/validators/users.py:10), [users.py](./source/routes/users.py:29)). Algunos valores JSON mal tipados pueden acabar en 400 poco claro o 500.

## Conclusión

La sintaxis Python es válida, pero el flujo de inicialización de la base y el login tienen errores bloqueantes. Antes de exponer la API, deben corregirse la clave JWT fija, el control de API key fail-open y la falta de CSRF/autorización por endpoint. Las rutas de negocio deben dejar de responder éxitos simulados antes de considerarlas funcionales.
