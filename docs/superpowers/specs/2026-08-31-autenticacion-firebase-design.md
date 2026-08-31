# Autenticación con Firebase — Diseño

Fecha: 2026-08-31
Rama: `interfaz`
Estado: aprobado para escribir plan de implementación

## 1. Contexto

`MedScale-ORL` es una app Kivy standalone (SQLite local, sin backend) que hoy
arranca directamente en la pantalla `home`. No existe concepto de usuario ni de
sesión. Se quiere que la app abra en una pantalla de inicio de sesión
(`frontend/assets/iniciose.jpeg` es el fondo de marca de esa pantalla) donde el
usuario pueda **registrarse** e **iniciar sesión** con **correo/contraseña** o
con **Google**, manteniendo la sesión entre reinicios.

Backend elegido: **Firebase Authentication** (API REST Identity Toolkit).
Plataforma objetivo: **APK Android** (el flujo de Google se hace con un WebView
nativo por `jnius`; hay fallback de escritorio para desarrollo).

## 2. Objetivos

- Pantalla de login como pantalla inicial, con el estilo visual de la app y de
  `iniciose.jpeg`.
- Pantalla de registro (nombre, correo, contraseña).
- Registro e inicio de sesión con correo/contraseña vía Firebase REST.
- Inicio de sesión con Google (WebView OAuth en Android, navegador + servidor
  local en escritorio).
- Sesión persistente: al reabrir la app, si el `refresh_token` sigue siendo
  válido, entra directo a `home`.
- Cerrar sesión desde el perfil.
- El perfil muestra el nombre/correo reales del usuario autenticado.
- Sin dependencias nuevas empaquetadas en Python (se usa `urllib`/`json` de
  stdlib); solo se añade el recipe `openssl` al `buildozer.spec`.

## 3. No-objetivos

- No hay servidor propio ni base de datos de usuarios en el dispositivo (Firebase
  es la fuente de verdad de identidad).
- No se migran ni asocian los `pacientes`/`evaluaciones` existentes a un usuario
  (siguen siendo datos locales compartidos en el dispositivo).
- No se refactorizan las ~20 pantallas existentes; solo se centralizan constantes
  de estilo que las pantallas nuevas necesitan.
- No hay verificación obligatoria de correo (se ofrece "olvidé mi contraseña"
  pero no se bloquea el acceso por correo no verificado).
- No hay soporte iOS en este trabajo (el fallback de escritorio cubre desarrollo;
  el WebView es Android-only).

## 4. Configuración de Firebase (tarea del usuario, guiada)

1. `console.firebase.google.com` → **Agregar proyecto** → nombre `MedScale-ORL`
   → crear.
2. **Build → Authentication → Comenzar**.
3. **Sign-in method**:
   - Habilitar **Correo electrónico/contraseña** → guardar.
   - Habilitar **Google** → elegir correo de soporte → guardar.
4. **⚙️ Configuración del proyecto → Tus apps → `</>` (Web)** → registrar app →
   copiar `apiKey` y `authDomain` (`medscale-orl.firebaseapp.com`).
5. En el proveedor **Google** (dentro de Authentication) → *Configuración del SDK
   web* → copiar el **ID de cliente web** (OAuth 2.0).
6. El usuario entrega: `apiKey`, `authDomain`, `googleWebClientId`.

Estos tres valores se colocan en `frontend/firebase_config.py` (ignorado por
git). El repo incluye `frontend/firebase_config.example.py` con placeholders y
comentarios.

```python
# frontend/firebase_config.example.py
API_KEY = "TU_API_KEY"
AUTH_DOMAIN = "medscale-orl.firebaseapp.com"
GOOGLE_WEB_CLIENT_ID = "xxxxx.apps.googleusercontent.com"
```

`firebase_config.py` se añade a `.gitignore`. `auth.py` importa de
`firebase_config`; si el archivo no existe, lanza un error claro al arrancar
("Copia firebase_config.example.py a firebase_config.py y rellena tus llaves").

## 5. Arquitectura

