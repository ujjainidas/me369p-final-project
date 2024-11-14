import numpy as np
from stl import mesh
import csv

def read_stl(file_path):
    return mesh.Mesh.from_file(file_path)

def get_bounding_box(stl_mesh):
    min_bound = np.min(stl_mesh.vectors, axis=(0, 1))
    max_bound = np.max(stl_mesh.vectors, axis=(0, 1))
    return min_bound, max_bound

def voxelize(mesh, voxel_size):
    min_bound, max_bound = get_bounding_box(mesh)
    
    # voxel grid dimensions
    grid_shape = ((max_bound - min_bound) / voxel_size).astype(int) + 1
    grid = np.zeros(grid_shape, dtype=bool)
    
    # Place triangles into the voxel grid
    for triangle in mesh.vectors:
        # Get the voxel space indices for the vertices of the triangle
        triangle_min = np.floor((triangle.min(axis=0) - min_bound) / voxel_size).astype(int)
        triangle_max = np.ceil((triangle.max(axis=0) - min_bound) / voxel_size).astype(int)
        
        for i in range(triangle_min[0], triangle_max[0] + 1):
            for j in range(triangle_min[1], triangle_max[1] + 1):
                for k in range(triangle_min[2], triangle_max[2] + 1):
                    grid[i, j, k] = True
    
    return grid, min_bound

def export_to_csv(grid, min_bound, voxel_size, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x", "y", "z"])
        
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                for z in range(grid.shape[2]):
                    if grid[x, y, z]:
                        coord = min_bound + np.array([x, y, z]) * voxel_size
                        writer.writerow(coord)

def main():
    file_path = ''
    output_file = ''
    voxel_size = 1.0
    
    stl_mesh = read_stl(file_path)
    grid, min_bound = voxelize(stl_mesh, voxel_size)
    export_to_csv(grid, min_bound, voxel_size, output_file)

if __name__ == "__main__":
    main()
