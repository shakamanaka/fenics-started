from pathlib import Path
import pyvista as pv

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
FILE_PATH = OUTPUTS_DIR / "solution.vtu"

if not FILE_PATH.exists():
    available = list(OUTPUTS_DIR.glob("*.vtu"))
    if available:
        FILE_PATH = available[0]
    else:
        raise FileNotFoundError(f"No encontré archivos .vtu en {OUTPUTS_DIR}")

data = pv.read(str(FILE_PATH))

plotter = pv.Plotter()
plotter.add_text(f"VTU Visualizer\n{FILE_PATH.name}", font_size=12)
plotter.add_mesh(data, show_edges=True)
plotter.show()