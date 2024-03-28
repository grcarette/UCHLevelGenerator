import xml.etree.ElementTree as ET
import random
import numpy as np
import math
import lzma
import os

class SnapshotCreator:
    def __init__(self, levelgrid, optimizer, theme_attributes, is_default_values):
        self.root = ET.Element("scene")
        self.block_list = optimizer.block_list
        self.level_grid = levelgrid
        self.block_count = 7
        self.center_x = 0
        self.center_y = 1
        self.pitleft_offset = 4
        self.ceilright_offset = 3
        self.start_offset = -0.5
        self.max_level_size = [88,110]
        self.boundaries = [np.size(optimizer.arr, 1), np.size(optimizer.arr, 0)]
        self.offset_x = self.center_x - math.floor(self.boundaries[0]/2)
        self.offset_y = self.center_y - math.floor(self.boundaries[1]/2)
        self.is_default_values = is_default_values
        
        self.themes = [
            'Stone',
            'Grass',
            'Desert',
            'Arctic',
            'Swamp',
            'Void'
            ]
        self.theme_attributes= theme_attributes
        
        self.background_dict = {
            'Default' : 1,
            'Cloudy' : 2,
            'Sunset' : 3,
            'Forest' : 4,
            'Night' : 5,
            'City' : 6,
            'Farm' : 7,
            'Windmill' : 8,
            'Dance Party' : 14,
            'Plains' : 15,
            'Water' : 16,
        }
        
        self.music_list = [
            'The Farm',
            'Rooftops',
            'Old Mansion',
            'Pyramid',
            'Waterfall',
            'Windmill',
            'Metal Plant',
            'Iceberg',
            'Dance Party',
            'The Pier',
            'Freeplay',
            'Jungle Temple',
            'Volcano',
            'The Mainframe',
            'Crumbling Bridge',
            'Nuclear Plant',
            'The Ballroom',
            'Space',
            'Roller Coaster',
            'Metro',
        ]
        
        self.startgoal_pos = levelgrid.startgoal_pos
        self.goal_rz = levelgrid.goal_rz
        self.special_blocks = levelgrid.special_blocks
        self.special_block_info = { #[blockID,offsetX,offsetY]
            "crate" : [0, 0, 0],
            "barrel" : [6, 0.5, 0.5],
            "scaffold" : [56,0,0],
            "door" : [15,0,0]
        }
        self.dir = os.path.join('C:\\Users', os.getlogin(), 'Appdata','LocalLow', 'Clever Endeavour Games', 'Ultimate Chicken Horse', 'snapshots')
        
        self.Generate_Level()
        
    def Generate_Level(self):
        self.Set_Level_Attributes()
        self.Create_Scene()
        self.Add_Blocks()
        self.Write_To_File()
        
    def Set_Level_Attributes(self):
        self.theme = self.theme_attributes[self.themes.index(self.level_grid.theme)]
        self.colour_dict = self.theme[0]
        
        if self.level_grid.background == 'Random':
            self.background = random.choice(self.theme[1])
        else:
            self.background = self.background_dict[self.level_grid.background]
            
        if self.level_grid.music == 'Random':
            self.music = random.choice([num for num in range(len(self.music_list)) if num != 10])
        else:
            self.music = self.music_list.index(self.level_grid.music)

    def Create_Scene(self):
        print(self.level_grid.theme, self.background)
        self.root.set("levelSceneName", "BlankLevel")
        self.root.set("saveFormatVersion", "1")
        self.root.set("customLevelBackground", f"{self.background}")
        self.root.set("customLevelMusic", f"{self.music}")
        self.root.set("customLevelAmbience", f"{self.music}")

        DeathPit = ET.SubElement(self.root, "moved")
        
        DeathPit.set("placeableID", "7")
        DeathPit.set("path", "DeathPit")
        DeathPit.set("pY", f"{self.offset_y-self.pitleft_offset}")
        
        
        LeftWall = ET.SubElement(self.root, "moved")
        
        LeftWall.set("placeableID", "9")
        LeftWall.set("path", "LeftWall")
        LeftWall.set("pX", f"{self.offset_x-self.pitleft_offset}")
        LeftWall.set("rZ", "270")


        Ceiling = ET.SubElement(self.root, "moved")
        

        Ceiling.set("placeableID", "8")
        Ceiling.set("path", "Ceiling")
        Ceiling.set("pY", f"{self.offset_y+self.boundaries[1]+self.ceilright_offset}")
        Ceiling.set("rZ", "180")
        
        
        RightWall = ET.SubElement(self.root, "moved")
        
        RightWall.set("placeableID", "6")
        RightWall.set("path", "RightWall")
        RightWall.set("pX", f"{self.offset_x+self.boundaries[0]+self.ceilright_offset}")
        RightWall.set("rZ", "90")
        
        
        StartPlank = ET.SubElement(self.root, "moved")
        
        StartPlank.set("placeableID", "11")
        StartPlank.set("path", "StartPlank")
        StartPlank.set("pX", f"{self.offset_x+self.startgoal_pos[0][1]+self.start_offset}")
        StartPlank.set("pY", f"{self.offset_y+self.startgoal_pos[0][0]}")
        
        
        GoalBlock = ET.SubElement(self.root, "block")
        
        GoalBlock.set("sceneID", "6")
        GoalBlock.set("placeableID", "2")
        GoalBlock.set("blockID", "39")
        GoalBlock.set("pX", f"{self.offset_x+self.startgoal_pos[1][1]}")
        GoalBlock.set("pY", f"{self.offset_y+self.startgoal_pos[1][0]}")
        GoalBlock.set("rZ", f"{self.goal_rz}")
        
    def Create_Block(self,x_pos,y_pos,blockID,block_offset_x, block_offset_y,rotation,colour,xscale=1):
        block = ET.SubElement(self.root, "block")
        
        pos_x = x_pos+self.offset_x+block_offset_x
        pos_y = y_pos+self.offset_y+block_offset_y
        
        block.set("sceneID", f"{self.block_count}")
        block.set("blockID",f"{blockID}")
        block.set("pX",f"{pos_x}")
        block.set("pY",f"{pos_y}")
        block.set("rZ",f"{rotation}")
        block.set("sX",f"{xscale}")
        block.set("colR",f"{self.colour_dict[colour][0]}")
        block.set("colG",f"{self.colour_dict[colour][1]}")
        block.set("colB",f"{self.colour_dict[colour][2]}")
        
        self.block_count += 1
        
    def Add_Blocks(self):
        for block in self.block_list:
            self.Create_Block(block[0], block[1],block[2],block[3],block[4],block[5],block[6])
        for sblock in self.special_blocks:
            info = self.special_block_info[sblock[0]]
            xscale = 1
            if len(sblock) == 6:
                xscale = -1
            self.Create_Block(sblock[1], sblock[2], info[0], info[1], info[2], sblock[3], sblock[4], xscale)
            
    def Get_Next_Filename(self):
        try: 
            with open('count.txt', 'r') as f:
                count = int(f.read().strip())
        except FileNotFoundError:
            current_count = 0
            for file in os.listdir(self.dir):
                if('GeneratedLevel.') in file and file[-14:-12].isdigit(): #-14 -11 is the location of the numerical code
                    print(file[-14:-11])
                    file_count = int(file[-14:-11])
                    print(file_count)
                    if file_count > current_count:
                        current_count = file_count
            count = current_count + 1
        
        if self.is_default_values:
            filename = f'GeneratedLevel.{count:03}.c.snapshot'   
        else:
            filename = f'GeneratedLevelND.{count:03}.c.snapshot' 
        count+=1
        
        with open('count.txt', 'w') as f:
            f.write(str(count))
        
        return filename
                
    def Write_To_File(self):
        xml_string = ET.tostring(self.root)
        filename = self.Get_Next_Filename()
        
        print(os.path.join(self.dir, filename))
        
        with lzma.open(os.path.join(self.dir, filename), "wb", format=lzma.FORMAT_ALONE) as output_file:
            output_file.write(xml_string)