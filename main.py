from tkinter import *
from tkinter import ttk

from parameters import *
import menubar as mb

if __name__ == '__main__':
    import map as mp

NAME = "Map Editor"
VERSION = "1.0.0 alpha"
INFO = NAME + " by nikonru\n Version " + VERSION

def update_list(event):
    """Updating lb_Tiles when changing category"""
    k = list(TILES.categories[category.get()].keys())
    k = StringVar(value=k)

    lb_Tiles.config(listvariable=k)


def update_preview(event):
    """updating preview"""
    if not lb_Tiles.curselection():
        return

    tile = lb_Tiles.get(lb_Tiles.curselection())
    cat = category.get()

    image = TILES.categories[cat][tile]["pil"]
    preview.image = ImageTk.PhotoImage(image)

    preview.create_image(0, 0, anchor=NW, image=preview.image)

# Setting GUI

root = Tk()
root.title(NAME)
#root.state('zoomed')
#root.attributes('-zoomed',True)

# dividing interface between base zones
map = Frame(root)
map.pack(expand=True, side=RIGHT)

toolbar = Frame(root)
toolbar.pack(expand=True, side=LEFT)

menubar = Menu(root)
# dividing interface between base zones

# Menubar
filemenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="New", command=mb.New)
filemenu.add_command(label="Open", command=mb.Open)
filemenu.add_command(label="Save", command=mb.Save)
filemenu.add_command(label="Save As", command=mb.Save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
# Menubar

# toolbar
Display_Grid = IntVar()
cb_grid = Checkbutton(toolbar, text = "Display Grid", variable = Display_Grid, onvalue = 1, offvalue = 0,
                      command = mp.Update)
cb_grid.grid(column=0)

Show_only_layer = IntVar()
chosen_layer = Checkbutton(toolbar, text = "Show only chosen layer", variable = Show_only_layer, onvalue = 1, offvalue = 0,
                      command = mp.Update)
chosen_layer.grid(column=0)

layer = ttk.Combobox(toolbar, values=["Skybox", "Background", "Level", "Foreground"], state="readonly")
layer.bind('<<ComboboxSelected>>', mp.Update)
layer.set("Layer")
layer.grid(column=0)

cat = list(TILES.categories.keys())

category = ttk.Combobox(toolbar, values = cat, state = "readonly")
category.bind('<<ComboboxSelected>>', update_list)
category.set("Category")
category.grid(column=0)

lb_Tiles = Listbox(toolbar, selectmode=SINGLE)
lb_Tiles.bind('<<ListboxSelect>>', update_preview)
lb_Tiles.grid(column=0)
# toolbar

# Canvas
cv = Canvas(map, bg='white', scrollregion=(0, 0, MAP.TILE_SIZE*MAP.WIDTH, MAP.TILE_SIZE*MAP.HEIGHT))

hbar = Scrollbar(map, orient=HORIZONTAL)
hbar.pack(side=BOTTOM, fill=X)
hbar.config(command=cv.xview)

vbar = Scrollbar(map, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=cv.yview)

cv.config(width=MAP.TILE_SIZE*MAP.WIDTH, height=MAP.TILE_SIZE*MAP.HEIGHT)
cv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
cv.pack(side=LEFT, expand=True, fill=BOTH)

# Canvas

#small preview
preview = Canvas(toolbar, bg="white")
preview.grid(column = 0)
preview.config(width = TILE_SIZE, height = TILE_SIZE)

#info
info = Label(toolbar,text = INFO)
info.grid(column = 0)
#Setting GUI

cv.bind('<ButtonRelease-1>', mp.paint,  add = "+")
cv.bind('<ButtonRelease-3>', mp.erase, add = "+")

cv.bind('<ButtonPress-1>', mp.CaptureFrame)
cv.bind('<B1-Motion>', mp.CaptureFrame)
cv.bind('<ButtonRelease-1>', mp.CaptureFrame, add = "+")

cv.bind('<ButtonPress-3>', mp.EraseFrame)
cv.bind('<B3-Motion>', mp.EraseFrame)
cv.bind('<ButtonRelease-3>', mp.EraseFrame, add = "+")

cv.bind('<MouseWheel>', mp.scale)

cv.pack(expand=YES, fill=BOTH)

#preparing images for Tkinter canvas
TILES.convert2Tk()

root.mainloop()


