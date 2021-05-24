from parameters import *
from tkinter import *

import __main__

def Update(clear = True):
    """Update Canvas with map"""
    if clear:
        print("nan")
        __main__.cv.delete("all")

    for i in range(4 * MAP.WIDTH * MAP.HEIGHT):
        if MAP.MAP[i] != 0:

            w = i % (MAP.HEIGHT * MAP.WIDTH) #array of layer

            m = w % MAP.WIDTH  #x coords
            d = w // MAP.WIDTH #y coords
            print("hi, i am tile", i, "with cords", m, d)

            x1 = m * MAP.TILE_SIZE
            y1 = d * MAP.TILE_SIZE

            print("It is me",MAP.MAP[i] )

            image = TILES.ID[MAP.MAP[i]]#return tuple (category_name, name)
            tile = TILES.categories[image[0]][image[1]]["tile"]

            __main__.cv.create_image(x1, y1, anchor=NW, image=tile)

    #drawing grid on canvas
    if __main__.Display_Grid.get():
        print(__main__.Display_Grid.get())
        #vertical lines
        for i in range(MAP.WIDTH + 1):

            x1 = i * MAP.TILE_SIZE
            y1 = 0
            y2 = MAP.TILE_SIZE * MAP.HEIGHT

            __main__.cv.create_line(x1, y1, x1, y2)

        #horizontal lines
        for i in range(MAP.HEIGHT + 1):

            y1 = i * MAP.TILE_SIZE
            x1 = 0
            x2 = MAP.TILE_SIZE * MAP.WIDTH

            __main__.cv.create_line(x1, y1, x2, y1)


def paint(event, tile_id = 1, layer = 1):
    """Drawing by updating map array"""
    #is lisbox selected?
    if __main__.lb_Tiles.get(ACTIVE) != "":
        tile = __main__.lb_Tiles.get(ACTIVE)
        category = __main__.category.get()

        if tile_id != 0:
            tile_id = TILES.categories[category][tile]["id"]

        # Spawn can be only in one tile
        if tile_id == SPAWN_ID:
            # deleting spawn tile
            MAP.reset()
    else:
        return

    if __main__.layer.get() != "Layer":
        layer = LAYER[__main__.layer.get()] * MAP.WIDTH * MAP.HEIGHT
        print("read", layer)
    else:
        return
    #handling moving around the canvas with scrollbar
    scroll_h_shift = int(__main__.hbar.get()[0] * MAP.TILE_SIZE * MAP.WIDTH)
    scroll_v_shift = int(__main__.vbar.get()[0] * MAP.TILE_SIZE * MAP.HEIGHT)

    x1, y1 = (event.x + scroll_h_shift), (event.y + scroll_v_shift)

    if x1 >= MAP.TILE_SIZE * MAP.WIDTH or y1 >= MAP.TILE_SIZE * MAP.HEIGHT:
        return


    cords = int(x1 // MAP.TILE_SIZE) + int(y1 // MAP.TILE_SIZE) * MAP.WIDTH
    cords += layer

    MAP.MAP[cords] = tile_id

    print(x1, y1)
    print(MAP.MAP)
    print(MAP.WIDTH, MAP.HEIGHT)

    Update()


def scale(event):
    """Resizing tiles"""
    print(event.delta)

    delta = 5

    if event.delta > 0:
        MAP.TILE_SIZE += delta
    elif MAP.TILE_SIZE - delta > 0:
        MAP.TILE_SIZE -= delta

    TILES.resize(MAP.TILE_SIZE)
    Update()
    #resizing canvas
    __main__.cv.config(scrollregion=(0, 0, MAP.TILE_SIZE * MAP.WIDTH, MAP.TILE_SIZE * MAP.HEIGHT))

def erase(event):
    """Erasing tile"""
    #TODO implement layers
    paint(event, tile_id = 0)

def CaptureFrame(event, tile_id = 1, layer = 1):
    """Creating frame to modify tiles in area"""
    global x1, y1
    #TODO
    #is lisbox selected?
    if __main__.lb_Tiles.get(ACTIVE) != "":
        tile = __main__.lb_Tiles.get(ACTIVE)
        category = __main__.category.get()

        if tile_id != 0:
            tile_id = TILES.categories[category][tile]["id"]

        #Spawn can be only in one tile
        if tile_id == SPAWN_ID:
            return
    else:
        return

    if __main__.layer.get() != "Layer":
        layer = LAYER[__main__.layer.get()] * MAP.WIDTH * MAP.HEIGHT
        print("read", layer)
    else:
        return


    #handling moving around the canvas with scrollbar
    scroll_h_shift = int(__main__.hbar.get()[0] * MAP.TILE_SIZE * MAP.WIDTH)
    scroll_v_shift = int(__main__.vbar.get()[0] * MAP.TILE_SIZE * MAP.HEIGHT)

    #"6" stands for Motion
    #"5" stands for ButtonRelease
    #"4" stands for ButtonPress
    if event.type == "4":
        x1, y1 = event.x + scroll_h_shift, event.y + scroll_v_shift

    if event.type == "5":
        x2, y2 = event.x + scroll_h_shift, event.y + scroll_v_shift

        #handling arrayboundary
        if x1 >= MAP.TILE_SIZE * MAP.WIDTH or y1 >= MAP.TILE_SIZE * MAP.HEIGHT:
            return
        if x2 >= MAP.TILE_SIZE * MAP.WIDTH or y2 >= MAP.TILE_SIZE * MAP.HEIGHT:
            return

        __main__.cv.delete("CaptureFrame")


        A = int(x1 // MAP.TILE_SIZE) + int(y1 // MAP.TILE_SIZE) * MAP.WIDTH
        B = int(x2 // MAP.TILE_SIZE) + int(y1 // MAP.TILE_SIZE) * MAP.WIDTH

        C = int(x1 // MAP.TILE_SIZE) + int(y2 // MAP.TILE_SIZE) * MAP.WIDTH
        #D = int(x2 // MAP.TILE_SIZE) + int(y2 // MAP.TILE_SIZE) * MAP.WIDTH
        #handling shape
        if C>=A:
            d = C // MAP.WIDTH - A // MAP.WIDTH
            k = 1
        else:
            d = A // MAP.WIDTH - C // MAP.WIDTH
            k = (-1)

        if A > B:
            A, B = B, A
        # A-----------B
        # |           |
        # |           |
        # |           |
        # C-----------D

        for j in range(d + 1):
            for i in range(A, B + 1):
                cords = i + k*j * MAP.WIDTH
                cords += layer

                MAP.MAP[cords] = tile_id

        print(MAP.MAP)

        Update()

        return

    if event.type == "6":
        x2, y2 = event.x + scroll_h_shift, event.y + scroll_v_shift

        __main__.cv.delete("CaptureFrame")
        __main__.cv.create_line(x1, y1, x1, y2, x2, y2, x2, y1, x1, y1, tags = "CaptureFrame")
    #(x1,y1)-----(x2,y1)
    # |           |
    # |           |
    # |           |
    #(x1,y2)-----(x2,y2)

def EraseFrame(event):
    """Erasing tiles in frame"""
    CaptureFrame(event, tile_id = 0)

