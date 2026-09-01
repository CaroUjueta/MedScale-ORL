# Autenticación con Firebase — Plan de Implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Que MedScale-ORL abra en una pantalla de inicio de sesión donde el usuario se registra e inicia sesión con correo/contraseña o con Google (Firebase), manteniendo la sesión entre reinicios.

**Architecture:** Módulo `frontend/auth.py` sin Kivy que habla con la API REST de Firebase Identity Toolkit usando `urllib`/`json` de la stdlib y guarda la sesión en la tabla `configuracion` que ya existe. `frontend/google_oauth.py` obtiene un `id_token` de Google (WebView `jnius` en Android, navegador + servidor local en escritorio) que `auth.py` canjea con Firebase. Dos pantallas Kivy nuevas (`login`, `register`) con el estilo de la app y de `frontend/assets/iniciose.jpeg`. `frontend/main.py` decide en el arranque si mostrar `home` o `login`.

**Tech Stack:** Python 3, Kivy, SQLite (stdlib `sqlite3`), Firebase Authentication REST API, `urllib` (stdlib), `pyjnius` (solo Android, ya incluido por python-for-android), Buildozer.

**Spec:** `docs/superpowers/specs/2026-08-31-autenticacion-firebase-design.md`

## Global Constraints

- Sin dependencias nuevas empaquetadas en Python: HTTP solo con `urllib` + `json` de la stdlib.
- `buildozer.spec`: `requirements = python3,kivy,openssl` (el resto del archivo no cambia salvo lo indicado).
- Todos los textos visibles para el usuario en español.
- Claves de sesión en la tabla `configuracion` (k/v ya existente), exactamente: `auth_refresh_token`, `auth_id_token`, `auth_expira_en`, `auth_uid`, `auth_correo`, `auth_nombre`.
- `frontend/firebase_config.py` va en `.gitignore`; `frontend/firebase_config.example.py` se commitea con placeholders.
- Endpoints Firebase: `https://identitytoolkit.googleapis.com/v1/accounts:<metodo>?key=<API_KEY>`; refresh: `https://securetoken.googleapis.com/v1/token?key=<API_KEY>`.
- Timeout de red: 15 s en `auth.py`; 120 s en el flujo de Google de escritorio.
- Plataforma objetivo: APK Android. El fallback de escritorio es solo para desarrollo.
- Paleta: primario `#1976D2`, primario oscuro `#1565C0`, texto `#1A1A2E`, texto secundario `#6B7280`, error `#D32F2F`, fondo de campo `#F0F2F5`, blanco `#FFFFFF`.
- Los tests usan `unittest` de la stdlib (sin pytest, sin dependencias nuevas). Se ejecutan con `python -m unittest <ruta>`.

---

### Task 1: Scaffolding del repositorio

**Files:**
- Create: `frontend/firebase_config.example.py`
- Modify: `.gitignore`
- Modify: `buildozer.spec:13`
- Create: `tests/_util.py`
- Create: `tests/__init__.py` (ya existe; no tocar si está)

**Interfaces:**
- Consumes: nada.
- Produces:
  - `frontend/firebase_config.example.py` con constantes `API_KEY: str`, `AUTH_DOMAIN: str`, `GOOGLE_WEB_CLIENT_ID: str`.
  - `tests/_util.py`:
    - `bd_temporal()` — context manager; crea una BD SQLite aislada (vía env `ANDROID_PRIVATE`), llama `init_db()`, hace `yield` del directorio, y restaura el entorno al salir.
    - `stub_cfg() -> types.SimpleNamespace` — objeto con `API_KEY`, `AUTH_DOMAIN`, `GOOGLE_WEB_CLIENT_ID` de prueba.

- [ ] **Step 1: Crear `frontend/firebase_config.example.py`**

```python
"""Plantilla de configuración de Firebase.

Copia este archivo a `frontend/firebase_config.py` y rellena los valores
reales de tu proyecto (consola de Firebase). `firebase_config.py` está en
.gitignore y NO debe subirse al repositorio.

Cómo obtener los valores: ver docs/firebase-setup.md
"""

# Firebase -> Configuración del proyecto -> Tus apps -> app Web -> "apiKey"
API_KEY = "PON_AQUI_TU_API_KEY"

# Normalmente "<id-del-proyecto>.firebaseapp.com"
AUTH_DOMAIN = "PON_AQUI_TU_AUTH_DOMAIN"

# Firebase -> Authentication -> Sign-in method -> Google
#   -> "Configuración del SDK web" -> "ID de cliente web"
GOOGLE_WEB_CLIENT_ID = "PON_AQUI_TU_WEB_CLIENT_ID.apps.googleusercontent.com"
```

- [ ] **Step 2: Añadir `firebase_config.py` a `.gitignore`**

Añadir al final de `.gitignore`:

```
frontend/firebase_config.py
```

- [ ] **Step 3: Actualizar `buildozer.spec`**

En `buildozer.spec` línea 13, cambiar:

```
requirements = python3,kivy
```

por:

```
requirements = python3,kivy,openssl
```

(`openssl` habilita HTTPS para `urllib` en Android. `pyjnius` ya lo incluye python-for-android por defecto, no hace falta añadirlo. `INTERNET` y `ACCESS_NETWORK_STATE` ya están en la línea 19.)

- [ ] **Step 4: Crear `tests/_util.py`**

```python
import contextlib
import os
import shutil
import tempfile
import types


@contextlib.contextmanager
def bd_temporal():
    """BD SQLite aislada para un test. Restaura el entorno al salir."""
    d = tempfile.mkdtemp(prefix="medscale-test-")
    prev = os.environ.get("ANDROID_PRIVATE")
    os.environ["ANDROID_PRIVATE"] = d
    try:
        from frontend.database import init_db
        init_db()
        yield d
    finally:
        if prev is None:
            os.environ.pop("ANDROID_PRIVATE", None)
        else:
            os.environ["ANDROID_PRIVATE"] = prev
        shutil.rmtree(d, ignore_errors=True)


def stub_cfg():
    """Config de Firebase falsa para tests (nunca toca la red real)."""
    return types.SimpleNamespace(
        API_KEY="test-key",
        AUTH_DOMAIN="test.firebaseapp.com",
        GOOGLE_WEB_CLIENT_ID="test-client.apps.googleusercontent.com",
    )
```

Nota: `frontend/database.py::_db_path()` devuelve `os.path.join(os.environ["ANDROID_PRIVATE"], "medscale.db")` cuando esa variable está definida, y lee la variable en cada llamada, por eso `bd_temporal()` funciona sin modificar `database.py`.

- [ ] **Step 5: Verificar el scaffolding**

Run: `python -c "import frontend.firebase_config_example if False else None; import ast; ast.parse(open('frontend/firebase_config.example.py').read()); print('example ok')"`
Run: `python -c "from tests._util import bd_temporal, stub_cfg; \
import os; \
_c=bd_temporal(); d=_c.__enter__(); \
from frontend.database import obtener_config, actualizar_config; \
actualizar_config('x','1'); assert obtener_config('x')=='1'; \
_c.__exit__(None,None,None); assert 'ANDROID_PRIVATE' not in os.environ; \
print('bd_temporal ok')"`
Run: `grep -n 'requirements = python3,kivy,openssl' buildozer.spec`
Run: `grep -n 'frontend/firebase_config.py' .gitignore`
Expected: las cuatro líneas imprimen/coinciden sin error.

- [ ] **Step 6: Commit**

```bash
git add frontend/firebase_config.example.py .gitignore buildozer.spec tests/_util.py
git commit -m "chore: scaffolding para autenticación con Firebase (config, gitignore, buildozer, util de tests)"
```

---

### Task 2: `auth.py` — configuración, errores y almacén de sesión

**Files:**
- Create: `frontend/auth.py`
- Create: `tests/test_auth.py`
- Test: `tests/test_auth.py`

**Interfaces:**
- Consumes:
  - `frontend.database.obtener_config(clave) -> str | None`
  - `frontend.database.actualizar_config(clave, valor) -> None`
  - `frontend.database.get_conn() -> sqlite3.Connection`
  - `tests._util.bd_temporal`, `tests._util.stub_cfg`
