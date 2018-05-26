import tkinter as tk
from PIL import ImageTk, Image
import threading
from time import sleep
import cv2
import sys
import numpy as np




def quit():
    global root
    #    root.quit()
    root.destroy()


def closeAll(event):
    #    root.withdraw() # if you want to bring it back
    root.destroy()
    sys.exit()  # if you want to exit the entire thing




if __name__ == '__main__':
    y_spacing = 50
    y_offset = 80
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # screen_size_string = str(screen_width) + 'x' + str(screen_height) + '+50+50'
    root.geometry('1065x710+50+10')
    background_colour = 'green'

    panel = tk.Canvas(root, width=800, height=700, cursor="cross", bg=background_colour)
    panel.place(x=5, y=5)

    image_filename_val = tk.StringVar()
    image_filename_val.set('C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\elephant.jpg')

    file_to_open = image_filename_val.get()
    imageTk = ImageTk.PhotoImage(Image.open(file_to_open))
    print('name:', file_to_open)
    panel_image = panel.create_image(0, 0, anchor="nw", image=imageTk)
    print(type(panel_image))



root.bind('<Escape>', closeAll)
root.mainloop()