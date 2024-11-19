# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 17:23:40 2024

@author: lando
"""

import csv
import math

# Define the part dictionary with part IDs and their shapes
part_Dict = {
    '2x2': [[1, 1], [1, 1]],
    '1x2': [[1, 1]],
    '1x1': [[1]]
}

def read_voxel_data(file_path):
    """Read voxel data from a CSV file and return a list of coordinates."""
    voxels = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            voxels.append({
                "x": int(row["x"]),
                "y": int(row["y"]),
                "z": int(row["z"]),
            })
    return voxels

def create_voxel_grid(voxels):
    """Convert a list of voxel coordinates into a 3D grid."""
    max_x = max(voxel["x"] for voxel in voxels)
    max_y = max(voxel["y"] for voxel in voxels)
    max_z = max(voxel["z"] for voxel in voxels)
    
    # Initialize a 3D grid with zeros
    grid = [[[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)] for _ in range(max_z + 1)]
    
    # Fill the grid based on voxel coordinates
    for voxel in voxels:
        grid[voxel["z"]][voxel["y"]][voxel["x"]] = 1
    
    return grid

def ispart(shape):
    """Check if a given shape matches any defined part in part_Dict."""
    for ID, defined_shape in part_Dict.items():
        if shape == defined_shape:
            return ID
    return None

def find_largest_part(voxel, x, y, z):
    """Find the largest part that fits at a specific position."""
    for ID, shape in sorted(part_Dict.items(), key=lambda x: len(x[1]) * len(x[1][0]), reverse=True):
        shape_height = len(shape)
        shape_width = len(shape[0])

        # Check if shape fits at the current location
        if all(
            z + dz < len(voxel) and
            y + dy < len(voxel[z + dz]) and
            x + dx < len(voxel[z + dz][y + dy]) and
            voxel[z + dz][y + dy][x + dx] == 1
            for dz in range(shape_height)
            for dy in range(shape_width)
            for dx in range(len(shape[0][0]))
        ):
            # Mark the used voxel spaces as 0
            for dz in range(shape_height):
                for dy in range(shape_width):
                    for dx in range(len(shape[0][0])):
                        voxel[z + dz][y + dy][x + dx] = 0
            return ID, shape, [(x + dx, y + dy, z + dz)
                               for dz in range(shape_height)
                               for dy in range(shape_width)
                               for dx in range(len(shape[0][0]))]

    return None, None, None

def legoize(voxel):
    """Convert a voxel grid into a list of LEGO parts."""
    part_list = []
    z_size, y_size, x_size = len(voxel), len(voxel[0]), len(voxel[0][0])

    # Iterate through the voxel grid
    for z in range(z_size):
        for y in range(y_size):
            for x in range(x_size):
                if voxel[z][y][x] == 1:
                    part_id, part_shape, part_coords = find_largest_part(voxel, x, y, z)
                    if part_id:
                        part_list.append((part_id, part_coords))
    
    return part_list

def convert_to_bricks(parts):
    """Convert LEGO plates into bricks where 3 plates equal 1 brick."""
    brick_parts = []
    for part_id, coords in parts:
        z_coords = sorted(set(c[2] for c in coords))
        if len(z_coords) == 3:  # Check if it can be stacked into a brick
            brick_parts.append((part_id + " Brick", coords))
        else:
            brick_parts.append((part_id, coords))
    return brick_parts

def main():
    # Read voxel data from the uploaded CSV file
    voxel_data = read_voxel_data('voxel.csv')
    
    # Create a 3D voxel grid
    voxel_grid = create_voxel_grid(voxel_data)
    
    # Convert the voxel grid to LEGO parts
    lego_parts = legoize(voxel_grid)
    
    # Convert plates to bricks where applicable
    final_parts = convert_to_bricks(lego_parts)
    
    # Output the final LEGO parts
    print("Generated LEGO Parts List:")
    for part in final_parts:
        print(part)

if __name__ == "__main__":
    main()
