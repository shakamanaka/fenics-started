from pathlib import Path
import pyvista as pv

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
FILE_PATH = OUTPUTS_DIR / "solution.pvtu"

if not FILE_PATH.exists():
    available = list(OUTPUTS_DIR.glob("*.pvtu"))
    if available:
        FILE_PATH = available[0]
    else:
        raise FileNotFoundError(f"No encontré archivos .pvtu en {OUTPUTS_DIR}")

data = pv.read(str(FILE_PATH))

plotter = pv.Plotter()
plotter.add_text(f"PVTU Visualizer\n{FILE_PATH.name}", font_size=12)

if hasattr(data, "n_blocks"):
    for i in range(data.n_blocks):
        block = data[i]
        if block is not None:
            plotter.add_mesh(block, show_edges=True)
else:
    plotter.add_mesh(data, show_edges=True)

plotter.show()