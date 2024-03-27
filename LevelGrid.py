import numpy as np
import matplotlib.pyplot as plt
import random
import math
from ArrayPlotter import ArrayPlotter

class LevelGrid:
    def __init__(self,array_plotter, level_args, test_display = 0):
        self.array_plotter = array_plotter
        self.test_display = test_display
        
        self.map_size = level_args[0]
        self.map_theme = level_args[1]
        self.thickness = level_args[2]
        self.music = level_args[3]
        self.asset_frequency = level_args[4]
        self.background = level_args[5]
        self.curve_intensity = int(float(level_args[6]))
        self.smooth_scaling = int(float(level_args[7]))
        
        self.step_list = []
        self.point_list = []
        self.line_points = []
        self.max_size = [4,5]
        self.startgoal_pos = []
        self.goal_rz = 0
        self.first_step = []
        self.last_step = []
        
        self.has_girders = True
        self.has_platforms = True
        
        self.special_blocks = []
        self.special_offset_row = 0
        self.special_offset_col = 0
        
        self.map_sizes = {
            "Small" : [7,9],
            "Medium" : [10,12],
            "Large" : [13,20],
        }
        self.map_size = self.map_sizes[self.map_size]
        
        self.pad_width = 4
        self.max_block_size = 22
        self.uch_level_size = (self.max_block_size*self.max_size[0],self.max_block_size*self.max_size[1])
        self.empty_block = 0
        self.aesthetic_block = 2
        self.filled_empty_block = 10
        self.expansion_const = 100
        self.overlap_const = 50
            
        self.steparray = np.ones(self.max_size).astype(int)
        self.steparray = np.pad(self.steparray, pad_width = self.pad_width, mode='constant', constant_values=0).astype(int)
        self.array = np.ones(self.uch_level_size).astype(int)
        self.Generate_Level()
        
    def Generate_Level(self):
        self.Path_Find()
        if self.test_display in [2,3]:
            self.array_plotter.Plot_Array(self.steparray)
        
        self.Generate_Points()
        if self.test_display in [1,3]:
            self.array_plotter.Plot_Array(self.array)
            
        self.Curve_Path()
        if self.test_display in [1,3]:
            self.array_plotter.Plot_Array(self.array)
            
        self.Connect_Lines()
        if self.test_display in [1,3]:
            self.array_plotter.Plot_Array(self.array,"rocky")
            
        self.Polish_Path()
        if self.test_display in [1,3]:
            self.array_plotter.Plot_Array(self.array, "rocky")

        self.Crop_Level()
        if self.test_display in [1,3]:
            self.array_plotter.Plot_Array(self.array, "rocky")

        self.Place_StartGoal()
        self.Add_Assets()

        
        if self.test_display == 1:
            self.array_plotter.Plot_Array(self.array, "rocky")
            
        if self.test_display == 4:
            self.array_plotter.Plot_Array(self.array, "rocky")
        
    def Path_Find(self):
        can_step = True
        current_step = 2 #Arbitrary. Must be above 1 so we can use np.ones and pad with 0's
        all_steps = [[0,1],[0,-1],[1,1],[1,-1],[-1,-1],[-1,1],[1,0],[-1,0]]
        starting_row = random.randint(self.pad_width, self.max_size[1]+self.pad_width-1)
        starting_col = random.randint(self.pad_width, self.max_size[0]+self.pad_width-1)
        current_position = [starting_row, starting_col]
        
        cons_horizontal = 0
        cons_diagonal = 0
        max_horizontal = 2
        last_horizontal = 2
        max_diagonal = 1
        last_diagonal = 6
        
        self.step_list.append([current_position[1], current_position[0]])
    
        while can_step:
            self.steparray[current_position[1],current_position[0]] = current_step
            
            if self.test_display == 3:
                self.array_plotter.Plot_Array(self.steparray)
            
            valid_steps = []

            for step in all_steps:
                if self.steparray[current_position[1]+step[1],current_position[0]+step[0]] == 1:
                    if step in all_steps[last_horizontal:last_diagonal]:
                        if self.steparray[current_position[1], current_position[0] + step[0]] == 1 or self.steparray[current_position[1] + step[1], current_position[0]] == 1:
                            valid_steps.append(step)
                    else:
                        valid_steps.append(step)
                                    
            if len(valid_steps) == 0 or current_step >= self.map_size[1]:
                can_step = False
            else:
                preferred_steps = [
                    step for step in valid_steps if step not in all_steps[max_horizontal*(cons_horizontal<max_horizontal):max_horizontal+(cons_diagonal*4)]
                    ]
                if len(preferred_steps) == 0:   
                    next_step = random.choice(valid_steps)
                else:
                    next_step = random.choice(preferred_steps)
                    if next_step in all_steps[:last_horizontal]:
                        cons_horizontal += 1
                        cons_diagonal = 0
                    elif next_step in all_steps[last_horizontal:last_diagonal]:
                        cons_diagonal += 1
                        cons_horizontal = 0
                    else:
                        cons_horizontal = 0
                        cons_diagonal = 0

                current_position[0] += next_step[0]
                current_position[1] += next_step[1]
                self.step_list.append([current_position[1], current_position[0]])
                if current_step == 2:
                    self.first_step = next_step
                self.last_step = next_step
                current_step += 1

        if len(self.step_list) < self.map_size[0]:
            self.steparray = np.ones(self.max_size)
            self.steparray = np.pad(self.steparray, pad_width = self.pad_width, mode='constant', constant_values=0)
            self.step_list = []
            self.Path_Find()

            
    def Plot_Points(self, point_list, val):
        for point in point_list:
            self.array[point[0],point[1]] = val
                
    def Generate_Points(self):
        if self.thickness == 'Thin':
            thickness_offset = -3
        if self.thickness == 'Regular':
            thickness_offset = 0
        if self.thickness == 'Thick':
            thickness_offset = 3
            
        chunk_pad = self.pad_width*2 + thickness_offset
        for step in self.step_list:
            point_x = self.max_block_size * (step[0]-self.pad_width) + random.randint(chunk_pad, self.max_block_size - chunk_pad)
            point_y = self.max_block_size * (step[1]-self.pad_width) + random.randint(chunk_pad, self.max_block_size - chunk_pad)
            pos = [point_x, point_y]
            self.point_list.append(pos)
            if step == self.step_list[0] or step == self.step_list[-1]:
                self.startgoal_pos.append(pos)
        self.Plot_Points(self.point_list, self.empty_block)
        
    def Curve_Line(self, points, recursion_depth, max_recursion, point_c = False, angle_ac = False):
        min_coeff = 9
        max_coeff = 6
        if recursion_depth == max_recursion:
            return points
        else:
            new_points = [np.array(points[0])]
            for i in range(len(points)-1):
                magnitude = np.linalg.norm(points[i] - points[i+1])
                mid_point = np.array([(points[i][0] + points[i+1][0])/2, (points[i][1] + points[i+1][1])/2])
                p_vector = np.array(points[i+1]) - np.array(points[i])
                orth_p_vector = np.array([-p_vector[1], p_vector[0]])
                unit_vector = orth_p_vector / np.linalg.norm(orth_p_vector)
                
                if self.curve_intensity == 1:
                    min_coeff = 14
                    max_coeff = 11
                if self.curve_intensity == 2:
                    min_coeff = 12
                    max_coeff = 9
                if self.curve_intensity == 4:
                    min_coeff = 7
                    max_coeff = 5
                if self.curve_intensity == 5:
                    min_coeff = 5
                    max_coeff = 3
                
                if angle_ac:
                    if angle_ac < 90:
                        v_dc = point_c - mid_point
                        direction = 1
                        if np.dot(v_dc, orth_p_vector) > 0:
                            direction = -1
                        random_coeff = random.randint(math.floor((magnitude/min_coeff)), math.ceil((magnitude/max_coeff))) * direction     
                    else:
                        random_coeff = random.randint(math.floor((magnitude/min_coeff)), math.ceil((magnitude/max_coeff))) * random.choice([-1, 1])
                else:
                    random_coeff = random.randint(math.floor((magnitude/min_coeff)), math.ceil((magnitude/max_coeff))) * random.choice([-1, 1])
                    
                new_point = mid_point + unit_vector * random_coeff
                for j in range(2):
                    if new_point[j] < 0:
                        new_point[j] = 0
                    if new_point[j] >= np.shape(self.array)[j] - 1:
                        new_point[j] = np.shape(self.array)[j] - 2
                new_points.append(np.round(new_point).astype(int))
                new_points.append(np.array(points[i+1]))
            
            recursion_depth += 1
            return self.Curve_Line(new_points, recursion_depth, max_recursion)
        
    def Find_Angle(self, points):
        v_ab = np.array(points[0] - points[1])
        v_bc = np.array(points[2] - points[1])
        mag_ab = np.linalg.norm(v_ab)
        mag_bc = np.linalg.norm(v_bc)
        cos_angle = np.dot(v_ab, v_bc) / (mag_ab * mag_bc)
        angle_ac = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))
        return angle_ac

    def Curve_Path(self):
        min_line_coeff = 8
        max_line_coeff = 10
        curved_points = []
        max_iteration = len(self.point_list)-1
        for i in range(max_iteration):
            points = np.array((self.point_list[i:i+2]))
            distance = np.linalg.norm(points[0] - points[1])
            max_recursion = random.randint(math.floor(distance/max_line_coeff), math.floor(distance/min_line_coeff)) #We want longer lines to be more likely to curve
            
            if(i <= (max_iteration - 2)):
                points = np.array((self.point_list[i:i+3]))
                angle_ac = self.Find_Angle(points)
                
                new_points = self.Curve_Line(points[0:2], 0, max_recursion, points[2], angle_ac)
            else:
                points = np.array((self.point_list[i:i+2]))
                new_points = self.Curve_Line(points[0:2], 0, max_recursion)
            curved_points.extend(new_points)
        
        curved_points.append(self.point_list[-1])
        self.point_list = curved_points
        self.Plot_Points(self.point_list, self.empty_block)
            
    def Connect_Lines(self):
        for i in range(len(self.point_list)-1):
            points = np.array((self.point_list[i:i+2]))
            
            if points[0][0] == points[1][0]:
                distance = points[0][1] - points[1][1]
                if points[0][1] < points [1][1]:
                    j = 0
                else:
                    j = 1
                for i in range(abs(distance)):
                    self.array[points[j][0],points[j][1]+i] = self.empty_block
                    self.line_points.append([points[j][0],points[j][1]+i])
            elif points[0][1] == points[1][1]:
                distance = points[0][0] - points[1][0]
                if points[0][0] < points [1][0]:
                    j = 0
                else:
                    j = 1
                for i in range(abs(distance)):
                    self.array[points[j][0]+i,points[j][1]] = self.empty_block
                    self.line_points.append([points[j][0]+i,points[j][1]])
            else:
                coeff = np.polyfit(points[:,0], points[:,1],1)
                polynomial = np.poly1d(coeff)
                
                if self.thickness == 'Thin':
                    freq = 16
                else:
                    freq = 8
                
                x_axis = np.linspace(points[0,0], points[1,0], freq)
                y_axis = polynomial(x_axis)
                
                new_points = np.round(np.dstack((x_axis, y_axis)).astype(int)[0])
                
                for point in new_points:
                    self.array[point[0],point[1]] = self.empty_block
                    self.line_points.append(point)

    def Find_Side(self, side, offset=0):
        side_block_list = []
        pad = 2
        if side == 'b':
            for row in range(pad, np.shape(self.array)[0] - pad):
                for col in range(1, np.shape(self.array)[1] - pad):
                    current_block = self.array[row,col]
                    next_block = self.array[row-1,col]
                    previous_block = self.array[row+1, col]
                    if current_block != self.empty_block and next_block != self.empty_block and previous_block == self.empty_block:
                        side_block_list.append([row,col])
                        
        if side == 'r' or side == 'l':
            for row in range(pad, np.shape(self.array)[0] - pad):
                for col in range(pad, np.shape(self.array)[1] - pad):
                    previous_block = self.array[row,col-1]
                    current_block = self.array[row,col]
                    next_block = self.array[row,col+1]
                    if current_block == self.aesthetic_block and next_block == self.empty_block and side == 'l':
                        if offset != 0 or previous_block != self.empty_block:
                            side_block_list.append([row,col+offset])
                    if current_block == self.aesthetic_block and previous_block == self.empty_block and side == 'r':
                        if offset != 0 or next_block != self.empty_block:
                            side_block_list.append([row,col+offset])
        return side_block_list
        
    def Apply_Noise(self, point_list, type, applying_twice=False):
        if type == 't': #terrain
            val = self.empty_block
            if self.smooth_scaling == 1:
                min_coeff = 2
                max_coeff = 3
            if self.smooth_scaling == 2:
                min_coeff = 2
                max_coeff = 4
            if self.smooth_scaling == 3:
                if applying_twice:
                    min_coeff = 4
                    max_coeff = 8
                else:
                    min_coeff = 2
                    max_coeff = 5
            if self.smooth_scaling == 4:
                min_coeff = 4
                max_coeff = 8
            
        if type == 'd': #decoration
            min_coeff = 1
            max_coeff = 5
        i = 0
        for point in point_list:
            if i % 10 == 0: 
                rocky_coefficient = random.randint(min_coeff,max_coeff)
            if type == 'd':
                shading_coeff = random.randint(min_coeff,4)
                if shading_coeff == 1:
                    val = 4
                else:
                    val = 3
                self.array[point[0], point[1]] = val
            else:
                if random.randint(1,rocky_coefficient) == 1:
                    self.array[point[0], point[1]] = val
            i+= 1

    def Polish_Path(self):
        self.Expand_Path()
        
        side_coeff = 1
        if self.smooth_scaling < 3:
            rocky_coeff = 2
        elif self.smooth_scaling == 3:
            rocky_coeff = random.randint(1,2)
        else:
            rocky_coeff = 2
            side_coeff = 2
        
        for i in range(rocky_coeff):
            bottom_block_list = self.Find_Side('b')
            self.Apply_Noise(bottom_block_list,'t')
        
        if self.smooth_scaling != 5:
            for i in range(side_coeff):
                left_block_list = self.Find_Side('l')
                self.Apply_Noise(left_block_list, 't')
                
                right_block_list = self.Find_Side('r')
                self.Apply_Noise(right_block_list, 't')
        
        bottom_block_list = self.Find_Side('b')
        self.Apply_Noise(bottom_block_list, 'd')


    def Expand_Path(self):
        self.array = np.pad(self.array, pad_width = self.pad_width, mode='constant', constant_values=0)
        min_variance = 2
        max_variance = 10
        next_change = random.randint(min_variance, max_variance)
        
        min_padding_x = 2 
        max_padding_x = 3
        min_padding_y = 2
        max_padding_y = 3
        
        if self.thickness == 'Thin':
            min_padding_x -= 1
            min_padding_y -= 1
        
        if self.thickness == 'Thick':
            min_padding_x += 1
            max_padding_x += 1
            min_padding_y += 1
            max_padding_y += 1

        padding = [2, 2, 2, 2]
        pad_left = padding[0]
        pad_right = padding[1]
        pad_down = padding[2]
        pad_up = padding[3]
        current_step = 1
        
        for point in self.line_points:
            if current_step % next_change == 0:
                pad_left += random.choice([num for num in [-1,0,1] if min_padding_x <= (pad_left + num) <= max_padding_x])
                pad_right += random.choice([num for num in [-1,0,1] if min_padding_x <= (pad_right + num) <= max_padding_x])
                pad_down += random.choice([num for num in [-1,0,1] if min_padding_y <= (pad_down + num) <= max_padding_y])
                pad_up += random.choice([num for num in [-1,0,1] if min_padding_y <= (pad_up + num) <= max_padding_y])
                
                next_change = random.randint(min_variance, max_variance)
                
             
                padding = [pad_left, pad_right, pad_down, pad_up]
            current_step += 1
            self.Expand_From_Point(point, padding, self.empty_block, current_step)
            self.Expand_From_Point(point, padding, self.aesthetic_block, current_step)
            
        for row in range(np.shape(self.array)[0]):
            for col in range(np.shape(self.array)[1]):
                if self.array[row,col] >= self.expansion_const:
                    self.array[row,col] = self.empty_block
        self.array = self.array[self.pad_width:-self.pad_width,self.pad_width:-self.pad_width]
        
    def Expand_From_Point(self, point, padding, block_type, current_step):
        x_min = point[0] - padding[0] + self.pad_width - block_type
        x_max = point[0] + padding[1] + self.pad_width + block_type
        y_min = point[1] - padding[2] + self.pad_width - block_type
        y_max = point[1] + padding[3] + self.pad_width + block_type
        if self.thickness == 'Thin':
            self.overlap_const = 120
        if self.thickness == 'Thick':
            self.overlap_const = 40
        current_val = current_step + self.expansion_const
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):  
                if not ((x == x_min or x == x_max-1) and(y == y_min or y == y_max-1)): 
                    if self.array[x,y] != self.empty_block:
                        if block_type == self.empty_block:
                            self.array[x,y] = current_val
                        else:
                            if self.array[x,y] < self.expansion_const:
                                self.array[x,y] = block_type
                            elif self.Check_Border([x,y], current_step) and self.array[x,y] == current_val:
                                self.array[x,y] = block_type
                                
    def Check_Border(self, point, current_step):
        adjacent_blocks = [[0,1],[1,0],[0,-1],[-1,0]]
        current_val = current_step + self.expansion_const
        border_count = 0
        if self.expansion_const <= self.array[point[0], point[1]] <= (current_val - self.overlap_const):
            return False
        for dir in adjacent_blocks:
            if (self.expansion_const <= self.array[point[0]+dir[0], point[1]+dir[1]] <= (current_val - self.overlap_const)):
                border_count +=1
        if border_count != 0:
            return True
    
    def Place_StartGoal(self):
        start_width = 4
        start_offset_l = -2
        start_offset_r = 2
        start_offset_y = 4
        safe_offset  = 1
        goal_offset_y = -1
        goal_safespot_y = -7
        goal_left = -2
        goal_right = 4
        girder_offset = 3
        
        if self.first_step == [0, -1]:
            self.startgoal_pos[0][0] += start_offset_y
            start_offset_y = 1
            while np.any(self.array[self.startgoal_pos[0][0] + start_offset_y, self.startgoal_pos[0][1] + start_offset_l:self.startgoal_pos[0][1]+start_offset_r] != 0):
                self.startgoal_pos[0][0] -= 1
                
            self.startgoal_pos[0][0] -= 1
            self.special_blocks.append(["scaffold", self.startgoal_pos[0][1]+start_offset_l, self.startgoal_pos[0][0], 0, 5])
            self.special_blocks.append(["scaffold", self.startgoal_pos[0][1]+start_offset_l+start_width-1, self.startgoal_pos[0][0], 0, 5]) 
        else:
            while np.all(self.array[self.startgoal_pos[0][0]-1,self.startgoal_pos[0][1] + start_offset_l:self.startgoal_pos[0][1] + start_offset_r] == 0):
                self.startgoal_pos[0][0] -= 1
            self.array[self.startgoal_pos[0][0]+goal_offset_y, self.startgoal_pos[0][1] + start_offset_l: self.startgoal_pos[0][1] + start_offset_r] = 5

                                
        if self.last_step == [0,1]:
            goal_offset_y = 1
            self.goal_rz = 180
            
        while self.array[self.startgoal_pos[1][0]][self.startgoal_pos[1][1]] == 0:
            self.startgoal_pos[1][0] += goal_offset_y

        if self.last_step == [0,1] and random.randint(0,1) == 1:
            self.array[self.startgoal_pos[1][0] + goal_safespot_y:self.startgoal_pos[1][0], self.startgoal_pos[1][1] + goal_left: self.startgoal_pos[1][1] + goal_right] = 0
            self.special_blocks.append(["scaffold", self.startgoal_pos[1][1]+start_offset_l+1, self.startgoal_pos[1][0]-start_width, 0, 5])
            self.special_blocks.append(["scaffold", self.startgoal_pos[1][1]+start_offset_l+start_width, self.startgoal_pos[1][0]-start_width, 0, 5])
            self.array[self.startgoal_pos[1][0]- start_width - goal_offset_y, self.startgoal_pos[1][1] - goal_offset_y:self.startgoal_pos[1][1] + goal_right - 1] = 5
            
        safe_offset_t = 3
        offset_l = start_offset_l - safe_offset
        offset_r = start_offset_r + safe_offset        
        self.array[self.startgoal_pos[0][0] + safe_offset:self.startgoal_pos[0][0] + safe_offset_t, self.startgoal_pos[0][1] + offset_l: self.startgoal_pos[0][1] + offset_r] = 0
            
    def Crop_Level(self):
        padding = 1
        
        crop = np.where(self.array != 1)
        
        crop_row_start = np.min(crop[0])
        crop_row_end = np.max(crop[0])
        crop_col_start = np.min(crop[1])
        crop_col_end = np.max(crop[1])

        self.array = self.array[crop_row_start:crop_row_end+padding, crop_col_start:crop_col_end+padding]
        self.array = np.pad(self.array, pad_width = padding, mode='constant', constant_values=1)
        self.array = np.pad(self.array, pad_width = padding, mode='constant', constant_values=0)
        
        self.special_offset_row = crop_row_start
        self.special_offset_col = crop_col_start
        
        self.startgoal_pos[0][0] -= self.special_offset_row - padding 
        self.startgoal_pos[0][1] -= self.special_offset_col - padding - 1
        
        self.startgoal_pos[1][0] -= self.special_offset_row - padding
        self.startgoal_pos[1][1] -= self.special_offset_col - padding
        
    def Find_Nearest_Walls(self, point):
        nearby_points = []
        origin_point = point
        directions = [[-1,0], [1,0], [0,-1], [0,1]]
        tmp_arr = np.copy(self.array)
        tmp_arr[origin_point[0], origin_point[1]] = 12
        for direction in directions:
            current_point = origin_point.copy()
            
            while self.array[current_point[0], current_point[1]] == 0 or self.array[current_point[0], current_point[1]] == self.filled_empty_block:
                current_point[0] += direction[0]
                current_point[1] += direction[1]
                tmp_arr[current_point[0], current_point[1]] += 8
                if self.array[current_point[0], current_point[1]] != 0 and self.array[current_point[0], current_point[1]] != self.filled_empty_block:
                    nearby_points.append(current_point)
        return nearby_points #[min_row, max_row, min_col, max_col]
    
    def Place_Girder(self, point):
        nearest_points = self.Find_Nearest_Walls(point)
        hor_dist = nearest_points[3][1] - nearest_points[2][1]
        vert_dist = nearest_points[1][0] - nearest_points[0][0]
        offset_list = [
            [0,0],
            [1,0],
            [1,-1],
            [2,-1],
            [2,-2]
        ]
        
        if vert_dist <= hor_dist:
            remainder = vert_dist % 5
            num_girder = int((vert_dist - remainder) / 5)
            for i in range(num_girder):
                self.special_blocks.append(["scaffold", point[1], nearest_points[0][0] + i*5 + offset_list[remainder][0], 0, 5])
            self.array[nearest_points[0][0]:nearest_points[0][0]+offset_list[remainder][0], point[1]] = 5
            self.array[nearest_points[1][0]+offset_list[remainder][1]:nearest_points[1][0], point[1]] = 5
            self.array[nearest_points[0][0]+offset_list[remainder][0]:nearest_points[1][0]+offset_list[remainder][1], point[1]] = self.filled_empty_block
        else:
            remainder = hor_dist % 5
            num_girder = int((hor_dist - remainder) / 5)
            for i in range(num_girder):
                self.special_blocks.append(["scaffold", nearest_points[2][1] + i*5 + offset_list[remainder][0], point[0], 270, 5])
            self.array[point[0], nearest_points[2][1]:nearest_points[2][1]+offset_list[remainder][0]] = 5
            self.array[point[0], nearest_points[3][1] + offset_list[remainder][1]:nearest_points[3][1]] = 5
            self.array[point[0], nearest_points[2][1]+offset_list[remainder][0]:nearest_points[3][1] + offset_list[remainder][1]] = self.filled_empty_block
            
    def Add_Girders(self, num_girders):
        girder_padding = 5
        girder_count = 0
        safe_r_offset = 3
        safe_l_offset = -2
        
        while girder_count < num_girders:
            point = [random.randint(girder_padding, np.shape(self.array)[0]-girder_padding), random.randint(girder_padding, np.shape(self.array)[1]-girder_padding)]
            if np.all(self.array[point[0]+safe_l_offset:point[0]+safe_r_offset, point[1]+safe_l_offset:point[1]+safe_r_offset] == self.empty_block):
                self.Place_Girder(point)
                girder_count += 1
        
    def Place_Platform(self, point, direction):
        if self.thickness == 'Thin':
            min_platform_size = 1
        else:
            min_platform_size = 2
        max_platform_size = 8
        mgs = 2 #min gap size. Small name because some of these lines are quite long
        current_platform_size = -1
        current_position = [point[0], point[1]]
        l_offset = mgs * direction[0] - direction[0]
        r_offset = mgs * direction[1] - direction[0]

        while np.all(self.array[current_position[0]-mgs:current_position[0]+mgs+1,current_position[1]+l_offset:current_position[1]+r_offset] == 0):
            current_position[1] += direction[2]
            current_platform_size += 1
        
        if current_platform_size <= min_platform_size:
            return False
        
        max_platform_size = min(max_platform_size, current_platform_size)
        platform_size = random.randint(min_platform_size, max_platform_size)
        
        if direction[2] == 1:
            self.array[point[0],point[1] : point[1] + platform_size] = 5
        if direction[2] == -1:
            self.array[point[0],point[1] - direction[2] - platform_size : point[1] - direction[2]] = 5
            
        if self.array[point[0]-1,point[1] - direction[2]] == 0:
            self.array[point[0]-1,point[1]-direction[2]] = 5
            if platform_size >= 3:
                self.array[point[0]-1,point[1]] = 5
        else:
            if platform_size > 3:
                j = 4
            if platform_size == 3:
                j = 3
            if platform_size < 3:
                j = 2
            
            for i in range(1,j):
                self.array[point[0]-i,point[1] + ((j - i - 1) * direction[2])] = 5
                if self.array[point[0]-i,point[1]-direction[2]] == self.empty_block:
                    self.array[point[0]-i,point[1]-direction[2]] = 5
        return True
        
    def Add_Platforms(self, num_left, num_right):
        left_wall = self.Find_Side('l', 1)
        right_wall = self.Find_Side('r', -1)
        min_platform_size = 5
        left_count = 0
        right_count = 0
        left_dir = [0,1,1]
        right_dir = [-1,0,-1]
        
        while left_count < num_left and len(left_wall) > 0:
            point = random.choice(left_wall)
            platform_fits = True
            for i in range(min_platform_size):
                if self.array[point[0] - i][point[1] + i] != self.empty_block:
                    platform_fits = False
            
            if platform_fits:
                if self.Place_Platform(point, left_dir):
                    left_count += 1
                else:
                    left_wall.remove(point)
            else:
                left_wall.remove(point)
        
        while right_count < num_right and len(right_wall) > 0:
            point = random.choice(right_wall)
            platform_fits = True
            for i in range(min_platform_size):
                if self.array[point[0] - i][point[1] - i] != self.empty_block:
                    platform_fits = False
            
            if platform_fits:
                if self.Place_Platform(point, right_dir):
                    right_count += 1
                else:
                    right_wall.remove(point)
            else:
                right_wall.remove(point)
        
    def Add_Assets(self):
        if self.asset_frequency == 'None':
            return        
        if self.asset_frequency == 'Low':
            asset_freq = 0.5
        if self.asset_frequency == 'Medium':
            asset_freq = 1
        if self.asset_frequency == 'High':
            asset_freq = 1.5
        
        min_girders = math.floor(self.map_size[0]/3)
        max_girders = math.floor(self.map_size[0]/2)
        num_girders = round(random.randint(min_girders, max_girders) * asset_freq)
        
        if self.has_girders:
            self.Add_Girders(num_girders)
        
        min_platforms = math.floor(self.map_size[0]/2)
        max_platforms = self.map_size[0] - 2
        num_platforms = round(random.randint(min_platforms, max_platforms) * asset_freq)
        num_left = random.randint(1, num_platforms-1)
        num_right = num_platforms - num_left
        
        if self.has_platforms:
            self.Add_Platforms(num_left, num_right)
            
                
if __name__ == "__main__":
    ap = ArrayPlotter()
    for i in range(1000):
        print(i)
        level = LevelGrid(ap, 0)

                    
                
            
            
        

            
    

                
            