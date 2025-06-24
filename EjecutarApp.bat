@echo off
cd /d "%~dp0"
echo ===============================
echo Verificando Python...
echo ===============================

REM Validar si existe carpeta "salida", si no, crearla
if not exist "Salida" (
  mkdir "Salida"
  echo Carpeta creada.
) else (
  echo La carpeta ya existe.
)

where python >nul 2>nul

if %errorlevel%==0 (
  echo Python instalado.
  python --version
  echo Ejecutando script...
  if not exist "buscar_timbres" (
    python -m venv buscar_timbres
    echo Entorno virutal creado.
  ) else (
    echo Entorno virtual ya existe.
  )
  .\buscar_timbres\Scripts\activate
  pip install -r requirements.txt
  cls
  python .\app.py
) else (
  echo Python no instalado o no en PATH.
  echo Instale Python desde https://www.python.org/downloads/
  pause
  exit /b
)

echo .
pause

