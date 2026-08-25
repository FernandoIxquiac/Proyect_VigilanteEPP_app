@echo off
title SafeGuard AI - Instalador Automatico
echo ========================================================
echo   INSTALANDO DEPENDENCIAS DE SAFEGUARD AI
echo ========================================================
echo.
echo Por favor espera unos momentos mientras se descargan
echo e instalan las librerias necesarias en tu computadora...
echo.

pip install -r requirements.txt

echo.
echo ========================================================
echo   INSTALACION COMPLETADA CON EXITO!
echo   Ahora puedes abrir "iniciar_app.bat" para usar el sistema.
echo ========================================================
echo.
pause