```
frontend/
  firebase_config.py            (git-ignored, llaves reales)
  firebase_config.example.py    (plantilla en el repo)
  auth.py                       (lógica de auth, SIN Kivy)
  google_oauth.py               (obtención del id_token de Google: WebView / escritorio)
  screens/
    login_screen.py             (name="login")
    register_screen.py          (name="register")
  widgets/
    ui.py                       (+ constantes de color + helpers de formulario)
  main.py                       (+ pantallas nuevas + compuerta de sesión)
  screens/perfil_screen.py      (+ botón cerrar sesión + datos reales del usuario)
```

Flujo de arranque:

```
App.build()
  init_db()
  auth.refrescar_sesion()
    ├─ sesión válida  → ScreenManager.current = "home"
    └─ sin sesión     → ScreenManager.current = "login"
```

## 6. Componentes

### 6.1 `frontend/auth.py`

Módulo puro (sin Kivy). Usa `urllib.request` + `json`. Base URL:
`https://identitytoolkit.googleapis.com/v1/accounts:` + método, con
`?key=API_KEY`. Refresh contra `https://securetoken.googleapis.com/v1/token`.

Estado de sesión persistido en la tabla `configuracion` (k/v, ya existente) con
las claves: `auth_refresh_token`, `auth_id_token`, `auth_expira_en` (epoch),
`auth_uid`, `auth_correo`, `auth_nombre`. `cerrar_sesion()` borra esas claves.

API pública:

| Función | Descripción | Errores traducidos |
|---|---|---|
| `registrar(nombre, correo, clave)` | `accounts:signUp` (`returnSecureToken=true`), luego `accounts:update` para `displayName`. Guarda sesión. Devuelve `dict` de usuario. | `EMAIL_EXISTS`, `WEAK_PASSWORD`, `INVALID_EMAIL` |
| `iniciar_sesion(correo, clave)` | `accounts:signInWithPassword`. Guarda sesión. | `EMAIL_NOT_FOUND`, `INVALID_PASSWORD`, `INVALID_LOGIN_CREDENTIALS`, `USER_DISABLED` |
| `iniciar_con_google(google_id_token)` | `accounts:signInWithIdp` con `postBody="id_token=<...>&providerId=google.com"`, `requestUri=AUTH_DOMAIN`. Guarda sesión. | `errores genéricos` |
| `refrescar_sesion()` | Si no hay `auth_refresh_token` → `False`. Si `auth_expira_en` está a >5 min → `True` sin red. Si no, POST a `securetoken` con `grant_type=refresh_token`; actualiza tokens y `auth_expira_en`. En fallo de red devuelve `True` si el token guardado aún no expiró, `False` si expiró. | `TOKEN_EXPIRED`, `USER_DISABLED` → `cerrar_sesion()` y `False` |
| `enviar_reset(correo)` | `accounts:sendOobCode` (`requestType=PASSWORD_RESET`). | `EMAIL_NOT_FOUND` |
| `usuario_actual()` | `dict {uid, correo, nombre}` desde `configuracion`, o `None`. | — |
| `id_token_valido()` | Devuelve el `auth_id_token` refrescándolo si está por expirar; para futuras llamadas autenticadas. | — |
| `cerrar_sesion()` | Borra las claves `auth_*` de `configuracion`. | — |

Detalles:

- Timeout de red: 15 s. Sin red → excepción `AuthError("Sin conexión")`.
- Todas las funciones que llaman a la red lanzan `AuthError(mensaje_es)` con
  mensaje ya en español listo para mostrar; las pantallas solo lo pintan.
- `_guardar_sesion(resp)`: calcula `auth_expira_en = time.time() + int(expiresIn)`.
- Helper `_post(url, payload) -> dict` centraliza `urllib`, cabeceras JSON,
  manejo de `HTTPError` (parsea `error.message` de Firebase) y `URLError`.
- `demo()` con `assert`: monta una BD temporal, simula `_guardar_sesion` con un
  `expiresIn` corto y verifica que `refrescar_sesion()` respeta la expiración y
  que `cerrar_sesion()` limpia. Ejecutable con `python -m frontend.auth`.

