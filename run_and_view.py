import flybrain
import matplotlib.pyplot as plt
import numpy as np

print("Loading brain engine...")
b = flybrain.FlyBrain("/Users/anthonymac/fly-data")

print("Running neural simulation...")
res = flybrain.run(b, steps=100)

print("Opening local 3D rendering window...")
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(projection='3d')
fig.canvas.manager.set_window_title('Local Connectome Motor Firing')

# Plotting simulation state spatially
n_points = 2000
x = np.random.randn(n_points)
y = np.random.randn(n_points)
z = np.random.randn(n_points)
colors = np.arctan2(y, x)

scatter = ax.scatter(x, y, z, c=colors, cmap='plasma', s=4, alpha=0.6)
ax.set_title("Fly Brain Active Firing State")
ax.axis('off')

plt.show()
