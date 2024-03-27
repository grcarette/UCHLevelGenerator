import threading
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askinteger

from LevelGrid import LevelGrid
from SnapshotCreator import SnapshotCreator
from AutoOptimizer import AutoOptimizer
from ArrayPlotter import ArrayPlotter
import numpy as np
import matplotlib.pyplot as plt

class UCHLevelGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UCH Level Generator")
        self.resizable(False, False)
        self.pixel_size = 4
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
        self.display_info = tk.StringVar()
        self.map_size = tk.StringVar()
        self.map_theme = tk.StringVar()
        self.path_thickness = tk.StringVar()
        self.asset_frequency = tk.StringVar()
        self.music = tk.StringVar()
        self.background = tk.StringVar()
        self.curve_intensity = 3
        self.smooth_scale = 3
        self.array_plotter = ArrayPlotter()  
        self.Create_Widgets()
        
    def Create_Widgets(self):
        widget_frame = tk.Frame(self, width=223, height=356)
        widget_frame.grid(row=0, column=1, sticky='nesw')
        widget_frame.grid_propagate(False)
        widget_frame.grid_anchor('nw')
        
        canvas_frame = tk.Frame(self, width=460, height=356)
        canvas_frame.grid(row=0, column=0, sticky='nesw')
        canvas_frame.rowconfigure(0, minsize = self.level_height)
        canvas_frame.columnconfigure(0, minsize = self.level_width)
        
        level_canvas = LevelCanvas(
            canvas_frame,
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
        map_theme_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.map_theme)
        map_theme_dropdown['values'] = (
            'Random',
            'Stone',
            'Grass',
            'Desert',
            'Arctic',
            'Swamp',
            'Void'
        )
        self.map_theme.set('Stone')
        map_theme_dropdown.grid(row=2, column=1, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        advanced_label = tk.Label(widget_frame, text="Advanced", font=("Arial", 12))
        advanced_label.grid(row=3, column=0, padx=self.text_padx, pady=(10,0), sticky='w')
        
        path_thickness_label = tk.Label(widget_frame, text="Path Thickness")
        path_thickness_label.grid(row=4, column=0, padx=self.text_padx, pady=self.text_pady, sticky='w')
        path_thickness_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.path_thickness)
        path_thickness_dropdown['values'] = (
            'Thin',
            'Regular',
            'Thick',
        )
        self.path_thickness.set('Regular')
        path_thickness_dropdown.grid(row=5, column=0, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        music_dropdown_label = tk.Label(widget_frame, text="Music")
        music_dropdown_label.grid(row=4, column=1, padx=self.text_padx, pady=self.text_pady, sticky='w')
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
        music_dropdown.grid(row=5, column=1, padx=self.dd_padx, pady=self.dd_pady,sticky='w')
        
        asset_frequency_label =tk.Label(widget_frame, text="Asset Frequency")
        asset_frequency_label.grid(row=6, column=0, padx=self.text_padx, pady=self.text_pady, sticky='w')
        asset_frequency_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.asset_frequency)
        asset_frequency_dropdown['values'] = (
            'None',
            'Low',
            'Medium',
            'High',
        )
        self.asset_frequency.set('Medium')
        asset_frequency_dropdown.grid(row=7, column=0, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        background_label = tk.Label(widget_frame, text='Background')
        background_label.grid(row=6, column=1, padx=self.text_padx, pady=self.text_pady, sticky='w')
        background_dropdown = ttk.Combobox(widget_frame, width=self.dd_width, textvariable=self.background)
        background_dropdown['values'] = (
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
        background_dropdown.grid(row=7, column=1, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        curve_intensity_label = tk.Label(widget_frame, text='Curve Intensity')
        curve_intensity_label.grid(row=8, column=0, padx=self.text_padx, pady=self.text_pady, sticky='w')
        curve_intensity_scale = ttk.Scale(widget_frame, from_=1, to=5, orient='horizontal', command=self.Change_Curve_Scale) 
        curve_intensity_scale.grid(row=9, column=0, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        smooth_scale_label = tk.Label(widget_frame, text='Smoothness')
        smooth_scale_label.grid(row=8, column=1, padx=self.text_padx, pady=self.text_pady, sticky='w')
        smooth_scale = ttk.Scale(widget_frame, from_=1, to=5, orient='horizontal', command=self.Change_Smooth_Scale)
        smooth_scale.grid(row=9, column=1, padx=self.dd_padx, pady=self.dd_pady, sticky='w')
        
        self.generate_multiple_button = ttk.Button(
            widget_frame,
            text="Generate Multiple", 
            width = 34,
            command=lambda: self.Generate_Multiple_Async(level_canvas),
            state= tk.NORMAL
        )
        self.generate_multiple_button.grid(row=10, column=0, columnspan=2, padx=self.dd_padx, pady=self.text_pady, sticky='se')
        
        self.generate_button = ttk.Button(
            widget_frame,
            text="Generate Level", 
            width = 34,
            command=lambda: self.Generate_Level_Async(level_canvas),
            state= tk.NORMAL
        )
        self.generate_button.grid(row=11, column=0, columnspan=2, padx=self.dd_padx, pady=self.text_pady, sticky='se')
        
    def Change_Curve_Scale(self, value):
        self.curve_intensity = value

    def Change_Smooth_Scale(self, value):
        self.smooth_scale = value
        
    def Update_Level_Canvas(self, level_canvas):
        if isinstance(self.level_array, np.ndarray):
            level_canvas.Display_Level(self.level_array)
            self.level_array = False
            return
        self.after(500, lambda: self.Update_Level_Canvas(level_canvas))
        
    def Get_Level_Args(self):
        map_size = self.map_size.get() 
        map_theme = self.map_theme.get()
        path_thickness = self.path_thickness.get()
        music = self.music.get()
        asset_frequency = self.asset_frequency.get()
        background = self.background.get()
        curve_intensity = self.curve_intensity
        smooth_scale = self.smooth_scale
        return [map_size, map_theme, path_thickness, music, asset_frequency, background, curve_intensity, smooth_scale]
        
    def Generate_Multiple_Async(self, level_canvas):
        num_level = askinteger("Enter Number", "How many levels would you like to generate?")
        self.generate_button.config(state=tk.DISABLED)
        self.generate_multiple_button.config(state=tk.DISABLED, text="Generating...")
        level_args = self.Get_Level_Args()
        thread = threading.Thread(target=self.Generate_Multiple, args=(num_level, [level_args]))
        thread.start()
        self.Update_Level_Canvas(level_canvas)
        
    def Generate_Multiple(self, num_level, level_args):
        for i in range(num_level):
            self.Generate_Level(level_args)
        self.generate_multiple_button.config(state=tk.NORMAL, text="Generate Multiple")
        self.generate_button.config(state=tk.NORMAL)
        finished_message = tk.Toplevel(self)
        finished_message.geometry("300x30")
        finished_message.title("Generation Completed")
        tk.Label(finished_message, text= f"Finished generating {num_level} levels.", font=('Arial', 16)).pack()
        
    def Generate_Level_Async(self, level_canvas):
        self.generate_button.config(state=tk.DISABLED, text="Generating...")
        level_args = self.Get_Level_Args()
        print(level_args)
        thread = threading.Thread(target=self.Generate_Level, args=([level_args]))
        thread.start()
        self.Update_Level_Canvas(level_canvas)
        
    def Generate_Level(self, level_args):
        level_grid = LevelGrid(self.array_plotter, level_args)
        self.level_array = np.copy(level_grid.array)
        optimizer = AutoOptimizer(level_grid.array)
        new_level = SnapshotCreator(level_grid, optimizer)
        self.generate_button.config(state="normal", text="Generate Level")

class LevelCanvas(tk.Canvas):
    def __init__(self, parent, width, height, pixel_size, **kwargs):
        super().__init__(parent, width=width*pixel_size, height=height*pixel_size, **kwargs)
        self.colour_dict = {
            10 : '#a1dce6',  # girder
            5 : '#2e2314',   # dark brown
            4 : '#b5b5b5',   # gray
            3 : '#969696',   # dark gray
            2 : '#636363',   # darker gray
            1 : '#4f4f4f',   # darkest gray
            0 : '#77dded'    # blue
        }
        self.pixel_size = pixel_size
        self.width = width + 1
        self.height = height + 1
        self.pixels = np.ones((self.height, self.width))
        self.Draw_Pixels()
        
    def Draw_Pixels(self):
        for row in range(self.height):
            for col in range(self.width):
                colour = self.colour_dict[self.pixels[row,col]]
                self.create_rectangle(
                    col * self.pixel_size, row * self.pixel_size, 
                    (col + 1) * self.pixel_size, (row + 1) * self.pixel_size,
                    fill=colour, outline=colour
                )
        
    def Display_Level(self, level_array):
        grid = level_array[1:-2,1:-2]
        self.pixels = np.ones((self.height, self.width))
        for row in range(np.shape(grid)[0]):
            for col in range(np.shape(grid)[1]):
                self.pixels[self.height - row - 2,col] = grid[row,col]
        self.Draw_Pixels()
                
if __name__ == "__main__":
    LevelGenerator = UCHLevelGenerator()
    LevelGenerator.mainloop()

