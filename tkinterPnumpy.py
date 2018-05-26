import tkinter as tk
from PIL import ImageTk, Image
import cv2
import numpy as np
from time import sleep

def setup_window():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_size_string = str(int(screen_width/2)) + 'x' + str(int(screen_height/2)) + '+50+50'
    root.geometry(screen_size_string)
    return root

def closeAll(event):
    #    root.withdraw() # if you want to bring it back
    root.destroy()
    sys.exit()  # if you want to exit the entire thing

def convNPimageToTK(npAr):
    new_im = Image.fromarray(npAr)
    new_imTk = ImageTk.PhotoImage(new_im, 'RGB')
    sleep(1)
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
    new_image = img_np
    new_imTk = convNPimageToTK(new_image)
    old_img = np.asarray( new_imTk, dtype='uint8' )
    print (old_img)
    print(val)
    print(type(new_imTk))
    print(type(img))
    resize_image(panel,panel_image,new_imTk)

if __name__ == '__main__':
    root = setup_window()

    path = 'C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\elephant.jpg'
    path2 = 'C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\lights600x400.jpg'
    img = ImageTk.PhotoImage(Image.open(path))
    img2 = ImageTk.PhotoImage(Image.open(path2))
    img_np = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img_np2 = cv2.imread(path2, cv2.IMREAD_UNCHANGED)

    panel = tk.Canvas(root, width=600, height=500, cursor="cross")
    panel_image = panel.create_image(0, 0, anchor="nw", image=img)

    panel.place(x=50, y=20)

    w = tk.Scale(panel, from_=0, to=40, command = change_brightness)
    w.place(x=100, y=100)

    imTk = createNewImage(path2)

    root.bind('<Escape>', closeAll)
    root.mainloop()
