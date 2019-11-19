from sympy import symbols
from numpy import linspace
from sympy import lambdify
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

t_pred = symbols('t_pred')
y_pred = symbols("y_pred")

x = t_pred**2 + y_pred**2
lam_x = lambdify([t_pred, y_pred], x, modules=['numpy'])

t_pred_vals = linspace(-10, 10, 100)
y_pred_vals = linspace(-10, 10, 100)
import numpy as np
X, Y = np.meshgrid(t_pred_vals, y_pred_vals)

Z = lam_x(X, Y)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

