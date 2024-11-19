import numpy as np
import pandas as pd
import trimesh
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def point_inside_triangle(point, triangle):
    """
    Checks if a point is inside a triangle using barycentric coordinates.
    """
    # Triangle vertices
    v0, v1, v2 = triangle

    # Vectors from point to triangle vertices
    v2_v0 = v2 - v0
    v1_v0 = v1 - v0
    point_v0 = point - v0

    # Barycentric coordinates
    dot00 = np.dot(v2_v0, v2_v0)
    dot01 = np.dot(v2_v0, v1_v0)
    dot02 = np.dot(v2_v0, point_v0)
    dot11 = np.dot(v1_v0, v1_v0)
    dot12 = np.dot(v1_v0, point_v0)

    # Denominator (determinant of the matrix)
    denom = dot00 * dot11 - dot01 * dot01

    # Barycentric coordinates (u, v)
    invDenom = 1.0 / denom
    u = (dot11 * dot02 - dot01 * dot12) * invDenom
    v = (dot00 * dot12 - dot01 * dot02) * invDenom

    # Check if point is inside the triangle
    return (u >= 0) and (v >= 0) and (u + v <= 1)

def voxelize(vertices, resolution):
    """
    Converts an STL's vertices into a voxel grid DataFrame.
    """
    min_coords = np.min(vertices, axis=(0, 1))
    max_coords = np.max(vertices, axis=(0, 1))
    grid_shape = np.ceil((max_coords - min_coords) / resolution).astype(int)
    voxel_data = []

    for triangle in vertices:
        bbox_min = np.min(triangle, axis=0)
        bbox_max = np.max(triangle, axis=0)
        x_range = np.arange(bbox_min[0], bbox_max[0], resolution)
        y_range = np.arange(bbox_min[1], bbox_max[1], resolution)
        z_range = np.arange(bbox_min[2], bbox_max[2], resolution)

        for x in x_range:
            for y in y_range:
                for z in z_range:
                    point = np.array([x, y, z])
                    if point_inside_triangle(point, triangle):
                        voxel_coord = np.floor((point - min_coords) / resolution).astype(int)
                        voxel_data.append((*voxel_coord, True))
    
    voxel_df = pd.DataFrame(voxel_data, columns=['x', 'y', 'z', 'filled'])
    return voxel_df


def fits_brick(voxel_df, x, y, z, size):
    """
    Checks if a LEGO brick of the given size fits at the specified position.
    """
    selection = voxel_df.query(
        f"x >= {x} and x < {x + size[0]} and "
        f"y >= {y} and y < {y + size[1]} and "
        f"z == {z} and filled == True"
    )
    return len(selection) == (size[0] * size[1])


def place_brick(lego_df, x, y, z, size, brick_id):
    """
    Places a LEGO brick of the given size in the structure.
    """
    # Collect new rows to be added
    new_rows = [{'x': x + dx, 'y': y + dy, 'z': z, 'brick_id': brick_id}
                for dx in range(size[0])
                for dy in range(size[1])]
    
    # Convert new rows into a DataFrame
    new_rows_df = pd.DataFrame(new_rows)
    
    # Concatenate the new rows with the existing DataFrame
    lego_df = pd.concat([lego_df, new_rows_df], ignore_index=True)
    return lego_df


def legoize(voxel_df):
    """
    Converts voxels into a LEGO structure using a DataFrame.
    """
    lego_df = pd.DataFrame(columns=['x', 'y', 'z', 'brick_id'])
    brick_sizes = [(4, 2), (3, 2), (2, 2), (1, 1)]
    max_z = voxel_df['z'].max()

    for z in range(max_z + 1):
        layer = voxel_df.query(f'z == {z} and filled == True')
        for _, row in layer.iterrows():
            x, y = row['x'], row['y']
            for size in brick_sizes:
                if fits_brick(voxel_df, x, y, z, size):
                    lego_df = place_brick(lego_df, x, y, z, size, brick_sizes.index(size) + 1)
                    break
    return lego_df


def generate_bom(lego_df):
    """
    Generates a Bill of Materials DataFrame for the LEGO structure.
    """
    bom_df = lego_df['brick_id'].value_counts().reset_index()
    bom_df.columns = ['brick_id', 'count']
    brick_sizes = {1: "1x1", 2: "2x2", 3: "3x2", 4: "4x2"}
    bom_df['brick_type'] = bom_df['brick_id'].map(brick_sizes)
    return bom_df[['brick_type', 'count']]


def visualize_lego(lego_df):
    """
    Visualizes the LEGO structure with 3D bars for each brick.
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Iterate through each brick and plot it
    for _, row in lego_df.iterrows():
        x, y, z = row['x'], row['y'], row['z']
        brick_id = row['brick_id']
        size = {1: (1, 1), 2: (2, 2), 3: (3, 2), 4: (4, 2)}.get(brick_id)
        
        if size:
            dx, dy = size
            ax.bar3d(x, y, z, dx, dy, 1, alpha=0.8, color=f'C{brick_id}')

    plt.title("LEGO-ized Structure")
    plt.show()


def main(stl_file_path, resolution=0.1):
    # Load STL file and extract vertices
    print(f"Loading STL file: {stl_file_path}")
    stl_mesh = mesh.Mesh.from_file(stl_file_path)
    vertices = stl_mesh.vectors

    # Voxelize model
    print("Voxelizing the model...")
    voxel_df = voxelize(vertices, resolution)

    # Convert to LEGO structure
    print("Converting to LEGO structure...")
    lego_df = legoize(voxel_df)

    # Visualize LEGO structure
    print("Visualizing LEGO structure...")
    visualize_lego(lego_df)

    # Generate BOM
    print("\nGenerating Bill of Materials...")
    bom_df = generate_bom(lego_df)
    print(bom_df)


if __name__ == "__main__":
    stl_file_path = 'test.stl'  # Replace with your STL file
    main(stl_file_path)
