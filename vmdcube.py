import subprocess
import os
from pathlib import Path
import sys


def vmd_script_generator(cubefile, isosurface):
    vmd_script=f"""light 1 off
light 0 rot y  30.0
light 0 rot x -30.0
#
# VMD script to plot MOs from cube files
#
# Load the molecule and change the atom style
mol load cube {cubefile}

mol modcolor 0 000 Element
# mol modstyle 0 000 Licorice 0.110000 10.000000 10.000000
mol modstyle 0 000 CPK 0.400000 0.40000 30.000000 16.000000

# Define the material
material change ambient Opaque 0.310000
material change diffuse Opaque 0.720000
material change specular Opaque 0.500000
material change shininess Opaque 0.480000
material change opacity Opaque  1.000000
material change outline Opaque 0.000000
material change outlinewidth Opaque 0.000000
material change transmode Opaque 0.000000
material change specular Opaque 0.750000

material change ambient   EdgyShiny 0.310000
material change diffuse   EdgyShiny 0.720000
material change shininess EdgyShiny 1.0000
material change opacity   EdgyShiny 1

# Customize atom colors
color Element C silver
color Element H white

# Rotate and translate the molecule
rotate x by 30.0
rotate y by 40.0
rotate z by 15.0
translate by 0.0 0.0 0.0
scale by 1.0

# Eliminate the axis and perfect the view
axes location on
display projection Orthographic
display depthcue off
display resize 400 400
color Display Background white
#
# Add a surface
mol color ColorID 3
mol representation Isosurface {isosurface} 0 0 0 1 1
mol selection all
mol material EdgyShiny
mol addrep 000
#
# Add a surface
mol color ColorID 23
mol representation Isosurface {float(isosurface) * -1} 0 0 0 1 1
mol selection all
mol material EdgyShiny
mol addrep 000
set molname [molinfo top get name]
puts "The molecule name is: $molname"
#FIX HERE: Molname size currently not working
display text "$molname" size 20x20 color red anchor center

# Define the position of the text
set position {{1.5 1.5 1.5}}

# Display the text
draw color red
draw text $position $molname

"""
    return vmd_script


def write_and_run_vmd_script(cubefile, vmd_script):
    vmd_path = os.environ.get('VMDPATH')
    vmd_file = Path(cubefile).with_suffix('.vmd')
    with open(vmd_file, 'w+') as fp:
        fp.writelines(vmd_script)
    FNULL = open(os.devnull, 'w')
    subprocess.call(("%s -e %s" % (vmd_path, vmd_file)), stdout=FNULL, shell=True)
    os.remove(vmd_file)


def main(cubefile, isosurface):
    vmd_script = vmd_script_generator(cubefile, isosurface)
    write_and_run_vmd_script(cubefile, vmd_script)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        cubefile = sys.argv[1]
        isosurface = float(0.02)
        main(cubefile, isosurface)
    elif len(sys.argv) == 3:
        cubefile = sys.argv[1]
        isosurface = float(sys.argv[2])
        main(cubefile, isosurface)
