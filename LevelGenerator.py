import xml.etree.ElementTree as ET
import random
import numpy as np
import math
import lzma
import os

class LevelGenerator:
    def __init__(self, boundaries, startgoal_pos):
        self.root = ET.Element("scene")
        self.block_count = 7
        self.center_x = 0
        self.center_y = 1
        self.pitleft_offset = 4
        self.ceilright_offset = 3
        self.tmp_offset = 9
        self.boundaries = boundaries
        self.offset_x = self.center_x - math.floor(self.boundaries[0]/2)
        self.offset_y = self.center_y - math.floor(self.boundaries[1]/2)
        self.startgoal_pos = startgoal_pos
        self.colour_dict = {
            4 : ["0.3308824", "0.3308824", "0.3308824"],
            3 : ["0.253", "0.253", "0.253"],
            2 : ["0.2039216","0.2039216","0.2039216"],
            1 : ["0.1764706","0.1764706","0.1764706"]
        }
        self.dir = os.path.join('C:\\Users', os.getlogin(), 'Appdata','LocalLow', 'Clever Endeavour Games', 'Ultimate Chicken Horse', 'snapshots')
        
    def Generate_Level(self, block_list):
        self.Create_Scene()
        self.Add_Blocks(block_list)
        self.Write_To_File()

    def Create_Scene(self):
        music = random.randint(1,20)
        
        self.root.set("levelSceneName", "BlankLevel")
        self.root.set("saveFormatVersion", "1")
        self.root.set("customLevelBackground", "1")
        self.root.set("customLevelMusic", f"{music}")
        self.root.set("customLevelAmbience", f"{music}")
        
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
        StartPlank.set("pX", f"{self.offset_x+self.startgoal_pos[0][1]}")
        StartPlank.set("pY", f"{self.offset_x+self.startgoal_pos[0][0]+self.tmp_offset*2}")
        
        GoalBlock = ET.SubElement(self.root, "block")
        
        GoalBlock.set("sceneID", "6")
        GoalBlock.set("placeableID", "2")
        GoalBlock.set("blockID", "39")
        GoalBlock.set("pX", f"{self.offset_x+self.startgoal_pos[1][1]}")
        GoalBlock.set("pY", f"{self.offset_x+self.startgoal_pos[1][0]+self.tmp_offset*2}")
        
    def Create_Block(self,x_pos,y_pos,blockID,block_offset_x, block_offset_y,rotation,colour):
        block = ET.SubElement(self.root, "block")
        
        pos_x = x_pos+self.offset_x+block_offset_x
        pos_y = y_pos+self.offset_y+block_offset_y
        
        block.set("sceneID", f"{self.block_count}")
        block.set("blockID",f"{blockID}")
        block.set("pX",f"{pos_x}")
        block.set("pY",f"{pos_y}")
        block.set("rZ",f"{rotation}")
        block.set("colR",f"{self.colour_dict[colour][0]}")
        block.set("colG", f"{self.colour_dict[colour][1]}")
        block.set("colB", f"{self.colour_dict[colour][2]}")
        
        self.block_count += 1
        
    def Add_Blocks(self, block_list):
        for block in block_list:
            self.Create_Block(block[0], block[1],block[2],block[3],block[4],block[5],block[6])
            
    def Get_Next_Filename(self):
        try: 
            with open('count.txt', 'r') as f:
                count = int(f.read().strip())
        except FileNotFoundError:
            count = 1
        
        filename = f'GeneratedLevel.{count:03}.c.snapshot'
        
        return filename
                
    def Write_To_File(self):
        xml_string = ET.tostring(self.root)
        filename = self.Get_Next_Filename()
        
        print(os.path.join(self.dir, filename))
        
        with lzma.open(os.path.join(self.dir, filename), "wb", format=lzma.FORMAT_ALONE) as output_file:
            output_file.write(xml_string)