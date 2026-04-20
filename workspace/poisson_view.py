from pathlib import Path

from mpi4py import MPI
import numpy as np
import pyvista
import ufl

from dolfinx import fem, mesh
from dolfinx.fem.petsc import LinearProblem
from dolfinx.io import VTKFile
from dolfinx.plot import vtk_mesh

BASE_DIR = Path("/workspace")
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pyvista.OFF_SCREEN = True

# -----------------------------
# 1) Crear malla
# -----------------------------
domain = mesh.create_unit_square(MPI.COMM_WORLD, 40, 40)
V = fem.functionspace(domain, ("Lagrange", 1))

# -----------------------------
# 2) Condiciones de borde
#    u = 0 en todo el borde
# -----------------------------
fdim = domain.topology.dim - 1
domain.topology.create_connectivity(fdim, domain.topology.dim)
boundary_facets = mesh.exterior_facet_indices(domain.topology)
boundary_dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)

bc = fem.dirichletbc(
    np.array(0.0, dtype=np.float64),
    boundary_dofs,
    V,
)

# -----------------------------
# 3) Problema de Poisson
# -----------------------------
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)
x = ufl.SpatialCoordinate(domain)

f_expr = 10.0 * ufl.exp(-((x[0] - 0.5) ** 2 + (x[1] - 0.5) ** 2) / 0.02)

a = ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = f_expr * v * ufl.dx

problem = LinearProblem(
    a,
    L,
    bcs=[bc],
    petsc_options_prefix="poisson_demo_",
    petsc_options={
        "ksp_type": "preonly",
        "pc_type": "lu",
        "ksp_error_if_not_converged": True,
    },
)

uh = problem.solve()
uh.name = "solution"

# -----------------------------
# 4) Exportar resultado
# -----------------------------
with VTKFile(domain.comm, str(OUT_DIR / "poisson_solution.pvd"), "w") as vtk:
    vtk.write_function(uh)

# -----------------------------
# 5) Visualización
# -----------------------------
cells, types, geometry = vtk_mesh(V)
grid = pyvista.UnstructuredGrid(cells, types, geometry)
grid.point_data["u"] = uh.x.array.real
grid.set_active_scalars("u")

plotter1 = pyvista.Plotter(off_screen=True)
plotter1.add_text("Poisson solution", font_size=12)
plotter1.add_mesh(grid, show_edges=True)
plotter1.view_xy()
plotter1.screenshot(str(OUT_DIR / "poisson_scalar.png"))
plotter1.close()

warped = grid.warp_by_scalar("u", factor=0.15)

plotter2 = pyvista.Plotter(off_screen=True)
plotter2.add_text("Warped solution", font_size=12)
plotter2.add_mesh(warped, show_edges=True)
plotter2.view_isometric()
plotter2.screenshot(str(OUT_DIR / "poisson_warped.png"))
plotter2.close()

if domain.comm.rank == 0:
    print(OUT_DIR / "poisson_solution.pvd")
    print(OUT_DIR / "poisson_scalar.png")
    print(OUT_DIR / "poisson_warped.png")