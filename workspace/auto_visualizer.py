from pathlib import Path
import pyvista as pv

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"

patterns = ["*.pvd", "*.pvtu", "*.vtu"]
file_path = None

for pattern in patterns:
    matches = list(OUTPUTS_DIR.glob(pattern))
    if matches:
        file_path = matches[0]
        break

if file_path is None:
    raise FileNotFoundError(
        f"No encontré archivos .pvd, .pvtu o .vtu en {OUTPUTS_DIR}"
    )

data = pv.read(str(file_path))

plotter = pv.Plotter()
plotter.add_text(f"Auto Visualizer\n{file_path.name}", font_size=12)

if hasattr(data, "n_blocks"):
    for i in range(data.n_blocks):
        block = data[i]
        if block is not None:
            plotter.add_mesh(block, show_edges=True)
else:
    plotter.add_mesh(data, show_edges=True)

plotter.show()