- Produces (usado por Tasks 3, 6, 7, 8, 9):
  - `class AuthError(Exception)` — el primer arg es un mensaje en español listo para mostrar.
  - `_cfg() -> module|namespace` con `API_KEY`, `AUTH_DOMAIN`, `GOOGLE_WEB_CLIENT_ID`. Lanza `RuntimeError` con instrucciones si falta `frontend/firebase_config.py`. Los tests lo sustituyen por `stub_cfg`.
  - `_traducir_error(code: str) -> str`
  - `_guardar_sesion(resp: dict, nombre: str | None = None) -> dict` — escribe las 6 claves `auth_*` en `configuracion`; devuelve `{"uid", "correo", "nombre"}`. Acepta tanto claves camelCase de Identity Toolkit (`idToken`, `refreshToken`, `expiresIn`, `localId`, `email`, `displayName`) como snake_case del endpoint de refresh (`id_token`, `refresh_token`, `expires_in`, `user_id`).
  - `usuario_actual() -> dict | None` — `{"uid", "correo", "nombre"}` o `None` si no hay `auth_refresh_token`.
  - `cerrar_sesion() -> None` — borra las 6 claves `auth_*`.
  - `_expira_en_segundos() -> float` — segundos hasta que expira el `id_token` guardado (negativo si ya expiró o no hay).
  - `_CLAVES: tuple[str, ...]` — las 6 claves `auth_*`.

- [ ] **Step 1: Escribir los tests que fallan**

```python
# tests/test_auth.py
import time
import unittest

from tests._util import bd_temporal, stub_cfg


class TestSesionStore(unittest.TestCase):
    def setUp(self):
        from frontend import auth
        self.auth = auth
        self._cfg_real = auth._cfg
        auth._cfg = stub_cfg

    def tearDown(self):
        self.auth._cfg = self._cfg_real

    def test_guardar_y_usuario_actual(self):
        with bd_temporal():
            self.auth._guardar_sesion({
                "idToken": "id-1",
                "refreshToken": "ref-1",
                "expiresIn": "3600",
                "localId": "uid-1",
                "email": "doc@correo.com",
            }, nombre="Dra. Ruiz")
            u = self.auth.usuario_actual()
            self.assertEqual(u, {"uid": "uid-1", "correo": "doc@correo.com",
                                 "nombre": "Dra. Ruiz"})

    def test_usuario_actual_sin_sesion_es_none(self):
        with bd_temporal():
            self.assertIsNone(self.auth.usuario_actual())

    def test_cerrar_sesion_borra_claves(self):
        with bd_temporal():
            from frontend.database import obtener_config
            self.auth._guardar_sesion({
                "idToken": "id-1", "refreshToken": "ref-1",
                "expiresIn": "3600", "localId": "uid-1", "email": "a@b.com",
            })
            self.auth.cerrar_sesion()
            self.assertIsNone(self.auth.usuario_actual())
            for c in self.auth._CLAVES:
                self.assertIsNone(obtener_config(c))

    def test_expira_en_segundos(self):
        with bd_temporal():
            self.auth._guardar_sesion({
                "idToken": "id-1", "refreshToken": "ref-1",
                "expiresIn": "3600", "localId": "u", "email": "a@b.com",
            })
            self.assertGreater(self.auth._expira_en_segundos(), 3000)


class TestTraducirError(unittest.TestCase):
    def test_codigos_conocidos(self):
        from frontend import auth
        self.assertEqual(auth._traducir_error("EMAIL_EXISTS"),
                         "Ese correo ya está registrado.")
        self.assertEqual(
            auth._traducir_error("WEAK_PASSWORD : Password should be at least 6 characters"),
            "La contraseña debe tener al menos 6 caracteres.")
        self.assertEqual(auth._traducir_error("INVALID_LOGIN_CREDENTIALS"),
                         "Correo o contraseña incorrectos.")

    def test_codigo_desconocido_se_devuelve_tal_cual(self):
        from frontend import auth
        self.assertEqual(auth._traducir_error("ALGO_RARO"), "ALGO_RARO")

    def test_codigo_vacio(self):
        from frontend import auth
        self.assertEqual(auth._traducir_error(""),
                         "No se pudo completar la operación.")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar los tests para verificar que fallan**

Run: `python -m unittest tests.test_auth -v`
Expected: FAIL / ERROR con `ModuleNotFoundError: No module named 'frontend.auth'`.

- [ ] **Step 3: Escribir `frontend/auth.py` (solo esta parte)**

```python
"""Autenticación con Firebase (Identity Toolkit REST). Sin dependencias de Kivy."""

import time

from frontend.database import actualizar_config, get_conn, obtener_config

_CLAVES = (
    "auth_refresh_token",
    "auth_id_token",
    "auth_expira_en",
    "auth_uid",
    "auth_correo",
    "auth_nombre",
)


class AuthError(Exception):
    """El primer argumento es un mensaje en español listo para mostrar."""


def _cfg():
    try:
        from frontend import firebase_config as fc
    except ModuleNotFoundError:
        raise RuntimeError(
            "Falta frontend/firebase_config.py. Copia "
            "frontend/firebase_config.example.py a frontend/firebase_config.py "
            "y rellena API_KEY, AUTH_DOMAIN y GOOGLE_WEB_CLIENT_ID "
            "(ver docs/firebase-setup.md)."
        )
    return fc


_ERRORES = {
    "EMAIL_EXISTS": "Ese correo ya está registrado.",
    "INVALID_PASSWORD": "Correo o contraseña incorrectos.",
    "INVALID_LOGIN_CREDENTIALS": "Correo o contraseña incorrectos.",
    "EMAIL_NOT_FOUND": "No existe una cuenta con ese correo.",
    "WEAK_PASSWORD": "La contraseña debe tener al menos 6 caracteres.",
    "INVALID_EMAIL": "El correo no es válido.",
    "MISSING_EMAIL": "Escribe tu correo.",
    "MISSING_PASSWORD": "Escribe tu contraseña.",
    "USER_DISABLED": "Esta cuenta está deshabilitada.",
    "TOO_MANY_ATTEMPTS_TRY_LATER": "Demasiados intentos. Intenta más tarde.",
    "TOKEN_EXPIRED": "Tu sesión expiró. Inicia sesión de nuevo.",
    "CREDENTIAL_TOO_OLD_LOGIN_AGAIN": "Tu sesión expiró. Inicia sesión de nuevo.",
}


def _traducir_error(code: str) -> str:
    for clave, msg in _ERRORES.items():
        if code.startswith(clave):
            return msg
    return code or "No se pudo completar la operación."


def _guardar_sesion(resp: dict, nombre: str | None = None) -> dict:
    id_token = resp.get("idToken") or resp.get("id_token") or ""
    refresh = resp.get("refreshToken") or resp.get("refresh_token") or ""
    expires = int(resp.get("expiresIn") or resp.get("expires_in") or 3600)
    uid = resp.get("localId") or resp.get("user_id") or ""
    correo = resp.get("email", "") or obtener_config("auth_correo") or ""
    nom = nombre or resp.get("displayName") or obtener_config("auth_nombre") or ""

    actualizar_config("auth_refresh_token", refresh)
    actualizar_config("auth_id_token", id_token)
    actualizar_config("auth_expira_en", str(int(time.time()) + expires))
    actualizar_config("auth_uid", uid)
    actualizar_config("auth_correo", correo)
    actualizar_config("auth_nombre", nom)
    return {"uid": uid, "correo": correo, "nombre": nom}


def usuario_actual() -> dict | None:
    if not obtener_config("auth_refresh_token"):
        return None
    return {
        "uid": obtener_config("auth_uid") or "",
        "correo": obtener_config("auth_correo") or "",
        "nombre": obtener_config("auth_nombre") or "",
    }


def cerrar_sesion() -> None:
    conn = get_conn()
    conn.executemany(
        "DELETE FROM configuracion WHERE clave = ?", [(c,) for c in _CLAVES]
    )
    conn.commit()
    conn.close()


def _expira_en_segundos() -> float:
    v = obtener_config("auth_expira_en")
    if not v:
        return -1.0
    return float(int(v) - time.time())
