# Utility for drawing vortex lines. I may want to use these when discussing
# the circulation distribution over a wing.
#
# The idea is to draw the vortices in 3D then save them as an SVG. It's easier
# to draw things using matplotlib then import them into Inkscape.
#
# I haven't studied the relationship between elevation and azimuth in mplot3d
# `Axes3D` and the "x angle" and "z angle" of axonometric grids in Inkscape,
# but I did figure out how to make isometric plots in matplotlib.
#
# Setting `azimuth=45deg, elev=90-rad2deg(arctan(sqrt(2)))`
#
#  * See: https://www.blender3darchitect.com/architectural-visualization/create-true-isometric-camera-architecture/
#
# Also possibly related if I want to make non-isometric views:
# https://github.com/matplotlib/matplotlib/issues/17172#issuecomment-617546105

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np
import pfh.glidersim as gsim

N = 1000
num_turns = 8
theta = np.linspace(0, num_turns * 2 * np.pi, N)
R = np.linspace(.1, 1.5, N)
x = np.linspace(0, 20, N)
y = R * np.cos(theta)
z = R * np.sin(theta)

# TODO: draw an ellipse in the yz-plane between the wing tips? Save time in Inkscape.

fig = plt.figure(figsize=(10, 10))
ax = plt.gca(projection='3d', proj_type='ortho')
ax.plot(x, y + 10, z)  # Counterlockwise (right wing tip)
ax.plot(x, y , -z)  # Clockwise (left wing tip)
gsim.plots._set_axes_equal(ax)
fig.tight_layout()
ax.view_init(elev=90 - np.rad2deg(np.arctan(np.sqrt(2))), azim=-45)
plt.show()
