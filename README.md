How to Use PyLego!!
Follow these steps to convert your STL model into a LEGO-style representation using PyLego:

1. Setup
   
  Create a folder and download the following Python files into it:
    voxelize.py
    legoizer.py
    voxel_bom.py
    visualize.py
    pylego_main.py
  Place your STL file in the same folder. We’ve provided a sample STL file in this repository that you can use.
  
2. Install Dependencies
   
Make sure to install the required Python packages by running:
  pip install pandas numpy matplotlib mpl_toolkits math random ast csv
  
3. Edit Python Files
   
  You need to modify specific lines in the provided scripts to work with your STL file. Follow these steps:
  
    a. voxelize.py
      Go to line 57 and specify the STL file you want to LEGO-ize.
      On line 58, update the desired name for the voxel CSV file.
    b. legoizer.py
      Go to line 174 and input the voxel CSV file name from step a.
      On line 189, specify the desired name for the LEGO-izer CSV file.
    c. voxel_bom.py
      Go to line 67 and input the LEGO-izer CSV file name from step b.
      On line 68, update the desired name for the Bill of Materials (BOM) CSV file.
    d. visualize.py
      Go to line 32 and input the LEGO-izer CSV file name from step b.
      
4. Run the Script
     
  Open pylego_main.py in your IDE and run it.
    This will generate all necessary CSV files (saved in the same folder) and display a 3D visualization of your LEGO-ized model.
    
Output
You’ll get the following files in the folder:
    Voxel CSV file
    LEGO-izer CSV file
    Bill of Materials CSV file
    A plot showing your LEGO-ized model will also be displayed.
Enjoy building with PyLego!

