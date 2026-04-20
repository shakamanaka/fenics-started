# 🧪 FEniCS Docker Starter

Pequeña abstracción para ejecutar FEniCS (FEniCSx / DOLFINx) dentro de Docker y visualizar resultados desde tu máquina local.

---

## 🎯 Objetivo

Este proyecto simplifica:

- Ejecutar simulaciones FEM sin instalar dependencias complejas
- Usar FEniCS desde Docker (Linux) en cualquier sistema (Mac/Windows)
- Visualizar resultados (`.pvd`, `.vtu`, `.pvtu`) localmente

---

## Arquitectura

Host (Mac / Windows)
 ├─ VS Code
 ├─ Python (.venv) → visualización (PyVista)
 └─ Docker → ejecución FEniCS

Docker Container (Ubuntu + FEniCSx)
 └─ Ejecuta simulaciones y genera outputs

Separación clave:
- Docker → cálculo
- Host local → visualización

---

## Uso rápido

### 1. Construir y levantar el entorno

docker compose build
docker compose up -d

### 2. Ejecutar scripts dentro de FEniCS

docker compose exec fenics bash
docker compose exec fenics python3 /workspace/test.py

### 3. Ver resultados

Los outputs se generan en:
workspace/outputs/

---

## Visualización local (GUI)

### Crear entorno local

python3 -m venv .venv
source .venv/bin/activate

### Instalar dependencias

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

### Abrir resultados

python3 workspace/file_visualizer.py workspace/outputs/poisson_solution.pvd

---

## Dependencias

requirements.txt incluye:
- pyvista
- vtk
- numpy
- matplotlib

---

## Qué hace este proyecto

Abstracción mínima para:
- evitar instalación manual de dependencias complejas
- encapsular FEniCS en Docker
- separar cálculo y visualización

---

## Notas

- No visualizar dentro del contenedor
- Usar host para GUI
- Docker garantiza compatibilidad Linux
