#!/usr/bin/env bash
set -e

echo "==> Creando entorno virtual..."
python3 -m venv .venv

echo "==> Activando entorno virtual..."
source .venv/bin/activate

echo "==> Actualizando pip..."
python3 -m pip install --upgrade pip

echo "==> Instalando dependencias..."
python3 -m pip install -r requirements.txt

echo "==> Inicialización completada."
echo ""
echo "Para activar el entorno manualmente luego usa:"
echo "source .venv/bin/activate"