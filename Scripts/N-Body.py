import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parámetros consistentes con Etapa 4
ETA = 0.0478
PHI0 = 1.0
RC = 1.0
BOX_SIZE = 100.0  # kpc/h
N_VORTICES = 500
DT = 0.05
DAMPING = 0.95    # Simula expansión/enfriamiento
N_STEPS = 1000

# Inicialización de estado
pos = np.random.uniform(0, BOX_SIZE, (N_VORTICES, 3))
vel = np.zeros((N_VORTICES, 3))
# Cargas n = ±1, ±2
n_labels = np.random.choice([-2, -1, 1, 2], N_VORTICES)

def update_physics(pos, vel, n):
    forces = np.zeros_like(pos)
    # Optimizamos con broadcasting para evitar el cuello de botella
    for i in range(N_VORTICES):
        # Distancia relativa con convención de imagen más cercana
        diff = pos[i] - pos
        diff = diff - BOX_SIZE * np.round(diff / BOX_SIZE)
        
        # r^2 regularizado con el radio de núcleo rc
        r2 = np.sum(diff**2, axis=1) + RC**2
        
        # Fuerza derivada del potencial logarítmico topológico
        # F_ij = 2*pi^2*ni*nj / r^2 * r_vec
        prefactor = (2 * np.pi**2 * n[i] * n) / r2
        forces[i] = np.sum(prefactor[:, np.newaxis] * diff, axis=0)
    
    # Integración de Euler-Cromer
    vel = vel * DAMPING + forces * DT
    pos = (pos + vel * DT) % BOX_SIZE
    return pos, vel

# Ejecución de la dinámica
for _ in range(N_STEPS):
    pos, vel = update_physics(pos, vel, n_labels)

# Visualización 3D profesional para el Paper
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Dividimos por carga para mejorar el estilo visual
for val in [-2, -1, 1, 2]:
    mask = n_labels == val
    color = 'red' if val > 0 else 'blue'
    alpha = 0.6 if abs(val) == 1 else 0.9
    size = 15 if abs(val) == 1 else 40
    ax.scatter(pos[mask,0], pos[mask,1], pos[mask,2], 
               c=color, s=size, alpha=alpha, label=f'n = {val}')

ax.set_title(f"Relajación de la Red de Vórtices IEC ($z < 1100$)\n $\eta={ETA}$, $r_c={RC}$", fontsize=14)
ax.set_xlabel('x [kpc/h]')
ax.set_ylabel('y [kpc/h]')
ax.set_zlabel('z [kpc/h]')
ax.legend(loc='upper right')
ax.view_init(elev=20, azim=45)

plt.savefig('red_cosmica_iec.png', dpi=300)
plt.show()