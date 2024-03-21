import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class AutoOptimizer:
    def __init__(self,arr):
        self.arr = arr
        self.current_colour = 1
        self.empty_block = 0
        self.bg_block = 1
        self.aesthetic_block = 2
        self.shape_list = []
        self.block_shapes = [ #[x,y,blockID,offsetX,offsetY,rz]
            [1,1,40,0,0,0],
            [2,1,41,0,0,0],
            [1,2,41,0,1,270],
            [3,1,42,1,0,0],
            [1,3,42,0,1,270],
            [4,1,43,1,0,0],
            [1,4,43,0,2,270],
            [8,1,44,4,0,0],
            [1,8,44,0,3,270],
            [16,1,45,7,0,0],
            [1,16,45,0,8,270],
            [2,2,47,0,1,0],
            [2,4,46,1,2,270],
            [4,2,46,1,1,0],
            [4,4,48,1,2,0],
            [8,8,49,3,4,0],
            [6,16,50,2,8,0],
            [16,6,50,8,3,270]
        ]
        self.block_list = []
        self.colour_dict = {
            0 : ["0.2083694","0.291612","0.6911675"],
            1 : ["0.1764706","0.1764706","0.1764706"],
            2 : ["0.2039216","0.2039216","0.2039216"],
            3 : ["0.253", "0.253", "0.253"],
            4 : ["0.3308824", "0.3308824", "0.3308824"]
        }
            
    def Plot_Matrix(self, arr):
        colours_float = {key: [float(val) for val in value] for key, value in self.colour_dict.items()}
        cmap = ListedColormap(colours_float.values())
        plt.imshow(arr, cmap=cmap)
        plt.gca().invert_yaxis()
        plt.show()
        
    def Optimize_Level(self):
        uncropped_rows = np.any(self.arr != 1, axis = 1)
        uncropped_cols = np.any(self.arr != 1, axis = 0)
        self.arr = self.arr[uncropped_rows][:,uncropped_cols]
        self.arr = np.pad(self.arr, pad_width = 1, mode='constant', constant_values=0)
        
        for colour in range(1,5):
            self.current_colour = colour
            self.shape_list = []
            self.Find_Shapes()
            for shape in self.shape_list:
                self.Optimize_Shape(shape)
            self.Plot_Matrix

            
    def Find_Shapes(self):
        arr_rows = np.size(self.arr,0)
        arr_cols = np.size(self.arr,1)
        for y in range(arr_cols):
            for x in range(arr_rows):
                if self.arr[x,y] == self.current_colour:
                    self.arr[x,y] = 7
                    self.arr[x,y] = self.current_colour
                    self.shape_list.append((self.Produce_Shape(np.zeros((arr_rows, arr_cols)),(x,y))))

    def Produce_Shape(self, shape_mat, position):
        queue = [position]
        shape_mat[position] = 1
        self.arr[position] = 5
        while len(queue) != 0:
            position = queue[0]
            adjacent_tiles = [(position[0]+1, position[1]),(position[0]-1, position[1]),(position[0], position[1]+1),(position[0], position[1]-1)]
            for tile in adjacent_tiles:
                if self.arr[tile] == self.current_colour:
                    queue.append(tile)
                    shape_mat[tile] = 1
                    self.arr[tile] = 5
            queue.remove(position)
        return shape_mat
    
    def Crop_Level(self):
        bounds = self.Crop_Shape(self.arr, self.bg_block)
        self.arr = self.arr[bounds[2]:bounds[3],bounds[0]:bounds[1]]
        self.arr = np.pad(self.arr, pad_width = 1, mode='constant', constant_values=0)
        

    def Iterate_Axis(self, shape, ax, block_type, ismax):
        max_val = np.size(shape, ax)
        if ismax:
            for i in reversed(range(max_val)):
                if np.any(shape != block_type, axis=ax):
                    return i
        else:
            for i in range(max_val):
                if np.any(shape != block_type, axis=ax):
                    return i
        
    def Crop_Shape(self, shape, block_type):      
        col_lst = [np.any(row) for row in shape]
        row_lst = [np.any(col) for col in shape.T]

        min_row = row_lst.index(True)
        max_row = len(row_lst) - row_lst[::-1].index(True)
        min_col = col_lst.index(True)
        max_col = len(col_lst) - col_lst[::-1].index(True)

        return [min_col,max_col,min_row,max_row]
    
    def Optimize_Shape(self, shape):
        crop = self.Crop_Shape(shape, self.empty_block)
        fitting_blocks = []
        for block in self.block_shapes:
            if block[1] <= (crop[1] - crop[0]) and block[0] <= (crop[3] - crop[2]):
                fitting_blocks.insert(0,block)
                
        for block in fitting_blocks:
            for x in range(crop[0],crop[1]-(block[1])+1):
                for y in range(crop[2],crop[3]-(block[0])+1):
                    if self.arr[x,y] == 5:
                        if np.all(self.arr[x:x+block[1],y:y+block[0]] == 5):
                            self.block_list.append([y,x,block[2],block[3],block[4],block[5], self.current_colour])
                            self.arr[x:x+block[1],y:y+block[0]] = block[2]
                        
if __name__ == "__main__":
    # test_matrix = np.ones([3,3])
    # # test_matrix = np.random.randint(2, size=(8,8))
    # test_matrix = np.pad(test_matrix, pad_width = 1, mode='constant', constant_values=0)
    # opt = AutoOptimizer(test_matrix)
    # opt.Optimize_Level()
    a = [1,2,3,4,5,6,7,8]
    print(a[2:6])