```

- [ ] **Step 4: Ejecutar los tests para verificar que pasan**

Run: `python -m unittest tests.test_auth -v`
Expected: PASS (7 tests).

- [ ] **Step 5: Commit**

```bash
git add frontend/auth.py tests/test_auth.py
git commit -m "feat(auth): almacén de sesión y traducción de errores de Firebase"
```

---

### Task 3: `auth.py` — llamadas REST a Firebase

**Files:**
- Modify: `frontend/auth.py` (añadir al final)
- Modify: `tests/test_auth.py` (añadir clases nuevas)
- Test: `tests/test_auth.py`

**Interfaces:**
- Consumes: todo lo de Task 2 (`_cfg`, `_guardar_sesion`, `_traducir_error`, `_expira_en_segundos`, `AuthError`).
- Produces (usado por Tasks 4, 6, 7, 8, 9):
  - `_post(url: str, payload: dict) -> dict` — POST JSON. Lanza `AuthError(mensaje_es)` en `HTTPError`/`URLError`/timeout.
  - `_post_form(url: str, campos: dict) -> dict` — POST `application/x-www-form-urlencoded`. Mismo manejo de errores.
  - `registrar(nombre: str, correo: str, clave: str) -> dict` — `signUp` + `update` (displayName). Guarda sesión. Devuelve `{"uid","correo","nombre"}`.
  - `iniciar_sesion(correo: str, clave: str) -> dict` — `signInWithPassword`. Guarda sesión.
  - `iniciar_con_google(google_id_token: str) -> dict` — `signInWithIdp`. Guarda sesión.
  - `enviar_reset(correo: str) -> None` — `sendOobCode` (PASSWORD_RESET).
  - `refrescar_sesion() -> bool` — `True` si hay sesión usable (refrescándola si hace falta), `False` si no. Nunca lanza.
  - `id_token_valido() -> str | None` — id_token vigente (lo refresca si está por expirar).
  - `demo() -> None` — self-check con `assert`, ejecutable con `python -m frontend.auth`.

- [ ] **Step 1: Escribir los tests que fallan**

Añadir a `tests/test_auth.py`:

```python
class _FakeHTTPError(Exception):
    """Imita urllib.error.HTTPError: tiene .read() con el cuerpo JSON."""
    def __init__(self, body: bytes):
        super().__init__("http error")
        self._body = body

    def read(self):
        return self._body


class TestLlamadasREST(unittest.TestCase):
    def setUp(self):
        from frontend import auth
        self.auth = auth
        self._cfg_real = auth._cfg
        self._post_real = auth._post
        self._post_form_real = auth._post_form
        auth._cfg = stub_cfg

    def tearDown(self):
        self.auth._cfg = self._cfg_real
        self.auth._post = self._post_real
        self.auth._post_form = self._post_form_real

    def test_registrar_guarda_sesion(self):
        llamadas = []

        def fake_post(url, payload):
            llamadas.append(url)
            if url.endswith("signUp?key=test-key"):
                return {"idToken": "id-9", "refreshToken": "ref-9",
                        "expiresIn": "3600", "localId": "uid-9",
                        "email": payload["email"]}
            return {}  # accounts:update

        self.auth._post = fake_post
        with bd_temporal():
            u = self.auth.registrar("Dr. Paz", "paz@correo.com", "secreto1")
            self.assertEqual(u["correo"], "paz@correo.com")
            self.assertEqual(u["nombre"], "Dr. Paz")
            self.assertEqual(self.auth.usuario_actual()["uid"], "uid-9")
        self.assertTrue(any("signUp" in u for u in llamadas))
        self.assertTrue(any("update" in u for u in llamadas))

    def test_iniciar_sesion_error_credenciales(self):
        def fake_post(url, payload):
            raise self.auth.AuthError(self.auth._traducir_error("INVALID_PASSWORD"))

        self.auth._post = fake_post
        with bd_temporal():
            with self.assertRaises(self.auth.AuthError) as ctx:
                self.auth.iniciar_sesion("x@y.com", "malo")
            self.assertEqual(str(ctx.exception), "Correo o contraseña incorrectos.")

    def test_iniciar_con_google_guarda_sesion(self):
        def fake_post(url, payload):
            self.assertIn("signInWithIdp", url)
            self.assertIn("id_token=GTOKEN", payload["postBody"])
            return {"idToken": "id-g", "refreshToken": "ref-g",
                    "expiresIn": "3600", "localId": "uid-g",
                    "email": "g@correo.com", "displayName": "Cuenta Google"}

        self.auth._post = fake_post
        with bd_temporal():
            u = self.auth.iniciar_con_google("GTOKEN")
            self.assertEqual(u["nombre"], "Cuenta Google")

    def test_refrescar_sesion_sin_token(self):
        with bd_temporal():
            self.assertFalse(self.auth.refrescar_sesion())

    def test_refrescar_sesion_token_vigente_no_llama_red(self):
        def boom(*a, **k):
            raise AssertionError("no debería llamar a la red")

        self.auth._post_form = boom
        with bd_temporal():
            self.auth._guardar_sesion({"idToken": "i", "refreshToken": "r",
                                       "expiresIn": "3600", "localId": "u",
                                       "email": "a@b.com"})
            self.assertTrue(self.auth.refrescar_sesion())

    def test_refrescar_sesion_token_expirado_ok(self):
        def fake_form(url, campos):
            return {"id_token": "nuevo", "refresh_token": "nuevo-ref",
                    "expires_in": "3600", "user_id": "u"}

        self.auth._post_form = fake_form
        with bd_temporal():
            from frontend.database import actualizar_config, obtener_config
            self.auth._guardar_sesion({"idToken": "viejo", "refreshToken": "r",
                                       "expiresIn": "3600", "localId": "u",
                                       "email": "a@b.com"})
            actualizar_config("auth_expira_en", "0")  # forzar expirado
            self.assertTrue(self.auth.refrescar_sesion())
            self.assertEqual(obtener_config("auth_id_token"), "nuevo")

    def test_refrescar_sesion_expirado_sin_red_devuelve_false(self):
        def fake_form(url, campos):
            raise self.auth.AuthError("Sin conexión. Revisa tu internet.")

        self.auth._post_form = fake_form
        with bd_temporal():
            from frontend.database import actualizar_config
            self.auth._guardar_sesion({"idToken": "v", "refreshToken": "r",
                                       "expiresIn": "3600", "localId": "u",
                                       "email": "a@b.com"})
            actualizar_config("auth_expira_en", "0")
            self.assertFalse(self.auth.refrescar_sesion())

    def test_post_traduce_httperror(self):
        import urllib.error
        from frontend import auth

        real_urlopen = auth.urllib.request.urlopen

        def fake_urlopen(req, timeout=None):
            raise urllib.error.HTTPError(
                req.full_url, 400, "Bad Request", {},
                _fake_body(b'{"error":{"message":"EMAIL_EXISTS"}}'))

        auth.urllib.request.urlopen = fake_urlopen
        try:
            with self.assertRaises(auth.AuthError) as ctx:
                auth._post("https://x/y", {"a": 1})
            self.assertEqual(str(ctx.exception), "Ese correo ya está registrado.")
        finally:
            auth.urllib.request.urlopen = real_urlopen


def _fake_body(data: bytes):
    import io
    return io.BytesIO(data)
```

- [ ] **Step 2: Ejecutar los tests para verificar que fallan**

Run: `python -m unittest tests.test_auth -v`
Expected: FAIL con `AttributeError: module 'frontend.auth' has no attribute '_post'` (y similares).

- [ ] **Step 3: Añadir la implementación a `frontend/auth.py`**

Añadir estos imports al principio del archivo (junto a `import time`):

```python
import json
import urllib.error
import urllib.parse
import urllib.request
```

Añadir al final del archivo:

```python
_TIMEOUT = 15
_IDENTITY = "https://identitytoolkit.googleapis.com/v1/accounts:"
_SECURETOKEN = "https://securetoken.googleapis.com/v1/token"


def _codigo_de_error(raw: bytes) -> str:
    try:
        body = json.loads(raw.decode())
    except Exception:
        return ""
    err = body.get("error")
    if isinstance(err, dict):
        return err.get("message", "") or ""
    return body.get("error_description", "") or ""


def _post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise AuthError(_traducir_error(_codigo_de_error(e.read())))
    except (urllib.error.URLError, TimeoutError, OSError):
        raise AuthError("Sin conexión. Revisa tu internet.")


def _post_form(url: str, campos: dict) -> dict:
    data = urllib.parse.urlencode(campos).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise AuthError(_traducir_error(_codigo_de_error(e.read())))
    except (urllib.error.URLError, TimeoutError, OSError):
        raise AuthError("Sin conexión. Revisa tu internet.")


def _url(metodo: str) -> str:
    return f"{_IDENTITY}{metodo}?key={_cfg().API_KEY}"


def registrar(nombre: str, correo: str, clave: str) -> dict:
    resp = _post(_url("signUp"), {
        "email": correo, "password": clave, "returnSecureToken": True,
    })
    try:
        _post(_url("update"), {
            "idToken": resp["idToken"],
            "displayName": nombre,
            "returnSecureToken": False,
        })
    except AuthError:
        pass  # el nombre es secundario; la cuenta ya quedó creada
    return _guardar_sesion(resp, nombre=nombre)


def iniciar_sesion(correo: str, clave: str) -> dict:
    resp = _post(_url("signInWithPassword"), {
        "email": correo, "password": clave, "returnSecureToken": True,
    })
    return _guardar_sesion(resp)


