import numpy as np
import matplotlib.pyplot as plt

def potencial_relajacion_lambda():
    phi = np.linspace(0, 5, 500)
    phi0 = 1.0
    m = 0.8
    hbar = 1.0
    
    # Potencial de relajación elástica IEC
    V_phi = 0.5 * m**2 * phi0**2 * (1 - np.exp(-(m**2 * phi**2) / hbar**2))
    
    # Potencial cuadrático estándar (para comparar)
    V_std = 0.5 * m**2 * phi**2

    plt.figure(figsize=(9, 6))
    plt.plot(phi, V_phi, label=r'Potencial IEC ($\Lambda_{\rm eff}$)', color='crimson', lw=2)
    plt.axhline(y=0.5 * m**2 * phi0**2, color='gray', linestyle='--', label='Límite de Relajación')
    
    plt.title('Mecanismo de Relajación Elástica del Vacío', fontsize=13)
    plt.xlabel(r'Campo de Desplazamiento $\phi$')
    plt.ylabel(r'Densidad de Energía $V(\phi)$')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Anotación técnica
    plt.annotate('Resolución del Problema\nde la Constante Cosmológica', xy=(3, 0.3), 
                 xytext=(3.2, 0.1), arrowprops=dict(arrowstyle='->'))
    
    plt.show()

if __name__ == "__main__":
    potencial_relajacion_lambda()