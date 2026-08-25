@echo off
title SafeGuard AI - Actualizador de GitHub
echo ========================================================
echo   SINCRONIZANDO CAMBIOS CON GITHUB Y STREAMLIT CLOUD
echo ========================================================
echo.

git branch -M main >nul 2>&1
git add .

set /p commit_msg="Escribe una breve nota del cambio (o presiona ENTER): "
if "%commit_msg%"=="" set commit_msg=Actualizacion automatica de SafeGuard AI

git commit -m "%commit_msg%"

echo.
echo Enviando cambios al repositorio remoto...
git push -u origin main

echo.
echo ========================================================
echo   PROCESO COMPLETADO!
echo ========================================================
echo.
pause