def iniciar_con_google(google_id_token: str) -> dict:
    resp = _post(_url("signInWithIdp"), {
        "postBody": f"id_token={google_id_token}&providerId=google.com",
        "requestUri": f"https://{_cfg().AUTH_DOMAIN}",
        "returnSecureToken": True,
    })
    return _guardar_sesion(resp)


def enviar_reset(correo: str) -> None:
    _post(_url("sendOobCode"), {"requestType": "PASSWORD_RESET", "email": correo})


def refrescar_sesion() -> bool:
    if not obtener_config("auth_refresh_token"):
        return False
    if _expira_en_segundos() > 300:
        return True
    try:
        resp = _post_form(f"{_SECURETOKEN}?key={_cfg().API_KEY}", {
            "grant_type": "refresh_token",
            "refresh_token": obtener_config("auth_refresh_token"),
        })
    except AuthError:
        return _expira_en_segundos() > 0
    if "id_token" not in resp:
        cerrar_sesion()
        return False
    _guardar_sesion(resp)
    return True


def id_token_valido() -> str | None:
    refrescar_sesion()
    return obtener_config("auth_id_token")


def demo() -> None:
    import os
    import tempfile

    d = tempfile.mkdtemp(prefix="medscale-authdemo-")
    os.environ["ANDROID_PRIVATE"] = d
    from frontend.database import init_db
    init_db()

    assert usuario_actual() is None
    _guardar_sesion({"idToken": "i", "refreshToken": "r", "expiresIn": "10",
                     "localId": "u", "email": "demo@correo.com"}, nombre="Demo")
    assert usuario_actual()["correo"] == "demo@correo.com"
    assert _expira_en_segundos() <= 10
    cerrar_sesion()
    assert usuario_actual() is None
    print("auth.demo OK")


if __name__ == "__main__":
    demo()
```

- [ ] **Step 4: Ejecutar los tests para verificar que pasan**

Run: `python -m unittest tests.test_auth -v`
Expected: PASS (todos, ~15 tests).

- [ ] **Step 5: Ejecutar el self-check**

Run: `python -m frontend.auth`
Expected: imprime `auth.demo OK`.

- [ ] **Step 6: Commit**

```bash
git add frontend/auth.py tests/test_auth.py
git commit -m "feat(auth): registro, login, login con Google y refresco de sesión (Firebase REST)"
```

---

### Task 4: `google_oauth.py` — obtención del id_token de Google

**Files:**
- Create: `frontend/google_oauth.py`
- Modify: `tests/test_auth.py` (añadir `TestGoogleOAuthUrl`) — o crear `tests/test_google_oauth.py`
- Test: `tests/test_google_oauth.py`

**Interfaces:**
- Consumes: `frontend.auth.AuthError`, `frontend.auth._cfg`.
- Produces (usado por Tasks 6, 7):
  - `_build_auth_url(redirect_uri: str, client_id: str, nonce: str) -> str` — URL de autorización de Google (`response_type=id_token`, `scope=openid email profile`, `prompt=select_account`).
  - `_en_android() -> bool` — `True` si corre dentro de una APK (env `ANDROID_ARGUMENT` presente).
  - `obtener_id_token_google() -> str` — bloqueante (se llama desde un hilo). Devuelve el `id_token` de Google o lanza `AuthError` (incluye cancelación por el usuario).

- [ ] **Step 1: Escribir el test que falla**

```python
# tests/test_google_oauth.py
import unittest
import urllib.parse


class TestBuildAuthUrl(unittest.TestCase):
    def test_url_contiene_parametros_oauth(self):
        from frontend.google_oauth import _build_auth_url
        url = _build_auth_url("https://x.firebaseapp.com/__/auth/handler",
                              "cid.apps.googleusercontent.com", "abc123")
        parsed = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(parsed.netloc, "accounts.google.com")
        self.assertEqual(parsed.path, "/o/oauth2/v2/auth")
        self.assertEqual(q["response_type"], ["id_token"])
        self.assertEqual(q["client_id"], ["cid.apps.googleusercontent.com"])
        self.assertEqual(q["redirect_uri"],
                         ["https://x.firebaseapp.com/__/auth/handler"])
        self.assertEqual(q["scope"], ["openid email profile"])
        self.assertEqual(q["nonce"], ["abc123"])
        self.assertEqual(q["prompt"], ["select_account"])

    def test_en_android_falso_en_desarrollo(self):
        import os
        from frontend.google_oauth import _en_android
        os.environ.pop("ANDROID_ARGUMENT", None)
        self.assertFalse(_en_android())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar el test para verificar que falla**

Run: `python -m unittest tests.test_google_oauth -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'frontend.google_oauth'`.

- [ ] **Step 3: Escribir `frontend/google_oauth.py`**

```python
"""Obtención de un id_token de Google para canjear con Firebase (signInWithIdp).

Android: WebView nativo vía pyjnius que intercepta el redirect.
Escritorio (solo desarrollo): navegador del sistema + servidor local que
captura el fragmento con un rebote de JavaScript.
"""

import os
import secrets
import threading
import urllib.parse

from frontend.auth import AuthError, _cfg

_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
_PUERTO_LOCAL = 8765
_TIMEOUT_ESCRITORIO = 120


def _build_auth_url(redirect_uri: str, client_id: str, nonce: str) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "id_token",
        "scope": "openid email profile",
        "nonce": nonce,
        "prompt": "select_account",
    }
    return _AUTH_ENDPOINT + "?" + urllib.parse.urlencode(params)


def _en_android() -> bool:
    return "ANDROID_ARGUMENT" in os.environ


def _id_token_del_fragmento(url: str) -> str:
    frag = url.split("#", 1)[1] if "#" in url else ""
    q = urllib.parse.parse_qs(frag)
    return (q.get("id_token") or [""])[0]


def obtener_id_token_google() -> str:
    client_id = _cfg().GOOGLE_WEB_CLIENT_ID
    nonce = secrets.token_urlsafe(16)
    if _en_android():
        redirect = f"https://{_cfg().AUTH_DOMAIN}/__/auth/handler"
        url = _build_auth_url(redirect, client_id, nonce)
        return _flujo_android(url, redirect)
    redirect = f"http://127.0.0.1:{_PUERTO_LOCAL}"
    url = _build_auth_url(redirect, client_id, nonce)
    return _flujo_escritorio(url, redirect)


# --- Escritorio (desarrollo) -------------------------------------------------

def _flujo_escritorio(auth_url: str, redirect: str) -> str:
    import http.server
    import webbrowser

    holder = {}
    done = threading.Event()

    class _Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/token":
                q = urllib.parse.parse_qs(parsed.query)
                holder["token"] = (q.get("id_token") or [""])[0]
                self._html("Listo. Puedes volver a la app.")
                done.set()
            else:
                # el id_token viene en el fragmento (#...), invisible al servidor:
                # lo rebotamos como query string.
                self._html(
                    "<script>location.replace('/token?'+"
                    "location.hash.slice(1))</script>"
                )

        def _html(self, cuerpo):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<!doctype html>{cuerpo}".encode())

    srv = http.server.HTTPServer(("127.0.0.1", _PUERTO_LOCAL), _Handler)
    hilo = threading.Thread(target=srv.serve_forever, daemon=True)
    hilo.start()
    try:
        webbrowser.open(auth_url)
        ok = done.wait(timeout=_TIMEOUT_ESCRITORIO)
    finally:
        srv.shutdown()
    token = holder.get("token")
    if not ok or not token:
        raise AuthError("No se pudo completar el inicio con Google.")
    return token


# --- Android ---------------------------------------------------------------

def _flujo_android(auth_url: str, redirect: str) -> str:
    from jnius import PythonJavaClass, autoclass, java_method
    from android.runnable import run_on_ui_thread

    WebView = autoclass("android.webkit.WebView")
    LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    activity = PythonActivity.mActivity

    estado = {}
    done = threading.Event()

    class _Client(PythonJavaClass):
        __javainterfaces__ = ["android/webkit/WebViewClient"]
        __javacontext__ = "app"

        @java_method("(Landroid/webkit/WebView;Ljava/lang/String;)Z")
        def shouldOverrideUrlLoading(self, view, url):
            if url.startswith(redirect):
                estado["token"] = _id_token_del_fragmento(url)
                done.set()
                _quitar()
                return True
            return False

    @run_on_ui_thread
    def _montar():
        wv = WebView(activity)
        wv.getSettings().setJavaScriptEnabled(True)
        wv.getSettings().setDomStorageEnabled(True)
        wv.setWebViewClient(_Client())
        activity.addContentView(wv, LayoutParams(-1, -1))
        estado["wv"] = wv
        wv.loadUrl(auth_url)

    @run_on_ui_thread
    def _quitar():
        wv = estado.get("wv")
        if wv is not None:
            parent = wv.getParent()
            if parent is not None:
                autoclass("android.view.ViewGroup")(parent).removeView(wv) \
                    if False else parent.removeView(wv)
            estado["wv"] = None

    _montar()
    ok = done.wait(timeout=_TIMEOUT_ESCRITORIO)
    if not ok:
        run_on_ui_thread(_quitar)()
        raise AuthError("Inicio con Google cancelado.")
    token = estado.get("token")
    if not token:
        raise AuthError("No se pudo completar el inicio con Google.")
    return token
```

