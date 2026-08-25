@echo off
title SafeGuard AI - Actualizador de GitHub
echo ========================================================
echo   SINCRONIZANDO CAMBIOS CON GITHUB Y STREAMLIT CLOUD
echo ========================================================
echo.

git add .

set /p commit_msg="Escribe una breve nota del cambio (o presiona ENTER): "
if "%commit_msg%"=="" set commit_msg=Actualizacion de la aplicacion EPP

git commit -m "%commit_msg%"
git push origin main

echo.
echo ========================================================
echo   EXITO: Version mas reciente subida a GitHub!
echo   Streamlit Cloud se actualizara en ~15 segundos.
echo ========================================================
echo.
pause
