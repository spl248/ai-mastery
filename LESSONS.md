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
- **Síntoma:** Al añadir el decorador @timer al comando un, Click dejaba de reconocer el comando (Error: No such command 'run').
- **Causa Raíz:** El decorador @timer no preservaba la firma de la función original. Click inspecciona la firma para detectar los argumentos del comando, y al no encontrarlos, ignoraba el comando.
- **Solución Aplicada:** Usar @functools.wraps(func) dentro del decorador para mantener los metadatos de la función original.
- **Prevención Futura:** Todos los decoradores que se apliquen sobre comandos de Click deben incluir @wraps(func).

### 3. Fallos de formato en CI/CD por Ruff (espacios y líneas largas)
- **Fecha:** 2026-04-13 y 2026-04-14
- **Síntoma:** GitHub Actions fallaba con múltiples errores W293 Blank line contains whitespace y E501 Line too long.
- **Causa Raíz:** El editor de código (VSCode) insertaba espacios en líneas vacías y se escribieron diccionarios en una sola línea que excedían los 100 caracteres.
- **Solución Aplicada:** Ejecutar uff check --fix localmente para corregir automáticamente los espacios, y reformatear manualmente los diccionarios largos en múltiples líneas.
- **Prevención Futura:** Configurar VSCode para que elimine espacios en blanco al guardar ("files.trimTrailingWhitespace": true), y mantener las líneas por debajo de 100 caracteres.

