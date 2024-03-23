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
            4 : ["0.3308824", "0.3308824", "0.3308824"],
            5 : ["0.1911765", "0.1084139", "0.07590831"]
        }
            
    def Plot_Matrix(self, arr):
        # colours_float = {key: [float(val) for val in value] for key, value in self.colour_dict.items()}
        # cmap = ListedColormap(colours_float.values())
        plt.imshow(arr)
        plt.gca().invert_yaxis()
        plt.show()
        
    def Optimize_Level(self):
        for colour in range(1, len(self.colour_dict)):
            self.current_colour = colour
            self.shape_list = []
            self.Find_Shapes()
            
            for shape in self.shape_list:
                self.Optimize_Shape(shape)
        # self.Plot_Matrix(self.arr)
            
    def Find_Shapes(self):
        arr_rows = np.size(self.arr,0)
        arr_cols = np.size(self.arr,1)
        tmp_arr = np.copy(self.arr)
        for col in range(arr_cols):
            for row in range(arr_rows):
                if tmp_arr[row,col] == self.current_colour:
                    self.shape_list.append((self.Produce_Shape(tmp_arr, (row,col))))

    def Produce_Shape(self, arr, position):
        shape = [position]
        queue = [position]
        visited = 10
        arr[position] = visited
        while len(queue) != 0:
            position = queue[0]
            adjacent_tiles = [(position[0]+1, position[1]),(position[0]-1, position[1]),(position[0], position[1]+1),(position[0], position[1]-1)]
            for tile in adjacent_tiles:
                if arr[tile] == self.current_colour:
                    queue.append(tile)
                    shape.append(tile)
                    arr[tile] = visited
            queue.remove(position)
        return shape
        
    def Crop_Shape(self, shape):
        min_x = min([coord[1] for coord in shape])
        max_x = max([coord[1] for coord in shape])
        min_y = min([coord[0] for coord in shape])
        max_y = max([coord[0] for coord in shape])

        return [min_x, max_x, min_y, max_y]
        
    def Optimize_Shape(self, shape):
        fitting_blocks = []
        full_positions = []
        crop = self.Crop_Shape(shape)
        for block in self.block_shapes:
            if block[1] <= (crop[3] - crop[2] + 1) and block[0] <= (crop[1] - crop[0] + 1):
                fitting_blocks.insert(0,block)

        for block in fitting_blocks:
            shape = [position for position in shape if position not in full_positions]
            full_positions.extend(self.Fit_Block(shape, block))
    
    def Fit_Block(self, shape, block):
        full_positions = []
        for position in shape:
            if np.all(self.arr[position[0]:position[0]+block[1],position[1]:position[1]+block[0]] == self.current_colour):
                self.block_list.append([position[1],position[0],block[2],block[3],block[4],block[5], self.current_colour])
                self.arr[position[0]:position[0]+block[1],position[1]:position[1]+block[0]] = block[2]
                full_positions.extend([pos for pos in shape if position[0] <= pos[0] <= position[0]+block[1] - 1 and position[1] <= pos[1] <= position[1]+block[0] - 1])
                
        return full_positions

if __name__ == "__main__":
    # test_matrix = np.random.randint(2, size=(128,128))
    # test_matrix = np.pad(test_matrix, pad_width = 1, mode='constant', constant_values=0)
    # opt = AutoOptimizer(test_matrix)
    # opt.Optimize_Level()
    pass

