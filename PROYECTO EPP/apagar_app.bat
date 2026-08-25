@echo off
title SafeGuard AI - Apagado Forzado
echo ========================================================
echo   CERRANDO SERVIDOR Y LIBERANDO CAMARA...
echo ========================================================
echo.

taskkill /F /IM python.exe /T >nul 2>&1

echo.
echo ========================================================
echo   TODOS LOS PROCESOS SE HAN CERRADO.
echo   La camara y el servidor estan 100%% apagados.
echo ========================================================
echo.
timeout /t 2 >nul
