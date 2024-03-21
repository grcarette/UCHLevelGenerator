from LevelGrid import LevelGrid
from LevelGenerator import LevelGenerator
from AutoOptimizer import AutoOptimizer
from ArrayPlotter import ArrayPlotter
import numpy as np
       
def generate_level(array_plotter):
    level_grid = LevelGrid([4,7], array_plotter)
    level_grid.Generate_Level()
    optimize_level(level_grid, array_plotter)
    
def optimize_level(level_grid,array_plotter):
    optimizer = AutoOptimizer(level_grid.array)
    optimizer.Optimize_Level()
    boundaries = [np.size(optimizer.arr, 1), np.size(optimizer.arr, 0)]
    generate_map(optimizer.block_list,boundaries, array_plotter, level_grid)

def generate_map(block_list, boundaries, array_plotter, level_grid):
    new_level = LevelGenerator(boundaries, level_grid.startgoal_pos)
    new_level.Generate_Level(block_list)

if __name__ == "__main__":
    array_plotter = ArrayPlotter()
    for i in range(1):
        generate_level(array_plotter)
    # test_arr = np.ones([9,9])
    # optimize_level(test_arr)


    
        

    