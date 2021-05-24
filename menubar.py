from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import numpy as np

from parameters import *
import map as mp
import __main__

def New():
    def set_map():
        """Setting new map and closing new map window"""

        MAP.WIDTH, MAP.HEIGHT = int(width.get()), int(height.get())

        map_square = MAP.WIDTH * MAP.HEIGHT

        # 4*map_square because we have 4 layers here on our map
        MAP.MAP = np.zeros(4 * map_square, dtype = np.uint8)

        #new file
        MAP.file_path = None

        #Checking should we fill skybox
        if fill_skybox.get() and category.get() != "Category":
            tile = Tiles.get(ACTIVE)
            cat = category.get()

            MAP.MAP[:map_square] = TILES.categories[cat][tile]["id"]

        mp.Update()

        #resizing canvas
        __main__.cv.config(scrollregion=(0, 0, MAP.TILE_SIZE*MAP.WIDTH, MAP.TILE_SIZE*MAP.HEIGHT))

        print(MAP.WIDTH, MAP.HEIGHT)
        print(MAP.MAP)
        new_window.destroy()

    # window
    new_window = Toplevel()
    new_window.title("New Map")
    new_window.geometry("180x300")

    new_window.grab_set()
    # window

    # GUI
    width = Entry(new_window)
    l_width = Label(new_window, text = "Width:")
    height = Entry(new_window)
    l_height = Label(new_window, text = "Height:")


    fill_skybox = IntVar()
    fill = Checkbutton(new_window, text="Fill skybox", variable=fill_skybox)

    def update_list(event):
        """Updating Tiles when changing category"""
        k = list(TILES.categories[category.get()].keys())
        k = StringVar(value=k)

        Tiles.config(listvariable=k)

    cat = list(TILES.categories.keys())

    category = ttk.Combobox(new_window, values = cat, state = "readonly")
    category.bind('<<ComboboxSelected>>', update_list)
    category.set("Category")
    category.grid(column=0)

    Tiles = Listbox(new_window, selectmode=SINGLE)
    Tiles.grid(column=0)

    button = Button(new_window, text = "Create",
                    command = set_map)
    # GUI

    #Placing GUI
    l_width.grid(row=0, column=0)
    width.grid(row = 0, column = 1)

    l_height.grid(row=1, column=0)
    height.grid(row = 1, column = 1)

    fill.grid(row = 2, column = 0, columnspan = 2)
    category.grid(row = 3, column = 0, columnspan = 2)
    Tiles.grid(row = 4, column = 0, columnspan = 2)

    button.grid(row = 5, column = 0, columnspan = 2)
    # Placing GUI



def Open():
    """Handles opening .map files"""
    f = filedialog.askopenfile(initialdir = ".", initialfile = "New map" ,
                                 title = "Select file",
                                 filetypes = (("map files","*.map"),("all files","*.*")),
                                 mode = "r", defaultextension = "*.map")

    MAP.file_path = f.name

    lines = f.read().splitlines()

    MAP.WIDTH = int(lines[0])
    MAP.HEIGHT = int(lines[1])

    map_square = MAP.WIDTH * MAP.HEIGHT
    # 4*map_square because we have 4 layers here on our map
    MAP.MAP = np.zeros(4 * map_square, dtype=np.uint8)

    #4 is number of layers
    #L stands for Layer
    for L in range(2,6):

        for i in range(MAP.WIDTH * MAP.HEIGHT):
            #TODO
            MAP.MAP[i + (L - 2) * MAP.WIDTH * MAP.HEIGHT] = ord(lines[L][i])-SHIFT

    #updating canvas
    mp.Update()

    print(MAP.WIDTH, MAP.HEIGHT)
    print(MAP.MAP)

    f.close()

def Save():
    """Saves MAP to file"""
    if MAP.file_path is None:
        Save_as()
        return

    f = open(MAP.file_path, mode = "w+")

    f.write(str(MAP.WIDTH) + "\n")
    f.write(str(MAP.HEIGHT) + "\n")

    for i in range(4 * MAP.WIDTH * MAP.HEIGHT):

        if i % (MAP.HEIGHT * MAP.WIDTH) == 0 and i != 0:
            f.write("\n")
    #TODO ASCII starts from ~32 symbol
        f.write(chr(MAP.MAP[i]+SHIFT))

    f.close()


def Save_as():
    """Saves MAP to file"""
    f = filedialog.asksaveasfile(initialdir = ".", initialfile = "New map" ,
                                 title = "Select directory",
                                 filetypes = (("map files","*.map"),("all files","*.*")),
                                 mode = "w", defaultextension = "*.map")

    if f is None:
        return

    MAP.file_path = f.name

    f.close()

    Save()