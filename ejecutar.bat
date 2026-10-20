@echo off
title Conversor de Longitud (mm, cm, m)
echo Iniciando Conversor de Longitud...
python Conversor.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ha ocurrido un error al ejecutar el programa.
    pause
)

