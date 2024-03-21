import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class ArrayPlotter:
    def __init__(self):
        self.rock_colours = {
            0 : ["0.2083694","0.291612","0.6911675"],
            1 : ["0.1764706","0.1764706","0.1764706"],
            2 : ["0.2039216","0.2039216","0.2039216"],
            3 : ["0.253", "0.253", "0.253"],
            4 : ["0.3308824", "0.3308824", "0.3308824"]
        }
        self.colour_schemes = {
            "rocky" : self.rock_colours
        }

    def Plot_Array(self, arr, colour_scheme="default"):
        if colour_scheme == "default":
            plt.imshow(arr)
            plt.gca().invert_yaxis()
            plt.show()
        else:
            colours = {key: [float(val) for val in value] for key, value in self.colour_schemes[colour_scheme].items()}
            cmap = ListedColormap(colours.values())
            plt.imshow(arr, cmap=cmap)
            plt.gca().invert_yaxis()
            plt.show()