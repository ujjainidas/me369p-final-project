import csv

# Prices for each part type
PART_PRICES = {
    '5x5': 0.59,
    '4x5': 0.41,
    '4x4': 0.36,
    '3x5': 0.34,
    '3x4': 0.32,
    '3x3': 0.26,
    '2x5': 0.27,
    '2x4': 0.21,
    '2x3': 0.17,
    '2x2': 0.13,
    '1x5': 0.26,
    '1x4': 0.16,
    '1x3': 0.15,
    '1x2': 0.10,
    '1x1': 0.07,
}

def read_parts_from_csv(file_path):
    """
    Reads the part types from the CSV file and returns a count of each type.
    
    :param file_path: Path to the input CSV.
    :return: Dictionary with part types as keys and counts as values.
    """
    part_counts = {}
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        
        if 'Part Type' not in reader.fieldnames:
            raise ValueError("CSV must have a column named 'part'")
        
        for row in reader:
            part = row['Part Type']
            if part in part_counts:
                part_counts[part] += 1
            else:
                part_counts[part] = 1
    
    return part_counts

def generate_bom(part_counts):
    """
    Generates the Bill of Materials (BOM) from the part counts.
    
    :param part_counts: Dictionary of part types and their counts.
    :return: List of BOM entries as dictionaries.
    """
    bom = []
    
    for part, quantity in part_counts.items():
        if part not in PART_PRICES:
            raise ValueError(f"Unknown part type: {part}")
        
        cost_per_part = PART_PRICES[part]
        total_cost = cost_per_part * quantity
        bom.append({
            "Part Type": part,
            "Quantity": quantity,
            "Cost per Part": round(cost_per_part, 2),
            "Total Cost": round(total_cost, 2)
        })
    
    return bom

def write_bom_to_csv(bom, output_file_path):
    """
    Writes the BOM data to a CSV file.

    :param bom: List of dictionaries representing the BOM.
    :param output_file_path: Path to save the BOM CSV.
    """
    with open(output_file_path, mode='w', newline='') as file:
        fieldnames = ["Part Type", "Quantity", "Cost per Part", "Total Cost"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bom)

# Main script
def main():
    input_csv_path = "Test_Brick_v1_voxel_2_parts.csv"  # CSV Input
    output_csv_path = "Test_Brick_v1_voxel_2_parts_bom.csv"  # CSV Output
    
    try:
        # Read parts and count occurrences
        part_counts = read_parts_from_csv(input_csv_path)
        
        # Generate the BOM
        bom = generate_bom(part_counts)
        
        # Write the BOM to a new CSV
        write_bom_to_csv(bom, output_csv_path)
        print(f"BOM has been successfully written to {output_csv_path}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

