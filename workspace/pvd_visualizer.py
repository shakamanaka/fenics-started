from pathlib import Path
import pyvista as pv

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
FILE_PATH = OUTPUTS_DIR / "poisson_solution.pvd"

if not FILE_PATH.exists():
    raise FileNotFoundError(f"No existe el archivo: {FILE_PATH}")

data = pv.read(str(FILE_PATH))

plotter = pv.Plotter()
plotter.add_text("PVD Visualizer", font_size=12)

if hasattr(data, "n_blocks"):
    for i in range(data.n_blocks):
        block = data[i]
        if block is not None:
            plotter.add_mesh(block, show_edges=True)
else:
    plotter.add_mesh(data, show_edges=True)

plotter.show()