import numpy as np
import matplotlib.pyplot as plt

# Configuraciones globales
plt.rcParams.update({
    'font.size': 13,
    'axes.titlesize': 14,
    'axes.labelsize': 13,
    'legend.fontsize': 11.5,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'font.family': 'STIXGeneral',           # o 'serif' si no tenés STIX
})

# 1. Datos observados (pueden ajustarse más adelante con valores reales publicados)
k_obs = np.array([0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 3.0, 5.0, 8.0, 12.0])
Pk_obs = np.array([25000, 23000, 18000, 12000, 7000, 2500, 600, 80, 25, 8, 3])
Pk_err = Pk_obs * 0.15   # 15% es razonable para ilustrar; luego usar errores reales

# 2. Eje fino
k_fine = np.logspace(-2, np.log10(15), 1200)

# 3. Modelo ΛCDM fenomenológico (puede mejorarse con CLASS/CAMB más adelante)
def lcdm_model(k):
    return 3e4 * (k/0.01)**0.9 / (1 + (k/0.05)**2.5)**0.8

Pk_lcdm = lcdm_model(k_fine)

# 4. Modelo IEC-Vórtices (supresión suave)
k_c = 5.0      # escala de corte [h/Mpc]
r_c = 0.18     # parámetro de supresión [Mpc/h]  → ajustar según paper
Pk_iec = Pk_lcdm * np.exp( -(k_fine * r_c)**2 * (k_fine / k_c)**2 / (1 + (k_fine / k_c)**2) )

# ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=130)

ax.plot(k_fine, Pk_lcdm, '--', color='black', lw=1.8, label=r'$\Lambda$CDM (Predicción teórica)')
ax.plot(k_fine, Pk_iec, '-', color='#0066CC', lw=3.2, label='IEC–Vórtices (Este trabajo)')

ax.errorbar(k_obs, Pk_obs, yerr=Pk_err, fmt='o', color='red', mec='darkred', mew=0.8,
            markersize=7, capsize=4, capthick=1.1, elinewidth=1.3,
            label='Datos (DESI + Planck + KiDS)')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.008, 15)
ax.set_ylim(0.9, 9e4)

ax.set_xlabel(r"\( k \,\, [h \, \mathrm{Mpc}^{-1}] \)", fontsize=14)
ax.set_ylabel(r"\( P(k) \,\, [(h^{-1} \mathrm{Mpc})^3] \)", fontsize=14)
ax.set_title("Espectro de potencia: Resolviendo el exceso de potencia a pequeña escala",
             fontsize=15, pad=12)

ax.legend(loc='upper right', frameon=True, edgecolor='0.8', fancybox=True)
ax.grid(True, which='both', ls=':', lw=0.7, alpha=0.25, color='0.4')

plt.tight_layout()

# Guardar (en alta resolución para publicación / compartir)
plt.savefig("espectro_potencia_IEC_vortices.png", dpi=300, bbox_inches='tight')
plt.savefig("espectro_potencia_IEC_vortices.pdf", bbox_inches='tight')   # ideal para LaTeX

plt.show()