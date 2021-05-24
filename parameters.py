import numpy as np
import xml.etree.ElementTree as ET

from PIL import ImageTk,Image

#This all are immuatble objects, so I made wrapper class for them to modify them outside this file
TILE_SIZE = 64

WIDTH = 10
HEIGHT = 4

#Constants
SPAWN_ID = 200

XML_PATH = "./tiles/test.xml"
TILES_PATH = "./tiles/texture.png"

LAYER = {
    "Skybox" : 0,
    "Background" : 1,
    "Level" : 2,
    "Foreground" : 3
}

#TODO I have to use this because of ASCII
SHIFT = 33
#MAP = np.zeros(4 * HEIGHT * WIDTH, dtype = np.uint8)

class map:
    """wrapper class to store map data"""
    def __init__(self, WIDTH, HEIGHT, TILE_SIZE):
        self.TILE_SIZE = TILE_SIZE

        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH

        self.MAP = np.zeros(4 * self.HEIGHT * self.WIDTH, dtype=np.uint8)

        self.file_path = None

    def reset(self):
        """deleting spawn tile"""
        id = np.where(self.MAP == SPAWN_ID)
        self.MAP[id] = 0

class tiles:
    """wrapper class to store pics of images and their id"""
    def __init__(self,table_file,pic_file,c_size):

        pic_table = ET.parse(table_file)
        data = pic_table.getroot()

        size = data.attrib["tile_size"]
        size = int(size)
        #dictionary with all categories
        self.categories = dict()
        #dictionary with IDs as keys and names as values
        self.ID = dict()

        for category in data:
            #dictionary with all tiles and their id
            tiles = dict()

            for tile in category:

                for block in tile:
                    if block.tag == "name":
                        name = block.text
                    if block.tag == "id":
                        id = int(block.text)
                    if block.tag == "x":
                        x = int(block.text)
                    if block.tag == "y":
                        y = int(block.text)

                # open image
                img = Image.open(pic_file).convert("RGBA")
                # crop and resize image
                x1 = size * x
                y1 = size * y
                x2 = x1 + size
                y2 = y1 + size

                img2 = img.crop((x1, y1, x2, y2))
                img2 = img2.resize((c_size, c_size))
                # Saving id and image in dictionary
                tiles[name] = {"id" : id,
                               "pil" : img2}
                                #"tile"
                                #"pil_res"
                #Saving name with category under ID
                self.ID[id] = (category.attrib["name"], name)
            #saving dictionry with pics and ids to main dictionary
            self.categories[category.attrib["name"]] = tiles

    def convert2Tk(self):
        """Converting all tile pics to format PhotoImage for using in Tkinter canvas"""
        for category in self.categories:
            for tile in self.categories[category]:
                self.categories[category][tile]["tile"] = ImageTk.PhotoImage(self.categories[category][tile]["pil"])

    def resize(self,size):
        """resizing pictures, quite slow btw"""
        for category in self.categories:
            for tile in self.categories[category]:
                #resizing PIL image
                self.categories[category][tile]["pil_res"] = self.categories[category][tile]["pil"].resize((size,size))
                #converting PIL image to Tkinter format
                self.categories[category][tile]["tile"] = ImageTk.PhotoImage(self.categories[category][tile]["pil_res"])


MAP = map(WIDTH, HEIGHT,TILE_SIZE)
TILES = tiles(XML_PATH,TILES_PATH,TILE_SIZE)


