import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import random

from LevelGrid import LevelGrid
from SnapshotCreator import SnapshotCreator
from AutoOptimizer import AutoOptimizer
import numpy as np

class UCHLevelGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UCH Level Generator")
        self.resizable(False, False)
        self.pixel_size = 3.65
        self.level_width = 110 * self.pixel_size
        self.level_height = 88 * self.pixel_size
        self.text_padx = 0
        self.dd_padx = 3
        self.text_pady = 0
        self.dd_width = 12
        self.dd_pady = (0, 6)
        self.bg_colour = '#8a8a8a'
        self.slider_colour = '#4a4a4a'
        self.level_array = False
        self.map_size = tk.StringVar()
        self.map_theme = tk.StringVar()
        self.path_thickness = tk.StringVar()
        self.asset_frequency = tk.StringVar()
        self.music = tk.StringVar()
        self.background = tk.StringVar()
        self.num_level = tk.StringVar()
        self.curve_intensity = 3
        self.smoothness = 3
        
        self.themes = [
            'Stone',
            'Grass',
            'Desert',
            'Arctic',
            'Swamp',
            'Void'
            ]
        self.theme_attributes=[                
            [{ #stone
                5 : ["0.1911765", "0.1084139", "0.07590831"],
                4 : ["0.3308824", "0.3308824", "0.3308824"],
                3 : ["0.253", "0.253", "0.253"],
                2 : ["0.2039216","0.2039216","0.2039216"],
                1 : ["0.1764706","0.1764706","0.1764706"]
            }, [1,2,3,6,7,15]],
            [{ #grass
                5 : ["0.1911765", "0.1084139", "0.07590831"],
                4 : ["0.3414807","0.3823529","0.295199"],
                3 : ["0.2647566", "0.3382353", "0.181552"],
                2 : ["0.2647059", "0.1474943", "0.1206748"],
                1 : ["0.1911765", "0.1084139", "0.07590831"]
            }, [1,2,3,4,5,6,7,8,15]],
            [{ #desert
                5 : ["0.1911765", "0.1084139", "0.07590831"],
                4 : ["0.4679692", "0.4852941", "0.1712803"],
                3 : ["0.5147059", "0.3879217", "0.04163063"],
                2 : ["0.4117647","0.1987249","0.1150519"],
                1 : ["0.3676471","0.1139868","0.05136246"]
            }, [1,2,3,4,7,8,15]],
            [{ #arctic
                5 : ["0.1911765", "0.1084139", "0.07590831"],
                4 : ["0.2058823" ,"0.3904664" ,"0.5"],
                3 : ["0.447" ,"0.447" ,"0.447"],
                2 : ["0.2083694" ,"0.291612" ,"0.6911765"],
                1 : ["0.1314879" ,"0.1899535" ,"0.4705882"]
            }, [1,2,3,4,5,6,16]],
           [{ #swamp
                5 : ["0.1911765", "0.1084139", "0.07590831"],
                4 : ["0.2647566" , "0.3382353" , "0.1815528"],
                3 : ["0.2484533" , "0.25" , "0.1378676"],
                2 : ["0.1323529" , "0.1258427" , "0.03795415"],
                1 : ["0.1102941" , "0.1051038" , "0.06325691"]
            }, [1,2,4,7,8,15]],
            [{ #void
                5 : ["0.122", "0.122", "0.122"],
                4 : ["0.4485294" , "0.313311", "0.4447993"],
                3 : ["0.3382353" , "0.1964749", "0.3167268"],
                2 : ["0.1764706" , "0.09083045", "0.1634769"],
                1 : ["0.053", "0.053", "0.053"]
            }, [1,6]]]
        
        self.default_values = [
            'Large',
            'Random',
            'Random',
            'Random',
            'Medium',
            'Medium',
            '3.0',
            '3.0',
        ]
        
        self.Create_Widgets()
        
    def Create_Widgets(self):
        widget_frame = tk.Frame(self, width=223, height=260)
        widget_frame.grid(row=0, column=1, sticky='nesw')
        widget_frame.grid_propagate(False)
        widget_frame.grid_anchor('nw')

        canvas_frame = tk.Frame(self, width=460, height=356)
        canvas_frame.grid(row=0, column=0, sticky='nesw')
        canvas_frame.rowconfigure(0, minsize = self.level_height)
        canvas_frame.columnconfigure(0, minsize = self.level_width)
        
        level_canvas = LevelCanvas(
            canvas_frame,
            level_generator_instance=self,
            width=110,
            height=88,
            pixel_size=self.pixel_size,
        )
        level_canvas.grid(row=0, column=0)
        
        map_settings_label = tk.Label(widget_frame, text="Map Settings", font=("Arial", 16))
        map_settings_label.grid(row=0, column=0, columnspan=3, padx=self.text_padx, pady=self.text_pady, sticky='w')
        
        map_size_label = tk.Label(widget_frame, text="Map Size")
        map_size_label.grid(row=1, column=0, padx=self.text_padx, pady=self.text_pady, sticky='w')
        map_size_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.map_size)
        map_size_dropdown['values'] = (
            'Small',
            'Medium',
            'Large'
        )
        self.map_size.set('Large')
        map_size_dropdown.grid(row=2, column=0, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        map_theme_label = tk.Label(widget_frame, text="Map Theme")
        map_theme_label.grid(row=1, column=1, padx=self.text_padx, pady=self.text_pady, sticky='w')
        self.map_theme_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.map_theme)
        self.map_theme_dropdown['values'] = (
            'Random',
            'Stone',
            'Grass',
            'Desert',
            'Arctic',
            'Swamp',
            'Void'
        )
        self.map_theme.set('Random')
        self.map_theme_dropdown.grid(row=2, column=1, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        music_dropdown_label = tk.Label(widget_frame, text="Music")
        music_dropdown_label.grid(row=3, column=0, padx=self.text_padx, pady=self.text_pady, sticky='w')
        music_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.music)
        music_dropdown['values'] = (
            'Random',
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
            'Jungle Temple',
            'Volcano',
            'The Mainframe',
            'Crumbling Bridge',
            'Nuclear Plant',
            'The Ballroom',
            'Space',
            'Roller Coaster',
            'Metro',
        )
        self.music.set('Random')
        music_dropdown.grid(row=4, column=0, padx=self.dd_padx, pady=self.dd_pady,sticky='w')

        background_label = tk.Label(widget_frame, text='Background')
        background_label.grid(row=3, column=1, padx=self.text_padx, pady=self.text_pady, sticky='w')
        self.background_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.background)
        self.background_dropdown['values'] = (
            'Random',
            'Default',
            'Cloudy',
            'Sunset',
            'Forest',
            'Night',
            'City',
            'Farm',
            'Windmill',
            'Dance Party',
            'Plains',
            'Water',
        )
        self.background.set('Random')
        self.background_dropdown.grid(row=4, column=1, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        advanced_label = tk.Label(widget_frame, text="Advanced", font=("Arial", 12))
        advanced_label.grid(row=5, column=0, padx=self.text_padx, pady=(10,0), sticky='w')
        
        path_thickness_label = tk.Label(widget_frame, text="Path Thickness")
        path_thickness_label.grid(row=6, column=0, padx=self.text_padx, pady=self.text_pady, sticky='w')
        path_thickness_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.path_thickness)
        path_thickness_dropdown['values'] = (
            'Thin',
            'Medium',
            'Thick',
        )
        self.path_thickness.set('Medium')
        path_thickness_dropdown.grid(row=7, column=0, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        asset_frequency_label =tk.Label(widget_frame, text="Asset Frequency")
        asset_frequency_label.grid(row=6, column=1, padx=self.text_padx, pady=self.text_pady, sticky='w')
        asset_frequency_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.asset_frequency)
        asset_frequency_dropdown['values'] = (
            'None',
            'Low',
            'Medium',
            'High',
        )
        self.asset_frequency.set('Medium')
        asset_frequency_dropdown.grid(row=7, column=1, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        curve_intensity_label = tk.Label(widget_frame, text='Curve Intensity')
        curve_intensity_label.grid(row=8, column=0, padx=self.text_padx, pady=self.text_pady, sticky='w')
        self.curve_intensity_scale = ttk.Scale(widget_frame, from_=1, to=5, orient='horizontal', command=self.Change_Curve_Scale) 
        self.curve_intensity_scale.grid(row=9, column=0, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        self.curve_intensity_scale.set(3)
        
        smooth_scale_label = tk.Label(widget_frame, text='Smoothness')
        smooth_scale_label.grid(row=8, column=1, padx=self.text_padx, pady=self.text_pady, sticky='w')
        self.smooth_scale = ttk.Scale(widget_frame, from_=1, to=5, orient='horizontal', command=self.Change_Smooth_Scale)
        self.smooth_scale.grid(row=9, column=1, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        self.smooth_scale.set(3)
        
        reset_to_default_button = ttk.Button(
            widget_frame,
            text="Reset to Defaults",
            width=34,
            command=lambda: self.Reset_To_Defaults(widget_frame)
        )
        reset_to_default_button.grid(row=10, column=0, columnspan=2, padx=self.dd_padx, pady=(8,0), sticky='w')
        
        generate_entry = tk.Entry(widget_frame, bg='white', justify='center', textvariable=self.num_level, width=5)
        self.num_level.set('1')
        generate_entry.grid(row=11, column=0, padx=self.dd_padx+1, pady=self.text_pady+1, sticky='w')
        
        self.generate_button = ttk.Button(
            widget_frame,
            text="Generate Level(s)", 
            width = 28,
            command=lambda: self.Generate_Level_Async(level_canvas),
            state= tk.NORMAL
        )
        self.generate_button.grid(row=11, column=0, columnspan=2, padx=self.dd_padx, pady=self.text_pady, sticky='e')
        
        self.Create_Placeholder_Image(level_canvas)
        
    def Reset_To_Defaults(self, widget_frame):     
        self.map_size.set(self.default_values[0])
        self.map_theme.set(self.default_values[1])
        self.music.set(self.default_values[2])
        self.background.set(self.default_values[3])
        self.path_thickness.set(self.default_values[4])
        self.asset_frequency.set(self.default_values[5])
        self.smooth_scale.set(int(float(self.default_values[6])))
        self.curve_intensity_scale.set(int(float(self.default_values[7])))
        self.num_level.set('1')

    def Change_Curve_Scale(self, value):
        self.curve_intensity = value

    def Change_Smooth_Scale(self, value):
        self.smoothness = value
        
    def Update_Level_Canvas(self, level_canvas, theme, background):
        if isinstance(self.level_array, np.ndarray):
            level_canvas.Display_Level(self.level_array, theme, background)
            self.level_array = False
            return
        self.after(500, lambda: self.Update_Level_Canvas(level_canvas, theme, background))
        
    def Create_Placeholder_Image(self, level_canvas):
        try:
            tmp_level_args = self.Get_Level_Args()
            tmp_level_grid = LevelGrid(tmp_level_args)
            self.level_array = np.copy(tmp_level_grid.array)
            self.Update_Level_Canvas(level_canvas, tmp_level_args[1], tmp_level_args[3])
        except:
            pass

    def Get_Level_Args(self):
        map_size = self.map_size.get() 
        map_theme = self.map_theme.get()
        music = self.music.get()
        background = self.background.get()
        path_thickness = self.path_thickness.get()
        asset_frequency = self.asset_frequency.get()
        curve_intensity = self.curve_intensity
        smooth_scale = self.smoothness
        return [map_size, map_theme, music, background, path_thickness, asset_frequency, curve_intensity, smooth_scale]
    
    def Pick_Random(self, theme, background):
        if theme == 'Random':
            theme = random.choice(self.map_theme_dropdown['values'][1:])
        if background == 'Random':
            background = random.choice(self.background_dropdown['values'][1:])
            
        return theme, background
    
    def Check_If_Default(self, level_args):
        print(level_args)
        for i in range(len(level_args)):
            print(i)
            print(level_args[i], self.default_values[i])
            if level_args[i] != self.default_values[i] and i not in [1, 2]:
                return False
        return True

    def Generate_Level_Async(self, level_canvas):
        self.generate_button.config(state=tk.DISABLED, text="Generating...")
        level_args = self.Get_Level_Args()
        is_default_values = self.Check_If_Default(level_args)
        level_args[1], level_args[3] = self.Pick_Random(level_args[1], level_args[3])
        num_level = self.num_level.get()
        if num_level.isdigit() and 1 <= int(num_level) <= 100:
            num_level = int(num_level) - 1
            thread = threading.Thread(target=self.Generate_Level, args=(level_args, is_default_values, 1))
            thread.start()
            self.Update_Level_Canvas(level_canvas, level_args[1], level_args[3])
            if num_level >= 1:
                thread = threading.Thread(target=self.Generate_Level, args=(level_args, is_default_values, num_level))
                thread.start()
        else:
            tk.messagebox.showerror('Error','Please enter number from 1-100')
            self.generate_button.config(state="normal", text="Generate Level(s)")
            
    def Generate_Level(self, level_args, is_default_values, num_level):
        for i in range(num_level):
            try:
                level_grid = LevelGrid(level_args)
                self.level_array = np.copy(level_grid.array)
                optimizer = AutoOptimizer(level_grid.array)
                SnapshotCreator(level_grid, optimizer, self.theme_attributes, is_default_values)
            except Exception as e: 
                tk.messagebox.showerror('Error','Map generation failed. Please try again.')
                print(e)
        self.generate_button.config(state="normal", text="Generate Level(s)")

class LevelCanvas(tk.Canvas):
    def __init__(self, parent, level_generator_instance, width, height, pixel_size, **kwargs):
        super().__init__(parent, width=width*pixel_size, height=height*pixel_size, **kwargs)
        self.level_generator = level_generator_instance
        self.colour_dict = {
            10 : '#a1dce6',  # girder
            5 : '#2e2314',   # dark brown
            4 : '#b5b5b5',   # gray
            3 : '#969696',   # dark gray
            2 : '#636363',   # darker gray
            1 : '#4f4f4f',   # darkest gray
            0 : '#77dded'    # blue
        }
        self.bg_colour_dict = {
            'Random':'#77dded',
            'Default':'#77dded',
            'Cloudy':'#77dded',
            'Sunset':'#f5da56',
            'Forest':'#77dded',
            'Night':'#262626',
            'City':'#cfb8de',
            'Farm':'#e3e2cc',
            'Windmill':'#e3e2cc',
            'Dance Party':'#262626',
            'Plains':'#cee3cc',
            'Water':'#77dded',
        }
        self.pixel_size = pixel_size
        self.width = width + 1
        self.height = height + 1
        self.pixels = np.ones((self.height, self.width))
        self.Draw_Pixels()
        
    def Rgb_To_Hex(self, rgb, theme):
        brightness_coeff = 1.8
        if theme == 'Arctic':
            brightness_coeff = 1.4
        hex_colour = '#{:02x}{:02x}{:02x}'.format(int(float(rgb[0])*255*brightness_coeff), int(float(rgb[1])*255*brightness_coeff), int(float(rgb[2])*255*brightness_coeff))
        return hex_colour
    
    def Set_Colours(self, theme, background):
        if theme == 'Random':
            theme = 'Stone'
        theme_colours = self.level_generator.theme_attributes[self.level_generator.themes.index(theme)]
        for colour in theme_colours[0]:
            hex_colour = self.Rgb_To_Hex(theme_colours[0][colour], theme)
            self.colour_dict[colour] = hex_colour
        self.colour_dict[0] = self.bg_colour_dict[background]
        
    def Draw_Pixels(self):
        for row in range(self.height):
            for col in range(self.width):
                colour = self.colour_dict[self.pixels[row,col]]
                self.create_rectangle(
                    col * self.pixel_size, row * self.pixel_size, 
                    (col + 1) * self.pixel_size, (row + 1) * self.pixel_size,
                    fill=colour, outline=colour
                )
        
    def Display_Level(self, level_array, theme, background):
        self.Set_Colours(theme, background)
        grid = level_array[1:-2,1:-2]
        self.pixels = np.ones((self.height, self.width))
        for row in range(np.shape(grid)[0]):
            for col in range(np.shape(grid)[1]):
                self.pixels[self.height - row - 2,col] = grid[row,col]
        self.Draw_Pixels()
                
if __name__ == "__main__":
    a = {
        'a' : 1,
        'b' : 2,
        'c' : 3
    }
    for d in a:
        print(a[d])