Nota para el implementador: `_flujo_android` **no se puede probar sin un dispositivo/APK**. Su verificación es manual (Task 10). Si en el dispositivo el `removeView` da problemas de tipo, sustituir la línea marcada por la variante con cast explícito a `android.view.ViewGroup`. El riesgo y la alternativa (Chrome Custom Tabs + `intent-filter`) están documentados en el spec §10.

- [ ] **Step 4: Ejecutar el test para verificar que pasa**

Run: `python -m unittest tests.test_google_oauth -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add frontend/google_oauth.py tests/test_google_oauth.py
git commit -m "feat(auth): flujo OAuth de Google (WebView Android + fallback escritorio)"
```

---

### Task 5: `widgets/ui.py` — constantes y helpers de formulario

**Files:**
- Modify: `frontend/widgets/ui.py` (añadir; no tocar lo existente)
- Create: `tests/test_ui_widgets.py`
- Test: `tests/test_ui_widgets.py`

**Interfaces:**
- Consumes: nada nuevo.
- Produces (usado por Tasks 6, 7):
  - Constantes: `C_PRIMARY`, `C_PRIMARY_DARK`, `C_CARD`, `C_TEXT_MAIN`, `C_TEXT_SEC`, `C_ERROR`, `C_FIELD_BG`, `C_WHITE` (todas listas RGBA de `get_color_from_hex`).
  - `text_field(hint: str, password: bool = False) -> kivy.uix.textinput.TextInput`
  - `primary_button(text: str) -> kivy.uix.button.Button`
  - `outline_button(text: str) -> kivy.uix.button.Button`
  - `link_label(text: str, on_press=None) -> kivy.uix.button.Button` — botón transparente que parece enlace; `on_press` es un callable sin argumentos.

- [ ] **Step 1: Escribir el test que falla**

```python
# tests/test_ui_widgets.py
import unittest


class TestUiWidgets(unittest.TestCase):
    def test_helpers_devuelven_widgets(self):
        try:
            from kivy.uix.textinput import TextInput
            from kivy.uix.button import Button
            from frontend.widgets import ui
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")

        campo = ui.text_field("Correo")
        self.assertIsInstance(campo, TextInput)
        self.assertFalse(campo.password)
        self.assertTrue(ui.text_field("Clave", password=True).password)

        self.assertIsInstance(ui.primary_button("Entrar"), Button)
        self.assertIsInstance(ui.outline_button("Google"), Button)

        pulsado = []
        enlace = ui.link_label("Regístrate", on_press=lambda: pulsado.append(1))
        self.assertIsInstance(enlace, Button)
        enlace.dispatch("on_press")
        self.assertEqual(pulsado, [1])

    def test_constantes_de_color(self):
        try:
            from frontend.widgets import ui
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")
        for nombre in ("C_PRIMARY", "C_TEXT_MAIN", "C_ERROR", "C_FIELD_BG",
                       "C_WHITE", "C_PRIMARY_DARK", "C_CARD", "C_TEXT_SEC"):
            valor = getattr(ui, nombre)
            self.assertEqual(len(valor), 4)  # RGBA


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar el test para verificar que falla**

Run: `python -m unittest tests.test_ui_widgets -v`
Expected: FAIL con `AttributeError: module 'frontend.widgets.ui' has no attribute 'text_field'`.

- [ ] **Step 3: Añadir a `frontend/widgets/ui.py`**

Añadir imports arriba (junto a los existentes):

```python
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Line
```

(`BoxLayout`, `Label`, `get_color_from_hex`, `dp`, `sp`, `Color`, `Rectangle` ya están importados en el archivo.)

Añadir al final:

```python
C_PRIMARY      = get_color_from_hex("#1976D2")
C_PRIMARY_DARK = get_color_from_hex("#1565C0")
C_CARD         = get_color_from_hex("#FFFFFF")
C_TEXT_MAIN    = get_color_from_hex("#1A1A2E")
C_TEXT_SEC     = get_color_from_hex("#6B7280")
C_ERROR        = get_color_from_hex("#D32F2F")
C_FIELD_BG     = get_color_from_hex("#F0F2F5")
C_WHITE        = get_color_from_hex("#FFFFFF")


def text_field(hint, password=False):
    return TextInput(
        hint_text=hint,
        multiline=False,
        password=password,
        write_tab=False,
        size_hint_y=None,
        height=dp(46),
        font_size=sp(14),
        padding=[dp(12), dp(12)],
        background_normal="",
        background_active="",
        background_color=C_FIELD_BG,
        cursor_color=C_PRIMARY,
        foreground_color=C_TEXT_MAIN,
        hint_text_color=C_TEXT_SEC,
    )


def primary_button(text):
    return Button(
        text=text,
        size_hint_y=None,
        height=dp(50),
        font_size=sp(16),
        bold=True,
        background_normal="",
        background_color=C_PRIMARY,
        color=C_WHITE,
    )


def outline_button(text):
    btn = Button(
        text=text,
        size_hint_y=None,
        height=dp(48),
        font_size=sp(15),
        bold=True,
        background_normal="",
        background_color=(0, 0, 0, 0),
        color=C_PRIMARY,
    )
    with btn.canvas.after:
        Color(*C_PRIMARY)
        btn._borde = Line(width=1.2)

    def _upd(*_):
        btn._borde.rounded_rectangle = (btn.x, btn.y, btn.width, btn.height, dp(8))

    btn.bind(pos=_upd, size=_upd)
    return btn


def link_label(text, on_press=None):
    btn = Button(
        text=text,
        font_size=sp(13),
        color=C_PRIMARY,
        size_hint_y=None,
        height=dp(24),
        background_normal="",
        background_color=(0, 0, 0, 0),
    )
    if on_press is not None:
        btn.bind(on_press=lambda *_: on_press())
    return btn
```

- [ ] **Step 4: Ejecutar el test para verificar que pasa**

Run: `python -m unittest tests.test_ui_widgets -v`
Expected: PASS (2 tests) o SKIP si Kivy no está.

- [ ] **Step 5: Commit**

```bash
git add frontend/widgets/ui.py tests/test_ui_widgets.py
git commit -m "feat(ui): helpers de formulario y constantes de color compartidas"
```

---

### Task 6: `screens/login_screen.py`

**Files:**
- Create: `frontend/screens/login_screen.py`
- Modify: `tests/test_frontend.py` (añadir test)
- Test: `tests/test_frontend.py`

**Interfaces:**
- Consumes: `frontend.auth` (`iniciar_sesion`, `iniciar_con_google`, `enviar_reset`, `AuthError`), `frontend.google_oauth.obtener_id_token_google`, `frontend.widgets.ui` (`text_field`, `primary_button`, `outline_button`, `link_label`, `C_TEXT_MAIN`, `C_ERROR`).
- Produces (usado por Task 8): `class LoginScreen(kivy.uix.screenmanager.Screen)`; se registra con `name="login"`. Al autenticar con éxito hace `self.manager.current = "home"`. El enlace "Regístrate" hace `self.manager.current = "register"`.

- [ ] **Step 1: Escribir el test que falla**

Añadir a `tests/test_frontend.py`:

```python
    def test_login_screen_importable(self):
        try:
            from frontend.screens.login_screen import LoginScreen
            screen = LoginScreen(name="login")
            self.assertEqual(screen.name, "login")
            self.assertTrue(hasattr(screen, "_correo"))
            self.assertTrue(hasattr(screen, "_clave"))
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")
```

- [ ] **Step 2: Ejecutar el test para verificar que falla**

Run: `python -m unittest tests.test_frontend.TestFrontend.test_login_screen_importable -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'frontend.screens.login_screen'`.

- [ ] **Step 3: Escribir `frontend/screens/login_screen.py`**

```python
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from frontend import auth, google_oauth
from frontend.widgets.ui import (
    C_ERROR,
    C_TEXT_MAIN,
    link_label,
    outline_button,
    primary_button,
    text_field,
)

