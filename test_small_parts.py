import tkinter as tk
from PIL import ImageTk, Image
import cv2
import numpy as np
from time import sleep

def setup_window():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_size_string = str(screen_width) + 'x' + str(screen_height) + '+50+50'
    root.geometry(screen_size_string)
    return root

def closeAll(event):
    #    root.withdraw() # if you want to bring it back
    root.destroy()
    sys.exit()  # if you want to exit the entire thing

def convNPimageToTK(npAr):
    new_im = Image.fromarray(npAr)
    new_imTk = ImageTk.PhotoImage(new_im, 'RGB')
    print('image conversion complete')
    return new_imTk

def createNewImage(path):
    frame = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    target_width = 100.0
    r = target_width / frame.shape[1]
    dim = (int(target_width), int(frame.shape[0] * r))
    resized_image = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    imTk = convNPimageToTK(resized_image)
    return imTk

def resize_image(panel_u, panel_u_image, immg):
    panel.itemconfig(panel_image, image=immg)

def change_brightness(val):
    global new_imTk
    new_image = img_np
    # new_imTk = convNPimageToTK(new_image)
    new_imTk = ImageTk.PhotoImage(Image.fromarray(new_image))
    print('hi there')
    # root.after(1000, resize_image,panel,panel_image,new_imTk)

    resize_image(panel, panel_image, new_imTk)
    print('update complete')
    # panel.itemconfigure(panel_image,image = img2)

def loadnewimage():
    global img
    print(str(path.get()))
    img = ImageTk.PhotoImage(Image.open(path.get()))
    panel.itemconfig(panel_image, image=img)

if __name__ == '__main__':
    root = setup_window()

    panel = tk.Canvas(root, width=600, height=500, cursor="cross")

    path = 'C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\elephant.jpg'
    path2 = 'C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\lights600x400.jpg'
    img = ImageTk.PhotoImage(Image.open(path))
    img2 = ImageTk.PhotoImage(Image.open(path2))
    img_np = cv2.imread(path2, cv2.IMREAD_UNCHANGED)
    new_image = img_np + 100
    new_imTk = convNPimageToTK(new_image)
    panel_image = panel.create_image(0, 0, anchor="nw", image=new_imTk)
    panel_rect = panel.create_rectangle(50, 25, 150, 75, outline="blue")

    # panel.pack(side = "top", fill = "both", expand = "yes")
    panel.place(x=50, y=20)
    w = tk.Scale(panel, from_=0, to=40, command = change_brightness)
    w.place(x=100, y=100)
    imTk = createNewImage(path2)
    # resize_image(panel, panel_image, imTk)
    new_image = img_np
    # new_imTk = convNPimageToTK(new_image)
    print('hi there')

    b = tk.Button(root, text = 'load', command = loadnewimage)
    b.place(x=500, y=600)
    path = tk.StringVar()
    e=tk.Entry(root, textvariable = path, width = 60)
    e.place(x=400,y=400)

    # root.after(1000, resize_image,panel,panel_image,new_imTk)

    root.bind('<Escape>', closeAll)
    root.mainloop()
