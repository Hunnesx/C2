import numpy as np
import matplotlib.pyplot as plt

# Winkel
phi = np.linspace(0, 2*np.pi, 500)

# Materialparameter (SI-Einheiten!)
# Aluminium
c11_Al = 1.068e11
c12_Al = 0.607e11
c44_Al = 0.282e11
rho_Al = 2679.5

# Kupfer
c11_Cu = 1.684e11
c12_Cu = 1.214e11
c44_Cu = 0.754e11
rho_Cu = 8899

def velocities(phi, c11, c12, c44, rho):
    term1 = (c11 - c44)**2 * np.cos(2*phi)**2
    term2 = (c12 + c44)**2 * np.sin(2*phi)**2
    root = np.sqrt(term1 + term2)
    
    c1 = np.sqrt((c11 + c44 + root) / (2*rho))
    c2 = np.sqrt((c11 + c44 - root) / (2*rho))
    c3 = np.sqrt(c44 / rho) * np.ones_like(phi)
    
    return c1, c2, c3

# Berechnung
c1_Al, c2_Al, c3_Al = velocities(phi, c11_Al, c12_Al, c44_Al, rho_Al)
c1_Cu, c2_Cu, c3_Cu = velocities(phi, c11_Cu, c12_Cu, c44_Cu, rho_Cu)

# -------------------------
# Plot 1: Aluminium
# -------------------------
plt.figure()
ax = plt.subplot(projection='polar')
ax.plot(phi, c1_Al, label='Longitudinal')
ax.plot(phi, c2_Al, label='Transversal 1')
ax.plot(phi, c3_Al, label='Transversal 2')
ax.set_title("Aluminium")
ax.legend()
plt.show()

# -------------------------
# Plot 2: Kupfer
# -------------------------
plt.figure()
ax = plt.subplot(projection='polar')
ax.plot(phi, c1_Cu, label='Longitudinal')
ax.plot(phi, c2_Cu, label='Transversal 1')
ax.plot(phi, c3_Cu, label='Transversal 2')
ax.set_title("Kupfer")
ax.legend()
plt.show()