_BG = "frontend/assets/iniciose.jpeg"


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raiz = FloatLayout()
        raiz.add_widget(Image(
            source=_BG, allow_stretch=True, keep_ratio=False,
            size_hint=(1, 1), pos_hint={"x": 0, "y": 0},
        ))

        form = BoxLayout(
            orientation="vertical", spacing=dp(10),
            size_hint=(0.82, None),
            pos_hint={"center_x": 0.5, "center_y": 0.44},
        )
        form.bind(minimum_height=form.setter("height"))

        form.add_widget(Label(
            text="Iniciar sesión", font_size=sp(20), bold=True,
            color=C_TEXT_MAIN, size_hint_y=None, height=dp(40),
        ))

        self._correo = text_field("Correo electrónico")
        self._clave = text_field("Contraseña", password=True)
        form.add_widget(self._correo)
        form.add_widget(self._clave)

        self._msg = Label(
            text="", font_size=sp(12), color=C_ERROR,
            size_hint_y=None, height=dp(20), opacity=0,
        )
        form.add_widget(self._msg)

        self._btn = primary_button("Iniciar sesión")
        self._btn.bind(on_press=lambda *_: self._ingresar())
        form.add_widget(self._btn)

        self._btn_google = outline_button("Continuar con Google")
        self._btn_google.bind(on_press=lambda *_: self._google())
        form.add_widget(self._btn_google)

        form.add_widget(link_label("¿Olvidaste tu contraseña?",
                                   on_press=self._reset))

        fila = BoxLayout(size_hint_y=None, height=dp(26), spacing=dp(4))
        fila.add_widget(Label(
            text="¿No tienes cuenta?", font_size=sp(13), color=C_TEXT_MAIN,
            halign="right", valign="middle",
        ))
        fila.add_widget(link_label(
            "Regístrate",
            on_press=lambda: setattr(self.manager, "current", "register"),
        ))
        form.add_widget(fila)

        raiz.add_widget(form)
        self.add_widget(raiz)

    def on_pre_enter(self):
        self._correo.text = ""
        self._clave.text = ""
        self._mostrar_msg("")

    # -- helpers de estado --

    def _mostrar_msg(self, texto, error=True):
        self._msg.text = texto
        self._msg.color = C_ERROR if error else (0.05, 0.43, 0.43, 1)
        self._msg.opacity = 1 if texto else 0

    def _ocupado(self, si, etiqueta="Iniciar sesión"):
        self._btn.disabled = si
        self._btn_google.disabled = si
        self._btn.text = "Ingresando…" if si else etiqueta

    def _ok(self):
        self._ocupado(False)
        self.manager.current = "home"

    def _fallo(self, msg):
        self._ocupado(False)
        self._mostrar_msg(msg)

    # -- acciones --

    def _ingresar(self):
        correo = self._correo.text.strip()
        clave = self._clave.text
        if not correo or not clave:
            self._mostrar_msg("Escribe tu correo y contraseña.")
            return
        self._mostrar_msg("")
        self._ocupado(True)
        threading.Thread(
            target=self._trabajo_login, args=(correo, clave), daemon=True
        ).start()

    def _trabajo_login(self, correo, clave):
        try:
            auth.iniciar_sesion(correo, clave)
            Clock.schedule_once(lambda *_: self._ok())
        except auth.AuthError as e:
            Clock.schedule_once(lambda *_, m=str(e): self._fallo(m))

    def _google(self):
        self._mostrar_msg("")
        self._ocupado(True)
        threading.Thread(target=self._trabajo_google, daemon=True).start()

    def _trabajo_google(self):
        try:
            token = google_oauth.obtener_id_token_google()
            auth.iniciar_con_google(token)
            Clock.schedule_once(lambda *_: self._ok())
        except auth.AuthError as e:
            Clock.schedule_once(lambda *_, m=str(e): self._fallo(m))

    def _reset(self):
        correo = self._correo.text.strip()
        if not correo:
            self._mostrar_msg("Escribe tu correo primero.")
            return

        def trabajo():
            try:
                auth.enviar_reset(correo)
                Clock.schedule_once(lambda *_: self._mostrar_msg(
                    "Te enviamos un correo para restablecer la contraseña.",
                    error=False))
            except auth.AuthError as e:
                Clock.schedule_once(lambda *_, m=str(e): self._mostrar_msg(m))

        threading.Thread(target=trabajo, daemon=True).start()
```

- [ ] **Step 4: Ejecutar el test para verificar que pasa**

Run: `python -m unittest tests.test_frontend.TestFrontend.test_login_screen_importable -v`
Expected: PASS o SKIP si Kivy no está.

- [ ] **Step 5: Commit**

```bash
git add frontend/screens/login_screen.py tests/test_frontend.py
git commit -m "feat(auth): pantalla de inicio de sesión con estilo de iniciose.jpeg"
```

---

### Task 7: `screens/register_screen.py`

**Files:**
- Create: `frontend/screens/register_screen.py`
- Modify: `tests/test_frontend.py` (añadir test)
- Test: `tests/test_frontend.py`

**Interfaces:**
- Consumes: `frontend.auth` (`registrar`, `iniciar_con_google`, `AuthError`), `frontend.google_oauth.obtener_id_token_google`, `frontend.widgets.ui` (`text_field`, `primary_button`, `outline_button`, `link_label`, `C_TEXT_MAIN`, `C_ERROR`).
- Produces (usado por Task 8): `class RegisterScreen(Screen)`; se registra con `name="register"`. Al crear cuenta con éxito hace `self.manager.current = "home"`. El enlace "Ya tengo cuenta" hace `self.manager.current = "login"`.

- [ ] **Step 1: Escribir el test que falla**

Añadir a `tests/test_frontend.py`:

```python
    def test_register_screen_importable(self):
        try:
            from frontend.screens.register_screen import RegisterScreen
            screen = RegisterScreen(name="register")
            self.assertEqual(screen.name, "register")
            for attr in ("_nombre", "_correo", "_clave", "_clave2"):
                self.assertTrue(hasattr(screen, attr))
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")

    def test_register_valida_localmente(self):
        try:
            from frontend.screens.register_screen import RegisterScreen
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")
        screen = RegisterScreen(name="register")
        screen._nombre.text = "Ana"
        screen._correo.text = "ana@correo.com"
        screen._clave.text = "abc123"
        screen._clave2.text = "otra"
        # claves distintas -> mensaje de error, sin lanzar
        screen._crear()
        self.assertIn("coinciden", screen._msg.text.lower())
```

- [ ] **Step 2: Ejecutar los tests para verificar que fallan**

Run: `python -m unittest tests.test_frontend -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'frontend.screens.register_screen'`.

- [ ] **Step 3: Escribir `frontend/screens/register_screen.py`**

```python
import threading

from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from frontend import auth, google_oauth
from frontend.widgets.ui import (
    C_ERROR,
    C_TEXT_MAIN,
    link_label,
    outline_button,
    primary_button,
    text_field,
)