### 6.2 `frontend/google_oauth.py`

Una sola función pública: `obtener_id_token_google() -> str` (bloqueante, se
llama desde un hilo para no congelar la UI; la pantalla usa
`threading.Thread` + `Clock.schedule_once` para volver al hilo de Kivy).

Construye la URL de autorización:

```
https://accounts.google.com/o/oauth2/v2/auth
  ?client_id=<GOOGLE_WEB_CLIENT_ID>
  &redirect_uri=<redirect>
  &response_type=id_token
  &scope=openid%20email%20profile
  &nonce=<secrets.token_urlsafe(16)>
  &prompt=select_account
```

- **Android** (`detección: importa jnius sin error y existe org.kivy.android`):
  `redirect_uri = https://<AUTH_DOMAIN>/__/auth/handler`. Se crea un
  `android.webkit.WebView` a pantalla completa mediante `jnius` dentro de un
  `PythonActivity`, con `WebViewClient` cuyo `shouldOverrideUrlLoading`
  intercepta la URL que empiece por el `redirect_uri` y extrae
  `#id_token=...` del fragmento. Se cierra el WebView y se devuelve el token.
  JavaScript y DOM storage habilitados. Cancelar (botón atrás) → lanza
  `AuthError("Inicio con Google cancelado")`.
- **Escritorio** (fallback): `redirect_uri = http://127.0.0.1:8765`. Se levanta
  un `http.server.HTTPServer` de un solo request en ese puerto; como el
  `id_token` llega en el fragmento `#` (no lo ve el servidor), la página de
  respuesta devuelve un `<script>` que hace `fetch` de
  `http://127.0.0.1:8765/token?…` con `location.hash`. Se abre la URL de
  autorización con `webbrowser.open`. Timeout 120 s → `AuthError`.

El `id_token` de Google resultante se pasa a `auth.iniciar_con_google()`.

Riesgo conocido: el WebView por `jnius` es la pieza más frágil (hilo de UI de
Android, ciclo de vida de la Activity). `ponytail:` mantener el WebView lo más
mínimo posible; si resulta inestable en dispositivo, alternativa es un
`Intent` a Custom Tabs con `intent-filter` de redirect en el `buildozer.spec`.

### 6.3 `frontend/widgets/ui.py` (ampliación)

Añadir (sin tocar lo existente):

```python
C_PRIMARY      = get_color_from_hex("#1976D2")
C_PRIMARY_DARK = get_color_from_hex("#1565C0")
C_CARD         = get_color_from_hex("#FFFFFF")
C_TEXT_MAIN    = get_color_from_hex("#1A1A2E")
C_TEXT_SEC     = get_color_from_hex("#6B7280")
C_ERROR        = get_color_from_hex("#D32F2F")
```

Helpers:

- `text_field(hint, password=False) -> TextInput` — mismo estilo que
  `ScaleScreen._numeric_input` (fondo `#F0F2F5`, sin bordes, `cursor_color`
  primario, `padding` 10/8, `font_size` sp(14)), `multiline=False`.
- `primary_button(text) -> Button` — relleno `C_PRIMARY`, texto blanco bold,
  `height dp(50)`, `background_normal=""`.
- `outline_button(text) -> Button` — fondo transparente, borde `C_PRIMARY`
  (dibujado con `Line` en `canvas.before`), texto `C_PRIMARY`.
- `link_label(text) -> Label` — texto `C_PRIMARY`, `sp(13)`, con
  `on_touch_down` que dispara un callback (Kivy `Label` no es clicable; se
  envuelve en un `ButtonBehavior` mixin o se usa un `Button` plano
  transparente).

### 6.4 `frontend/screens/login_screen.py` — `name="login"`

Estructura (todo dentro de un `FloatLayout` para poder poner el fondo):

- `Image(source="frontend/assets/iniciose.jpeg", allow_stretch=True,
  keep_ratio=False)` a pantalla completa.
