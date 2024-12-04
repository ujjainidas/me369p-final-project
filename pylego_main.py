import voxelize
import legoizer
import voxel_bom
import visualize

def main():
    print("Starting voxelize...")
    voxelize.main()
    print("Voxelize completed.")
    
    print("Starting legoizer...")
    legoizer.main()
    print("Legoizer completed.")
    
    print("Starting voxel_bom...")
    voxel_bom.main()
    print("Voxel BOM completed.")
    
    print("Starting visualize...")
    visualize.main()
    print("Visualization completed.")
    
    print("All processes completed successfully.")

if __name__ == "__main__":
    main()
