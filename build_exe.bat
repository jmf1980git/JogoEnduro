@echo off
echo ============================================
echo   Criando executavel Enduro 2D...
echo ============================================
echo.

REM Instalar PyInstaller se nao estiver instalado
pip install pyinstaller

echo.
echo Gerando executavel...
echo.

pyinstaller --onefile --windowed --name "Enduro2D" ^
    --add-data "asset;asset" ^
    --add-data "code;code" ^
    --add-data "records.json;." ^
    --icon "asset/picture/icon.ico" ^
    main.py

echo.
echo ============================================
if exist "dist\Enduro2D.exe" (
    echo   SUCESSO! Executavel criado em:
    echo   dist\Enduro2D.exe
) else (
    echo   Tentando sem icone...
    pyinstaller --onefile --windowed --name "Enduro2D" ^
        --add-data "asset;asset" ^
        --add-data "code;code" ^
        --add-data "records.json;." ^
        main.py
    if exist "dist\Enduro2D.exe" (
        echo   SUCESSO! Executavel criado em:
        echo   dist\Enduro2D.exe
    ) else (
        echo   ERRO ao criar executavel.
    )
)
echo ============================================
echo.
pause