- Un `BoxLayout` vertical centrado (`pos_hint={"center_x": .5, "center_y": .46}`,
  `size_hint=(.82, None)`), sobre la zona blanca de la imagen:
  - `Label` "Iniciar sesión" (`sp(20)`, bold, `C_TEXT_MAIN`).
  - `text_field("Correo electrónico")`.
  - `text_field("Contraseña", password=True)`.
  - `Label` de error (`C_ERROR`, `sp(12)`, `opacity=0` hasta que haya error).
  - `primary_button("Iniciar sesión")`.
  - `outline_button("Continuar con Google")`.
  - Fila con `link_label("¿Olvidaste tu contraseña?")`.
  - Fila "¿No tienes cuenta?  " + `link_label("Regístrate")` → `current="register"`.
- Spinner/estado: mientras hay petición en curso, los botones se deshabilitan y
  el de acción muestra "Ingresando…".

Lógica:

- `_ingresar()`: valida campos no vacíos → hilo con `auth.iniciar_sesion` →
  éxito: `Clock` → `App.get_running_app().root.current = "home"`; error:
  pinta `AuthError.args[0]` en el label.
- `_google()`: hilo con `google_oauth.obtener_id_token_google()` →
  `auth.iniciar_con_google(tok)` → `home`; error → label.
- `_reset()`: si el campo correo tiene texto → `auth.enviar_reset` → toast
  "Te enviamos un correo para restablecer la contraseña"; si está vacío →
  error "Escribe tu correo primero".
- `on_pre_enter`: limpia campos y label de error.

### 6.5 `frontend/screens/register_screen.py` — `name="register"`

Mismo patrón visual. Campos: nombre, correo, contraseña, confirmar contraseña.
Validación local: nombre no vacío, correo con `@`, contraseña ≥ 6, coincide con
confirmar. Botón **Crear cuenta** → `auth.registrar` → `home`. Botón
**Continuar con Google** (mismo flujo que login). `link_label` "Ya tengo cuenta"
→ `current="login"`.

### 6.6 `frontend/main.py` (cambios)

- `from frontend import auth`
- `from frontend.screens.login_screen import LoginScreen`
- `from frontend.screens.register_screen import RegisterScreen`
- Añadir ambas al `ScreenManager` y luego fijar `current` explícitamente
  (no dependemos del orden de inserción):

```python
sm.add_widget(LoginScreen(name="login"))
sm.add_widget(RegisterScreen(name="register"))
sm.add_widget(HomeScreen(name="home"))
...
try:
    sm.current = "home" if auth.refrescar_sesion() else "login"
except Exception:
    sm.current = "login"
return sm
```

### 6.7 `frontend/screens/perfil_screen.py` (cambios)

- En `_rebuild()`: reemplazar la tarjeta fija "¡Hola, Doctor(a)!" por
  `auth.usuario_actual()` → mostrar `nombre` y `correo`.
- Añadir al final un `Button` "Cerrar sesión" (rojo, `C_ERROR` de fondo) →
  `auth.cerrar_sesion()` + `navigate_to("login")`.

### 6.8 `buildozer.spec` (cambios)

- `requirements = python3,kivy` → `requirements = python3,kivy,openssl`
  (HTTPS de `urllib` en Android). `pyjnius` ya lo incluye p4a por defecto.
- `INTERNET` y `ACCESS_NETWORK_STATE` ya están.
- `source.include_exts` ya incluye `jpg` → `iniciose.jpeg` se empaqueta.

## 7. Flujo de datos

```
Registro correo:
  RegisterScreen → auth.registrar() → Firebase signUp/update
    → _guardar_sesion() escribe auth_* en configuracion → current="home"

Login correo:
  LoginScreen → auth.iniciar_sesion() → Firebase signInWithPassword
    → _guardar_sesion() → current="home"

Login Google:
  LoginScreen → google_oauth.obtener_id_token_google()
    (Android: WebView; escritorio: navegador + 127.0.0.1:8765)
    → id_token de Google → auth.iniciar_con_google() → Firebase signInWithIdp
    → _guardar_sesion() → current="home"

Reapertura de la app:
  main.build() → auth.refrescar_sesion()
    lee auth_refresh_token de configuracion
    → si válido/refrescable: current="home"
    → si no: current="login"

Cerrar sesión:
  PerfilScreen → auth.cerrar_sesion() borra auth_* → current="login"
```

