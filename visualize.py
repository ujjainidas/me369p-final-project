import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import ast
import matplotlib.cm as cm
import random

def plot_cube(ax, x, y, z, dx=1, dy=1, dz=1, color='b'):
    ax.bar3d(x, y, z, dx, dy, dz, color=color, alpha=0.8)

def visualize_lego(lego_df):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    colors = ['b', 'r', 'g', 'y', 'c', 'm', 'k']

    for idx, row in lego_df.iterrows():
        coordinates_str = row['Coordinates']
        
        coordinates = ast.literal_eval(coordinates_str)
        color = random.choice(colors)
        
        for (x, y, z) in coordinates:
            plot_cube(ax, x, y, z, dx=1, dy=1, dz=1, color=color)

    ax.set_title("LEGO-ized Structure")
    plt.show()

def load_lego_data(csv_file):
    lego_df = pd.read_csv(csv_file)
    return lego_df

csv_file = 'lego_parts.csv' 
lego_df = load_lego_data(csv_file)
visualize_lego(lego_df)