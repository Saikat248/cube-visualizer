from mayavi import mlab
import numpy as np
import sys 


"""
Resources
1.  About Cube File : http://sobereva.com/125
2. Plotting Volumetric Data and Molecule: https://docs.enthought.com/mayavi/mayavi/auto/example_chemistry.html
3. Mayavi Install: pip install https://github.com/enthought/mayavi/zipball/master
Found from this discussion https://github.com/enthought/mayavi/issues/1232
PyQT5 Install for Mayavi: pip install PyQt5

"""

if len(sys.argv) == 2:
    cubefile = sys.argv[1]
    isosurface = float(0.02)
elif len(sys.argv) == 3:
    cubefile = sys.argv[1]
    isosurface = float(sys.argv[2])


## Mayavi Color and Resolution Settings
    
bgcolor = (0.2823529411764706, 0.8117647058823529, 0.9529411764705882)
scale_factor = 0.8
resolution = 20
tube_radius = 0.1
blue = (0, 0, 1)
isosurface_pos = (1, 0.031, 0.031)  # Red
isosurface_neg = (1, 0.984, 0.027)  # Yellow
opacity = 0.9

fig = mlab.figure(figure=cubefile, bgcolor=bgcolor, size = (400, 250))
aa=0.5291772083

with open(cubefile, 'r') as f:
    lines = f.readlines()

natoms = int(lines[2].split()[0])
origin = np.array(lines[2].split()[1:]).astype(np.float64)

nx, xvec = int(lines[3].split()[0]), np.array(lines[3].strip().split()[1:]).astype(np.float64)
ny, yvec = int(lines[4].split()[0]), np.array(lines[4].strip().split()[1:]).astype(np.float64)
nz, zvec = int(lines[5].split()[0]), np.array(lines[5].strip().split()[1:]).astype(np.float64)


N2_1 = np.array(lines[6].strip().split()[2:]).astype(np.float64) * aa
N2_2 = np.array(lines[7].strip().split()[2:]).astype(np.float64) * aa

# Normalize all data to Angstrom Unit
origin *= aa
xvec *= aa
yvec *= aa
zvec *= aa

molecule = [N2_1, N2_2]

#Plot the Molecule and the bonds

x_coord, y_coord, z_coord = np.array(molecule).T
mlab.points3d(x_coord, y_coord, z_coord, color=blue, scale_factor=scale_factor, resolution=resolution)
mlab.plot3d(x_coord, y_coord, z_coord, [1, 1], tube_radius=tube_radius, color = blue) 

# Read Grid Data

data = np.zeros((nx*ny*nz))
idx = 0
for line in lines[8:]:
    for val in line.strip().split():
        data[idx] = float(val)
        idx += 1

data = np.reshape(data, (nx, ny, nz))


x = np.linspace(origin[0],  origin[0] + (nx - 1)*xvec[0], nx)
y = np.linspace(origin[1],  origin[1] + (ny - 1)*yvec[1], ny)
z = np.linspace(origin[2],  origin[2] + (nz - 1)*zvec[2], nz)

xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')


# Plot positive isosurface
positive_values = np.where(data >= 0, data, 0)
contour_pos = mlab.contour3d(xx, yy, zz, positive_values, contours=[isosurface], color=isosurface_pos, opacity=opacity, transparent=True)

# Plot negative isosurface
negative_values = np.where(data < 0, -data, 0)
contour_neg =  mlab.contour3d(xx, yy, zz, negative_values, contours=[isosurface], color=isosurface_neg, opacity=opacity, transparent=True)

for contour in [contour_pos, contour_neg]:
    contour.actor.property.specular = 0.8  # Set the specular intensity (0-1)
    contour.actor.property.specular_power = 80  # Set the specular power (higher values for sharper highlights)

mlab.show()