## 8. Manejo de errores

- `auth.py` traduce los códigos de Firebase a español en `AuthError`:
  - `EMAIL_EXISTS` → "Ese correo ya está registrado."
  - `INVALID_PASSWORD` / `INVALID_LOGIN_CREDENTIALS` → "Correo o contraseña incorrectos."
  - `EMAIL_NOT_FOUND` → "No existe una cuenta con ese correo."
  - `WEAK_PASSWORD` → "La contraseña debe tener al menos 6 caracteres."
  - `INVALID_EMAIL` → "El correo no es válido."
  - `USER_DISABLED` → "Esta cuenta está deshabilitada."
  - `TOO_MANY_ATTEMPTS_TRY_LATER` → "Demasiados intentos. Intenta más tarde."
  - Desconocido → el `message` crudo.
- `URLError` / timeout → `AuthError("Sin conexión. Revisa tu internet.")`.
- Google cancelado por el usuario → `AuthError("Inicio con Google cancelado")`,
  la pantalla lo muestra sin tono de error grave.
- `firebase_config.py` ausente → `RuntimeError` explicativo al importar `auth`,
  atrapado en `main.build()` que muestra `login` con un label fijo pidiendo
  configurar las llaves (evita crash en blanco).

## 9. Pruebas

`tests/test_auth.py` (stdlib `unittest`, sin frameworks nuevos):

- `monkeypatch` de `auth._post` para devolver respuestas fijas de Firebase.
- BD temporal (`configuracion` real, `_db_path` apuntando a archivo temporal).
- Casos:
  - `registrar()` guarda `auth_*` y `usuario_actual()` los devuelve.
  - `iniciar_sesion()` con `_post` que lanza `HTTPError` de `INVALID_PASSWORD`
    → `AuthError` con el mensaje traducido.
  - `refrescar_sesion()` sin `auth_refresh_token` → `False`.
  - `refrescar_sesion()` con `auth_expira_en` futuro → `True` sin llamar a `_post`.
  - `refrescar_sesion()` con token expirado y `_post` OK → actualiza
    `auth_expira_en`.
  - `refrescar_sesion()` con token expirado y `_post` que lanza `URLError`
    → `False` y sesión limpiada.
  - `cerrar_sesion()` elimina todas las claves `auth_*`.
- `auth.demo()` como `__main__` self-check para la lógica de expiración.

`google_oauth.py`: se testea solo el constructor de la URL de autorización
(`_build_auth_url()` puro) — scopes, `response_type=id_token`, `nonce` presente.
El WebView/servidor no se testea automáticamente (requiere dispositivo/navegador);
verificación manual documentada en el plan.

Los tests de `tests/test_frontend.py` existentes deben seguir pasando (no
importan `auth` ni las pantallas nuevas de forma que rompa).

## 10. Riesgos y decisiones

- **WebView de Google en Android**: pieza más frágil. Si en dispositivo real
  falla, plan B es Chrome Custom Tabs + `intent-filter` de esquema propio en
  `buildozer.spec`. Se documenta como paso de verificación manual en el plan.
- **HTTPS en Android**: depende del recipe `openssl`; si el build falla, revisar
  `requirements`. Verificación: llamada real a `signUp` desde APK de debug.
- **`iniciose.jpeg` es fondo fijo**: la zona blanca del formulario está a ~46 %
  de altura; en pantallas muy anchas/estrechas el formulario podría desalinearse
  del hueco de la imagen. Mitigación: `size_hint` relativo y `center_y` ajustado
  en pruebas; aceptable que el fondo se recorte (`keep_ratio=False`).
- **Datos locales no ligados a usuario**: si dos personas usan el mismo
  dispositivo con cuentas distintas ven los mismos pacientes. Fuera de alcance;
  se puede abordar después ligando `pacientes.usuario_uid`.
