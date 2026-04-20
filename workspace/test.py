from mpi4py import MPI
from dolfinx import mesh, fem
import ufl

domain = mesh.create_unit_square(MPI.COMM_WORLD, 8, 8)
V = fem.functionspace(domain, ("Lagrange", 1))

u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)
x = ufl.SpatialCoordinate(domain)

f = 10.0 * ufl.exp(-((x[0] - 0.5)**2 + (x[1] - 0.5)**2) / 0.02)
a = ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = f * v * ufl.dx

print("FEniCSx OK")
print("Número de celdas:", domain.topology.index_map(domain.topology.dim).size_local)