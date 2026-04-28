# Lecciones Aprendidas — ai-mastery

> *"Si el código falla, es un dato. Aquí lo documentamos."*

## Formato Estándar
- **Fecha:** YYYY-MM-DD
- **Síntoma:** ¿Qué observé?
- **Causa Raíz:** ¿Por qué ocurrió realmente?
- **Solución Aplicada:** ¿Cómo lo arreglé?
- **Prevención Futura:** ¿Qué test o check añadí?

---
## Semana 1 — Fundamentos y Primer Proyecto

### 1. Error de codificación UTF-8 en Windows PowerShell
- **Fecha:** 2026-04-12
- **Síntoma:** Los emojis (🔥, ✅, ❌) se mostraban como ?? o caracteres extraños en la terminal y en los archivos guardados con Out-File.
- **Causa Raíz:** PowerShell, por defecto, guarda los archivos en UTF-16LE o UTF-8 con BOM, lo que provoca que Python interprete mal los caracteres especiales.
- **Solución Aplicada:** Usar [System.IO.File]::WriteAllText(..., UTF8Encoding::new(False)) para forzar UTF-8 sin BOM.
- **Prevención Futura:** Utilizar siempre este método para archivos que contengan emojis o acentos, y verificar con Get-Content -Encoding UTF8.

### 2. Error de importación circular en Click y decoradores
- **Fecha:** 2026-04-13
- **Síntoma:** Al añadir el decorador @timer al comando 
un, Click dejaba de reconocer el comando (Error: No such command 'run').
- **Causa Raíz:** El decorador @timer no preservaba la firma de la función original. Click inspecciona la firma para detectar los argumentos del comando, y al no encontrarlos, ignoraba el comando.
- **Solución Aplicada:** Usar @functools.wraps(func) dentro del decorador para mantener los metadatos de la función original.
- **Prevención Futura:** Todos los decoradores que se apliquen sobre comandos de Click deben incluir @wraps(func).

### 3. Fallos de formato en CI/CD por Ruff (espacios y líneas largas)
- **Fecha:** 2026-04-13 y 2026-04-14
- **Síntoma:** GitHub Actions fallaba con múltiples errores W293 Blank line contains whitespace y E501 Line too long.
- **Causa Raíz:** El editor de código (VSCode) insertaba espacios en líneas vacías y se escribieron diccionarios en una sola línea que excedían los 100 caracteres.
- **Solución Aplicada:** Ejecutar 
uff check --fix localmente para corregir automáticamente los espacios, y reformatear manualmente los diccionarios largos en múltiples líneas.
- **Prevención Futura:** Configurar VSCode para que elimine espacios en blanco al guardar ("files.trimTrailingWhitespace": true), y mantener las líneas por debajo de 100 caracteres.

## Fallos más frecuentes (Mes 4)

### 1. Error de estilo Ruff que rompía el CI
- **Síntoma:** El pipeline de CI fallaba con errores `W292` (falta de nueva línea final) e `I001` (imports desordenados).
- **Causa Raíz:** Los archivos modificados no se formateaban con `ruff format` antes del commit.
- **Solución Aplicada:** Ejecutar `ruff check --fix src/` antes de cada commit y enmendar los commits fallidos con `git commit --amend`.
- **Prevención Futura:** Añadir un hook de pre‑commit que ejecute Ruff automáticamente, o configurar VS Code para formatear al guardar.

### 2. Fallo de conexión a PostgreSQL (Supabase)
- **Síntoma:** `psycopg2.OperationalError: could not translate host name` al intentar conectar con la base de datos de Supabase.
- **Causa Raíz:** Se usó el host directo (`db.xxxxx.supabase.co`) en lugar del Session Pooler, que es necesario en redes IPv4.
- **Solución Aplicada:** Obtener la URI del Session Pooler desde Supabase (host `aws-0-eu-west-1.pooler.supabase.com`, puerto `5432`) y usarla en `DATABASE_URL`.
- **Prevención Futura:** Verificar la conectividad con un script mínimo (`ping.py`) antes de integrar cualquier base de datos externa.

### 3. Archivo `.env` corrupto con codificación incorrecta
- **Síntoma:** `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff` al leer el archivo `.env`.
- **Causa Raíz:** El bloc de notas de Windows guardó el archivo en UTF‑16 en lugar de UTF‑8.
- **Solución Aplicada:** Eliminar el archivo corrupto y volver a crearlo directamente en VS Code, asegurando la codificación UTF‑8 sin BOM.
- **Prevención Futura:** Usar siempre VS Code para editar archivos de configuración y verificar la codificación antes de guardar.