_BG = "frontend/assets/iniciose.jpeg"


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raiz = FloatLayout()
        raiz.add_widget(Image(
            source=_BG, allow_stretch=True, keep_ratio=False,
            size_hint=(1, 1), pos_hint={"x": 0, "y": 0},
        ))

        form = BoxLayout(
            orientation="vertical", spacing=dp(9),
            size_hint=(0.82, None),
            pos_hint={"center_x": 0.5, "center_y": 0.44},
        )
        form.bind(minimum_height=form.setter("height"))

        form.add_widget(Label(
            text="Crear cuenta", font_size=sp(20), bold=True,
            color=C_TEXT_MAIN, size_hint_y=None, height=dp(38),
        ))

        self._nombre = text_field("Nombre")
        self._correo = text_field("Correo electrónico")
        self._clave = text_field("Contraseña", password=True)
        self._clave2 = text_field("Confirmar contraseña", password=True)
        for w in (self._nombre, self._correo, self._clave, self._clave2):
            form.add_widget(w)

        self._msg = Label(
            text="", font_size=sp(12), color=C_ERROR,
            size_hint_y=None, height=dp(20), opacity=0,
        )
        form.add_widget(self._msg)

        self._btn = primary_button("Crear cuenta")
        self._btn.bind(on_press=lambda *_: self._crear())
        form.add_widget(self._btn)

        self._btn_google = outline_button("Continuar con Google")
        self._btn_google.bind(on_press=lambda *_: self._google())
        form.add_widget(self._btn_google)

        fila = BoxLayout(size_hint_y=None, height=dp(26), spacing=dp(4))
        fila.add_widget(Label(
            text="¿Ya tienes cuenta?", font_size=sp(13), color=C_TEXT_MAIN,
            halign="right", valign="middle",
        ))
        fila.add_widget(link_label(
            "Inicia sesión",
            on_press=lambda: setattr(self.manager, "current", "login"),
        ))
        form.add_widget(fila)

        raiz.add_widget(form)
        self.add_widget(raiz)

    def on_pre_enter(self):
        for w in (self._nombre, self._correo, self._clave, self._clave2):
            w.text = ""
        self._mostrar_msg("")

    def _mostrar_msg(self, texto):
        self._msg.text = texto
        self._msg.opacity = 1 if texto else 0

    def _ocupado(self, si, etiqueta="Crear cuenta"):
        self._btn.disabled = si
        self._btn_google.disabled = si
        self._btn.text = "Creando…" if si else etiqueta

    def _ok(self):
        self._ocupado(False)
        self.manager.current = "home"

    def _fallo(self, msg):
        self._ocupado(False)
        self._mostrar_msg(msg)

    def _crear(self):
        nombre = self._nombre.text.strip()
        correo = self._correo.text.strip()
        clave = self._clave.text
        clave2 = self._clave2.text
        if not nombre or not correo or not clave:
            self._mostrar_msg("Completa todos los campos.")
            return
        if "@" not in correo or "." not in correo:
            self._mostrar_msg("El correo no es válido.")
            return
        if len(clave) < 6:
            self._mostrar_msg("La contraseña debe tener al menos 6 caracteres.")
            return
        if clave != clave2:
            self._mostrar_msg("Las contraseñas no coinciden.")
            return
        self._mostrar_msg("")
        self._ocupado(True)
        threading.Thread(
            target=self._trabajo, args=(nombre, correo, clave), daemon=True
        ).start()

    def _trabajo(self, nombre, correo, clave):
        try:
            auth.registrar(nombre, correo, clave)
            Clock.schedule_once(lambda *_: self._ok())
        except auth.AuthError as e:
            Clock.schedule_once(lambda *_, m=str(e): self._fallo(m))

    def _google(self):
        self._mostrar_msg("")
        self._ocupado(True)
        threading.Thread(target=self._trabajo_google, daemon=True).start()

    def _trabajo_google(self):
        try:
            token = google_oauth.obtener_id_token_google()
            auth.iniciar_con_google(token)
            Clock.schedule_once(lambda *_: self._ok())
        except auth.AuthError as e:
            Clock.schedule_once(lambda *_, m=str(e): self._fallo(m))
```

- [ ] **Step 4: Ejecutar los tests para verificar que pasan**

Run: `python -m unittest tests.test_frontend -v`
Expected: PASS (o SKIP si Kivy no está).

- [ ] **Step 5: Commit**

```bash
git add frontend/screens/register_screen.py tests/test_frontend.py
git commit -m "feat(auth): pantalla de registro"
```

---

### Task 8: Compuerta de sesión en `main.py`

**Files:**
- Modify: `frontend/main.py`
- Modify: `tests/test_frontend.py` (añadir test)
- Test: `tests/test_frontend.py`

**Interfaces:**
- Consumes: `frontend.auth.refrescar_sesion`, `LoginScreen`, `RegisterScreen`.
- Produces: al arrancar, el `ScreenManager` contiene las pantallas `login` y `register`, y `sm.current` es `"home"` si `auth.refrescar_sesion()` devuelve `True`, o `"login"` en caso contrario (o ante cualquier excepción).

- [ ] **Step 1: Escribir el test que falla**

Añadir a `tests/test_frontend.py`:

```python
    def test_arranque_sin_sesion_muestra_login(self):
        try:
            from frontend.main import MedScaleORLApp
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")
        from tests._util import bd_temporal
        with bd_temporal():
            sm = MedScaleORLApp().build()
            nombres = {s.name for s in sm.screens}
            self.assertIn("login", nombres)
            self.assertIn("register", nombres)
            self.assertEqual(sm.current, "login")
```

- [ ] **Step 2: Ejecutar el test para verificar que falla**

Run: `python -m unittest tests.test_frontend.TestFrontend.test_arranque_sin_sesion_muestra_login -v`
Expected: FAIL (`AssertionError: 'login' not found in ...` o `sm.current == 'home'`).

- [ ] **Step 3: Modificar `frontend/main.py`**

En el bloque de imports de pantallas (después de la línea `from frontend.database import init_db`), añadir:

```python
from frontend import auth
from frontend.screens.login_screen import LoginScreen
from frontend.screens.register_screen import RegisterScreen
```

Dentro de `build()`, justo después de `init_db()` y de crear `sm = ScreenManager(...)`, añadir estas dos líneas **antes** de `sm.add_widget(HomeScreen(name="home"))`:

```python
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
```

Y sustituir el `return sm` final por:

```python
        try:
            sm.current = "home" if auth.refrescar_sesion() else "login"
        except Exception:
            sm.current = "login"
        return sm
```

- [ ] **Step 4: Ejecutar los tests para verificar que pasan**

Run: `python -m unittest tests.test_frontend -v`
Expected: PASS (todos) o SKIP si Kivy no está.

- [ ] **Step 5: Commit**

```bash
git add frontend/main.py tests/test_frontend.py
git commit -m "feat(auth): abrir en login y auto-entrar si hay sesión válida"
```

---

### Task 9: Cerrar sesión y datos reales en el perfil

**Files:**
- Modify: `frontend/screens/perfil_screen.py`
- Modify: `tests/test_frontend.py` (añadir test)
- Test: `tests/test_frontend.py`

**Interfaces:**
- Consumes: `frontend.auth.usuario_actual`, `frontend.auth.cerrar_sesion`, `frontend.widgets.app_header.navigate_to`.
- Produces: `PerfilScreen` muestra el nombre y correo de `auth.usuario_actual()`; tiene un método `_cerrar_sesion()` que llama `auth.cerrar_sesion()` y navega a `"login"`.

- [ ] **Step 1: Escribir el test que falla**

Añadir a `tests/test_frontend.py`:

```python
    def test_perfil_tiene_cerrar_sesion(self):
        try:
            from frontend.screens.perfil_screen import PerfilScreen
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")
        self.assertTrue(hasattr(PerfilScreen, "_cerrar_sesion"))

    def test_perfil_cerrar_sesion_borra_sesion(self):
        try:
            from frontend.screens.perfil_screen import PerfilScreen
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")
        from tests._util import bd_temporal
        from frontend import auth
        with bd_temporal():
            auth._guardar_sesion({"idToken": "i", "refreshToken": "r",
                                  "expiresIn": "3600", "localId": "u",
                                  "email": "a@b.com"}, nombre="X")
            screen = PerfilScreen(name="perfil")
            try:
                screen._cerrar_sesion()
            except Exception:
                pass  # navigate_to falla sin App corriendo; lo que importa es la sesión
            self.assertIsNone(auth.usuario_actual())
```

- [ ] **Step 2: Ejecutar los tests para verificar que fallan**

Run: `python -m unittest tests.test_frontend -v`
Expected: FAIL (`PerfilScreen` no tiene `_cerrar_sesion`).

- [ ] **Step 3: Modificar `frontend/screens/perfil_screen.py`**

Añadir el import de `auth` arriba:

```python
from frontend import auth
```

Añadir `C_ERROR` a las constantes del archivo:

```python
C_ERROR = get_color_from_hex("#D32F2F")
```

En `_rebuild()`, sustituir la tarjeta fija de perfil:

```python
        self._card(
            self._content,
            "Perfil",
            "¡Hola, Doctor(a)!",
        )
```

por:

```python
        u = auth.usuario_actual()
        if u:
            self._card(self._content, u["nombre"] or "Perfil",
                       u["correo"] or "-")
        else:
            self._card(self._content, "Perfil", "Sin sesión")
```

Y al final de `_rebuild()`, después del botón "Abrir configuracion", añadir:

```python
        salir = Button(
            text="Cerrar sesión",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(15),
            bold=True,
            background_normal="",
            background_color=C_ERROR,
            color=get_color_from_hex("#FFFFFF"),
        )
        salir.bind(on_press=lambda _: self._cerrar_sesion())
        self._content.add_widget(salir)
```

Añadir el método a la clase:

```python
    def _cerrar_sesion(self):
        auth.cerrar_sesion()
        navigate_to("login")
