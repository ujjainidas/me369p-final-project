import csv
from collections import defaultdict

def read_voxel_data(file_path):
    """Read voxel data from CSV file."""
    voxels = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            voxels.append({
                "x": float(row["x"]),
                "y": float(row["y"]),
                "z": float(row["z"]),
            })
    return voxels

def group_voxels_into_bricks(voxels, voxel_size):
    """Group voxels into bricks (rectangular blocks)."""
    voxel_map = defaultdict(list)
    for voxel in voxels:
        # Group by voxel grid coordinates
        key = (int(voxel["x"] / voxel_size), int(voxel["y"] / voxel_size), int(voxel["z"] / voxel_size))
        voxel_map[key].append(voxel)
    
    bricks = []
    for key, brick_voxels in voxel_map.items():
        x_coords = [v["x"] for v in brick_voxels]
        y_coords = [v["y"] for v in brick_voxels]
        z_coords = [v["z"] for v in brick_voxels]
        dimensions = (
            round((max(x_coords) - min(x_coords) + voxel_size), 2),
            round((max(y_coords) - min(y_coords) + voxel_size), 2),
            round((max(z_coords) - min(z_coords) + voxel_size), 2),
        )
        bricks.append({
            "dimensions": dimensions,
            "count": len(brick_voxels)
        })
    return bricks

def calculate_cost(bricks, cost_per_unit_volume):
    """Calculate cost for each brick and total cost."""
    for brick in bricks:
        volume = brick["dimensions"][0] * brick["dimensions"][1] * brick["dimensions"][2]
        brick["volume"] = volume
        brick["cost"] = round(volume * cost_per_unit_volume, 2)
    
    total_cost = sum(brick["cost"] for brick in bricks)
    return bricks, total_cost

def export_bom(bricks, total_cost, output_file):
    """Export the BOM to a CSV file."""
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Brick Dimensions (x, y, z)", "Number of Voxels", "Cost per Brick ($)", "Volume per Brick (units³)"])
        for brick in bricks:
            writer.writerow([
                f"{brick['dimensions'][0]} x {brick['dimensions'][1]} x {brick['dimensions'][2]}",
                brick["count"],
                brick["cost"],
                brick["volume"]
            ])
        writer.writerow(["Total", "", total_cost, ""])

def main():
    voxel_file = 'voxel_data.csv'  # Input voxel data file from voxelize.py
    bom_output_file = 'voxel_bom.csv'  # Output BOM file
    voxel_size = 1.0  # Voxel size used in voxelize.py
    cost_per_unit_volume = 10.0  # Cost per unit volume for a brick
    
    # Read voxel data
    voxels = read_voxel_data(voxel_file)

    # Group voxels into bricks
    bricks = group_voxels_into_bricks(voxels, voxel_size)

    # Calculate costs
    bricks, total_cost = calculate_cost(bricks, cost_per_unit_volume)

    # Export BOM
    export_bom(bricks, total_cost, bom_output_file)

if __name__ == "__main__":
    main()
