# #ME369P Final Project
# import numpy as np
# from stl import mesh
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def voxelize(vertices, resolution):
#     min_coords = np.min(vertices, axis=(0, 1))
#     max_coords = np.max(vertices, axis=(0, 1))
#     grid_shape = np.ceil((max_coords - min_coords) / resolution).astype(int)
#     voxels = np.zeros(grid_shape, dtype=bool)
    
#     for triangle in vertices:
#         for vertex in triangle:
#             voxel_coord = np.floor((vertex - min_coords) / resolution).astype(int)
#             voxels[tuple(voxel_coord)] = True
    
#     return voxels

# def fits_brick(voxels, x, y, z, size):
#     if x + size[0] > voxels.shape[0] or y + size[1] > voxels.shape[1]:
#         return False
#     return np.all(voxels[x:x+size[0], y:y+size[1], z])

# def place_brick(lego_structure, x, y, z, size):
#     brick_id = len(size)  # Use brick size as identifier
#     lego_structure[x:x+size[0], y:y+size[1], z] = brick_id

# def legoize(voxels):
#     lego_structure = np.zeros_like(voxels, dtype=int)
#     brick_sizes = [(4, 2), (3, 2), (2, 2), (1, 1)]  # Common LEGO brick sizes
    
#     for z in range(voxels.shape[2]):
#         for y in range(voxels.shape[1]):
#             for x in range(voxels.shape[0]):
#                 if voxels[x, y, z]:
#                     for size in brick_sizes:
#                         if fits_brick(voxels, x, y, z, size):
#                             place_brick(lego_structure, x, y, z, size)
#                             break
    
#     return lego_structure

# def visualize_lego(lego_structure):
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
    
#     colors = plt.cm.jet(np.linspace(0, 1, len(np.unique(lego_structure))))
    
#     for z in range(lego_structure.shape[2]):
#         for y in range(lego_structure.shape[1]):
#             for x in range(lego_structure.shape[0]):
#                 if lego_structure[x, y, z] != 0:
#                     c = colors[lego_structure[x, y, z] - 1]
#                     ax.bar3d(x, y, z, 1, 1, 1, color=c, alpha=0.8)
    
#     plt.title("LEGO-ized Structure")
#     plt.show()

# def generate_bom(lego_structure):
#     unique, counts = np.unique(lego_structure, return_counts=True)
#     bom = dict(zip(unique, counts))
#     del bom[0]  # Remove empty space
    
#     print("Bill of Materials:")
#     brick_sizes = {1: "1x1", 2: "2x2", 3: "3x2", 4: "4x2"}
#     for brick_type, count in bom.items():
#         print(f"{brick_sizes[brick_type]} brick: {count} pieces")

# def main(stl_file_path, resolution=0.1):
#     # Load and process STL file
#     print(f"Loading STL file: {stl_file_path}")
#     stl_mesh = mesh.Mesh.from_file(stl_file_path)
#     vertices = stl_mesh.vectors

#     # Voxelize the model
#     print("Voxelizing the model...")
#     voxels = voxelize(vertices, resolution)

#     # Convert to LEGO structure
#     print("Converting to LEGO structure...")
#     lego_structure = legoize(voxels)

#     # Visualize the result
#     print("Generating visualization...")
#     visualize_lego(lego_structure)

#     # Generate bill of materials
#     print("\nGenerating Bill of Materials...")
#     generate_bom(lego_structure)

# if __name__ == "__main__":
#     stl_file_path = 'test.stl'  
#     main(stl_file_path)


import pyvista as pv
import numpy as np

def load_stl(file_path):
    print(f"Loading STL file: {file_path}")
    return pv.read(file_path)

def voxelize(mesh, resolution):
    print("Voxelizing the model...")
    voxels = pv.voxelize(mesh, density=resolution)
    return voxels

def legoize(voxels):
    print("Converting to LEGO structure...")
    lego_structure = voxels.copy()
    lego_structure.cell_data['brick_type'] = np.ones(lego_structure.n_cells)
    return lego_structure

def visualize_lego(lego_structure):
    print("Generating visualization...")
    p = pv.Plotter()
    p.add_mesh(lego_structure, scalars='brick_type', cmap='viridis', show_edges=True)
    p.show()

def generate_bom(lego_structure):
    print("\nGenerating Bill of Materials...")
    unique, counts = np.unique(lego_structure.cell_data['brick_type'], return_counts=True)
    print("Bill of Materials:")
    for brick_type, count in zip(unique, counts):
        print(f"1x1 brick: {count} pieces")

def main(stl_file_path, resolution=0.1):
    # Load STL file
    mesh = load_stl(stl_file_path)

    # Voxelize the model
    voxels = voxelize(mesh, resolution)

    # Convert to LEGO structure
    lego_structure = legoize(voxels)

    # Visualize the result
    visualize_lego(lego_structure)

    # Generate bill of materials
    generate_bom(lego_structure)

if __name__ == "__main__":
    stl_file_path = 'test.stl'  
    main(stl_file_path)