```

- [ ] **Step 4: Ejecutar los tests para verificar que pasan**

Run: `python -m unittest tests.test_frontend -v`
Expected: PASS (todos) o SKIP si Kivy no está.

- [ ] **Step 5: Commit**

```bash
git add frontend/screens/perfil_screen.py tests/test_frontend.py
git commit -m "feat(auth): cerrar sesión desde el perfil y mostrar usuario real"
```

---

### Task 10: Documentación de configuración y verificación manual

**Files:**
- Create: `docs/firebase-setup.md`
- Modify: `README.md` (sección nueva "Autenticación")

**Interfaces:**
- Consumes: nada.
- Produces: guía para que la persona usuaria cree el proyecto Firebase y rellene `frontend/firebase_config.py`, más una checklist de verificación manual (no automatizable) del flujo completo.

- [ ] **Step 1: Crear `docs/firebase-setup.md`**

```markdown
# Configurar Firebase Authentication

La app usa Firebase Authentication para el registro e inicio de sesión
(correo/contraseña y Google). Necesitas un proyecto de Firebase gratuito.

## 1. Crear el proyecto

1. Entra a https://console.firebase.google.com
2. **Agregar proyecto** → nombre `MedScale-ORL` → crear (Analytics opcional).

## 2. Activar los métodos de inicio de sesión

1. Menú lateral → **Build → Authentication → Comenzar**.
2. Pestaña **Sign-in method**:
   - **Correo electrónico/contraseña** → habilitar → guardar.
   - **Google** → habilitar → elegir un correo de soporte → guardar.

## 3. Registrar una app Web (para obtener las llaves)

1. Icono ⚙️ (arriba a la izquierda) → **Configuración del proyecto**.
2. Sección **Tus apps** → botón **</>** (Web).
3. Apodo de la app: `MedScale-ORL` → **Registrar app**.
4. En el snippet `firebaseConfig` copia:
   - `apiKey`  → será `API_KEY`
   - `authDomain` (algo como `medscale-orl.firebaseapp.com`) → será `AUTH_DOMAIN`

## 4. Obtener el ID de cliente web de Google

1. **Authentication → Sign-in method → Google** (el que activaste).
2. Despliega **Configuración del SDK web**.
3. Copia **ID de cliente web** (termina en `.apps.googleusercontent.com`)
   → será `GOOGLE_WEB_CLIENT_ID`.

## 5. Rellenar la configuración local

```bash
cp frontend/firebase_config.example.py frontend/firebase_config.py
```

Edita `frontend/firebase_config.py` con los tres valores. Este archivo está
en `.gitignore`: no se sube al repositorio.

## Notas

- El inicio con Google en Android se hace con un WebView dentro de la app y
  redirige a `https://<AUTH_DOMAIN>/__/auth/handler`, que Firebase ya tiene
  como dominio autorizado. No hace falta registrar la huella SHA-1 ni usar
  Google Play Services.
- En escritorio (desarrollo con `python -m frontend`), el inicio con Google
  abre el navegador del sistema y usa `http://127.0.0.1:8765` como redirect.
```

- [ ] **Step 2: Añadir sección a `README.md`**

Añadir después de la sección de requisitos/instalación (ubicación exacta a criterio del implementador; debe quedar visible en el índice si lo hay):

```markdown
## Autenticación

La app abre en una pantalla de inicio de sesión. El registro y el login
(correo/contraseña o Google) usan **Firebase Authentication**.

Antes de ejecutar, configura tus llaves de Firebase siguiendo
[`docs/firebase-setup.md`](docs/firebase-setup.md) y crea
`frontend/firebase_config.py` a partir de `frontend/firebase_config.example.py`.

Sin ese archivo, la app arranca igual pero cualquier intento de login mostrará
un aviso pidiendo configurar las llaves.

La sesión se guarda en la tabla local `configuracion` y se mantiene entre
reinicios hasta que se pulse **Cerrar sesión** en el Perfil.
```

- [ ] **Step 3: Verificación manual (escritorio)**

Con `frontend/firebase_config.py` ya configurado:

1. `python -m frontend` → debe abrir en la pantalla **Iniciar sesión** (fondo `iniciose.jpeg`, formulario centrado en la zona blanca).
2. Pulsar **Regístrate** → rellenar nombre/correo/contraseña (≥6, coincidentes) → **Crear cuenta** → debe entrar a **home**.
3. Cerrar la app y volver a abrir → debe entrar directo a **home** (sesión mantenida).
4. Ir a **Perfil** → ver el nombre y correo reales → **Cerrar sesión** → vuelve a **Iniciar sesión**.
5. **Iniciar sesión** con el mismo correo/contraseña → entra a **home**.
6. **Iniciar sesión** con contraseña incorrecta → mensaje rojo "Correo o contraseña incorrectos.".
7. **¿Olvidaste tu contraseña?** con el correo puesto → mensaje verde de confirmación y llega el correo de Firebase.
8. **Continuar con Google** → se abre el navegador, se elige cuenta, vuelve a la app y entra a **home**.
9. Verificar en la consola de Firebase → Authentication → Users que aparecen las cuentas creadas.

- [ ] **Step 4: Verificación manual (APK Android)**

1. `buildozer android debug` → build sin errores (comprobar que `openssl` se compila).
2. Instalar el APK en un dispositivo.
3. Repetir los pasos 1–7 de la verificación de escritorio en el dispositivo
   (comprobar especialmente que las llamadas HTTPS a Firebase funcionan).
4. **Continuar con Google** → se abre el WebView dentro de la app, se elige
   cuenta, el WebView se cierra solo y entra a **home**.
   - Si el WebView no cierra o falla `removeView`: aplicar la variante con cast
     a `android.view.ViewGroup` indicada en `frontend/google_oauth.py`, o
     cambiar a Chrome Custom Tabs + `intent-filter` (spec §10).

- [ ] **Step 5: Commit**

```bash
git add docs/firebase-setup.md README.md
git commit -m "docs: guía de configuración de Firebase y checklist de verificación"
```

---

## Self-Review

**1. Cobertura del spec**

| Sección del spec | Task |
|---|---|
| §4 Configuración Firebase (guiada) | Task 1 (`firebase_config.example.py`), Task 10 (`docs/firebase-setup.md`) |
| §5 Arquitectura / árbol de archivos | Tasks 2–9 |
| §6.1 `auth.py` (store + REST) | Tasks 2, 3 |
| §6.2 `google_oauth.py` | Task 4 |
| §6.3 `ui.py` constantes + helpers | Task 5 |
| §6.4 `login_screen.py` | Task 6 |
| §6.5 `register_screen.py` | Task 7 |
| §6.6 compuerta en `main.py` | Task 8 |
| §6.7 `perfil_screen.py` logout + usuario real | Task 9 |
| §6.8 `buildozer.spec` (`openssl`) | Task 1 |
| §7 Flujo de datos | Tasks 6–9 (integración) |
| §8 Manejo de errores (tabla en español) | Task 2 (`_ERRORES`/`_traducir_error`), Task 3 (`_post`) |
| §9 Pruebas | Tasks 2–9 (cada una con tests), Task 10 (manual) |
| §10 Riesgos (WebView, openssl, encuadre imagen) | Task 4 (nota), Task 10 (verificación manual) |

Sin huecos.

**2. Escaneo de placeholders**

Sin "TBD"/"TODO"/"implementar después". Todos los pasos de código llevan bloque de código real. El único "pass" deliberado (`registrar` cuando falla `accounts:update`) está justificado en comentario. `_flujo_android` lleva implementación concreta + nota de verificación manual (no es un placeholder: es código que corre, con un plan B documentado).

**3. Consistencia de tipos**

- `_guardar_sesion(resp, nombre=None) -> dict {"uid","correo","nombre"}` — mismo nombre y forma en Tasks 2, 3, 9.
- `usuario_actual() -> dict|None` con claves `uid/correo/nombre` — consistente en Tasks 2, 9.
- `refrescar_sesion() -> bool` — consistente en Tasks 3, 8.
- `AuthError` (primer arg = mensaje español) — consistente en Tasks 2–7.
- Claves `configuracion`: `auth_refresh_token`, `auth_id_token`, `auth_expira_en`, `auth_uid`, `auth_correo`, `auth_nombre` — mismas en `_CLAVES`, `_guardar_sesion`, `usuario_actual`, `refrescar_sesion`, tests.
- `text_field/primary_button/outline_button/link_label` — mismas firmas en Task 5 (definición) y Tasks 6, 7 (uso).
- Nombres de pantalla `"login"`, `"register"`, `"home"` — consistentes en Tasks 6, 7, 8, 9.
- `obtener_id_token_google() -> str` — Task 4 (def), Tasks 6, 7 (uso).

Sin inconsistencias.
