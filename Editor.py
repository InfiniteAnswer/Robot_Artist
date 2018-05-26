import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import threading
from time import sleep
import cv2
import sys
import numpy as np

class slider_control():
    def __init__(self,y_pos, label):
        y_offset = 0
        self.enable = tk.Checkbutton(panel_menu, bg='green', text = label)
        self.enable.place(x=10, y=y_pos+y_offset)
        self.slider = tk.Scale(panel_menu, from_=-100, to=100, orient = tk.HORIZONTAL, bg='green', relief=tk.RAISED)
        self.slider.place(x=100, y=y_pos-10+y_offset)

class pixel_control():
    def __init__(self,y_pos, label):
        y_offset = 0
        self.label = tk.Label(panel_menu, bg='green', text=label)
        self.label.place(x=30, y=y_pos+y_offset)
        self.value = tk.Entry(panel_menu, width=10)
        self.value.place(x=100, y=y_pos+y_offset)

class mapping_entry():
    def __init__(self,y_pos,step):
        y_offset = 0
        self.value = tk.Entry(panel_menu, width=4)
        self.value.insert(tk.END, '{:03d}'.format(mapping_values[step]))
        self.value.place(x=70, y=y_pos + y_offset)

class PixelControl():
    def __init__(self,widget, y_pos, label):
        y_offset = 0
        self.value_val = tk.StringVar()
        self.label = tk.Label(widget, bg='green', text=label)
        self.label.place(x=30, y=y_pos+y_offset)
        self.value = tk.Entry(widget, width=10, textvariable=self.value_val)
        self.value.place(x=100, y=y_pos+y_offset)

class Slide():
    def __init__(self, widget, y_pos, label):
        y_offset = 0
        self.enable_val = tk.IntVar()
        self.enable = tk.Checkbutton(widget, bg='green', text = label, variable=self.enable_val)
        self.enable.place(x=10, y=y_pos+y_offset)
        self.slider = tk.Scale(widget, from_=-100, to=100, orient = tk.HORIZONTAL, bg='green', relief=tk.RAISED)
        self.slider.place(x=100, y=y_pos-10+y_offset)

class Mapping():
    def __init__(self,widget, y_pos, value):
        y_offset = 0
        self.value_val = tk.StringVar()
        self.value = tk.Entry(widget, width=4, textvariable=self.value_val)
        self.value.insert(tk.END, '{:03d}'.format(value))
        self.value.place(x=70, y=y_pos + y_offset)

class Win():
    def __init__(self, win, background_colour):
        y_spacing = 50
        y_offset = 80
        win.geometry('1065x710+50+10')

        # Setup 2 panels in the window and open a starting image
        self.image_panel = tk.Canvas(win, width=800, height=700, cursor="cross", bg=background_colour)
        self.menu_panel = tk.Canvas(win, width=250, height=700, cursor="cross", bg=background_colour)
        self.image_panel.place(x=5, y=5)
        self.menu_panel.place(x=810, y=5)

        # Add the controls for contrast and brightness
        self.contrast_check = Slide(self.menu_panel, y_offset + 0 * y_spacing, "Contrast")
        self.brightness_check = Slide(self.menu_panel, y_offset + 1 * y_spacing, "Brightness")

        # Add the controls for pixelation
        self.pixelate_val = tk.IntVar()
        self.pixelate = tk.Checkbutton(self.menu_panel, bg=background_colour, text = "Pixelate",
                                       variable=self.pixelate_val)
        self.pixelate.place(x=10, y=y_offset + 3*y_spacing)
        self.x_px = PixelControl(self.menu_panel, y_offset + 4*y_spacing, "Pixelate X")
        self.y_px = PixelControl(self.menu_panel, y_offset + 5*y_spacing, "Pixelate Y")

        # Add the controls for mapping grays to tile colours
        self.mapping_val = tk.IntVar()
        self.mapping = tk.Checkbutton(self.menu_panel, bg=background_colour, text = "Mapping",
                                      variable=self.mapping_val)
        self.mapping.place(x=10, y=y_offset + 7*y_spacing)
        self.mapping_values = [1,2,3,4]
        self.mapping_0 = tk.Label(self.menu_panel, bg=background_colour, text='000 ... ')
        self.mapping_0.place(x=30, y=y_offset + 8*y_spacing)
        self.mapping_0_val = Mapping(self.menu_panel, y_offset + 8*y_spacing,1)
        self.mapping_1 = tk.Label(self.menu_panel, bg=background_colour, text='{:03d} ... '.
                                  format(self.mapping_values[0]))
        self.mapping_1.place(x=30, y=y_offset + 9 * y_spacing)
        self.mapping_1_val = Mapping(self.menu_panel, y_offset + 9 * y_spacing,self.mapping_values[1])
        self.mapping_2 = tk.Label(self.menu_panel, bg=background_colour, text='{:03d} ... '.
                                  format(self.mapping_values[1]))
        self.mapping_2.place(x=30, y=y_offset + 10 * y_spacing)
        self.mapping_2_val = Mapping(self.menu_panel, y_offset + 10 * y_spacing,self.mapping_values[2])
        self.mapping_3 = tk.Label(self.menu_panel, bg=background_colour, text='{:03d} ... '.
                                  format(self.mapping_values[2]))
        self.mapping_3.place(x=30, y=y_offset + 11 * y_spacing)
        self.mapping_3_val = Mapping(self.menu_panel, y_offset + 11 * y_spacing,self.mapping_values[3])

        # Add controls to load an image
        self.image_filename_val = tk.StringVar()
        self.image_filename_val.set('C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\elephant.jpg')
        self.image_filename = tk.Entry(self.image_panel, width=100, textvariable=self.image_filename_val)
        self.image_filename.place(x=50, y=650)
        self.image_np_original = self.load_master()
        self.image_np_modified = self.image_np_original
        # self.imageTk = resize_numpy_image(cv2.imread(self.image_filename_val.get(),cv2.IMREAD_GRAYSCALE),790.0)
        self.imageTk = ImageTk.PhotoImage(Image.fromarray(self.image_np_modified))
        self.imge = self.image_panel.create_image(5, 5, anchor="nw", image = self.imageTk)
        handler = lambda \
            img_np=cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE), img=resize_numpy_image(
            cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE), 790.0): load_image(
            self.image_panel, self.imge, img, self.image_filename_val.get(), img_np)

        self.image_browse = tk.Button(self.image_panel, text="Browse", command=self.open_browser)
        self.image_browse.place(x=665, y=648)
        self.image_load = tk.Button(self.image_panel, text="Load", command=self.update_all)
        self.image_load.place(x=720, y=648)
        root.bind("<ButtonRelease-1>", self.update_event_handler)

    def update_event_handler(self, event):
        self.update_all()

    def open_browser(self):
        self.image_filename_val.set(filedialog.askopenfilename(parent=root))
        self.image_np_original = self.load_master()
        self.image_np_modified = self.image_np_original
        print('new image loaded')

    def load_master(self):
        numpy_image = cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE)
        return numpy_image

    def modify_con_bri(self):
        if self.contrast_check.enable_val.get()==1:
            multiply_array = np.ones_like(self.image_np_modified,dtype=np.float) * self.contrast_check.slider.get() /100 + 1
            print(self.contrast_check.slider.get())
            print(multiply_array)
            self.image_np_modified = np.multiply(self.image_np_modified, multiply_array)
            self.image_np_modified.astype(int)
        if self.brightness_check.enable_val.get()==1:
            print('Brightness: ', self.brightness_check.slider.get())
            self.image_np_modified += self.brightness_check.slider.get()

    def pixelate_image(self):
        if self.pixelate_val.get() == 1:
            dim_original = (self.image_np_modified.shape[1], self.image_np_modified.shape[0])
            # dim_original = map(tuple,self.image_np_modified.shape)
            dim = (int(self.x_px.value_val.get()), int(self.y_px.value_val.get()))
            self.image_np_modified = cv2.resize(self.image_np_modified, dim, interpolation=cv2.INTER_AREA)
            self.image_np_modified = cv2.resize(self.image_np_modified, dim_original, interpolation=cv2.INTER_AREA)

    def mapping_image(self):
        self.mapping_values = [int(self.mapping_0_val.value_val.get()),
                               int(self.mapping_1_val.value_val.get()),
                               int(self.mapping_2_val.value_val.get()),
                               int(self.mapping_3_val.value_val.get())]
        if self.mapping_val.get() == 1:
            print(self.mapping_values)
            map_0=(self.image_np_modified<self.mapping_values[0])
            map_1=np.logical_and (self.image_np_modified>=self.mapping_values[0], self.image_np_modified<self.mapping_values[1])
            map_2 = np.logical_and(self.image_np_modified >= self.mapping_values[1], self.image_np_modified < self.mapping_values[1])
            map_3 = np.logical_and(self.image_np_modified >= self.mapping_values[2], self.image_np_modified < self.mapping_values[3])
            self.image_np_modified[map_0]=0
            self.image_np_modified[map_1] = 90
            self.image_np_modified[map_2] = 180
            self.image_np_modified[map_3] = 255


    def image_update(self):
        # self.image_panel.itemconfigure(self.imge, image=ImageTk.PhotoImage(Image.fromarray(self.image_np_modified)))
        self.imageTk=ImageTk.PhotoImage(Image.fromarray(self.image_np_modified))
        self.image_panel.itemconfigure(self.imge,image=self.imageTk)

    def update_all(self):
        self.image_np_modified = self.load_master()
        # If the brightness and contrast checkbutton is on, then modify the contrast and brightness
        self.modify_con_bri()
        # If the pixelate button is on, then modify the resolution
        self.pixelate_image()
        # If the mapping button is on, modify the mapping
        self.mapping_image()
        # Update the image
        self.image_update()
        pass


def load_image(widget, widget_image, img, name,name2):
    global new_image
    new_image = img
    np_image = cv2.imread(name,cv2.IMREAD_GRAYSCALE)
    new_image = resize_numpy_image(np_image,700)
    widget.itemconfigure(widget_image, image=new_image)
    pass

def resize_numpy_image(np_image,w):
    target_width = w
    ratio = target_width / np_image.shape[1]
    target_dim = (int(target_width), int(np_image.shape[0] * ratio))
    resized_np_image = cv2.resize(np_image, target_dim, interpolation=cv2.INTER_AREA)
    new_imTk = ImageTk.PhotoImage(Image.fromarray(resized_np_image))
    return new_imTk

def update_mappings():
    pass


def quit():
    global root
    #    root.quit()
    root.destroy()


def closeAll(event):
    #    root.withdraw() # if you want to bring it back
    root.destroy()
    sys.exit()  # if you want to exit the entire thing


def setup_screen():
    global root, panel_top, panel_original, panel_con_bri, panel_thresh, panel_pixelate,image_filename_val
    global root, panel_menu, mapping_entry, mapping_values, panel, panel_image, imageTk
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
    panel_menu = tk.Canvas(root, width=250, height=700, cursor="cross", bg=background_colour)
    panel_menu.place(x=810, y=5)

    contrast_check = slider_control(y_offset + 0*y_spacing,"Contrast")
    contrast_check = slider_control(y_offset + 1*y_spacing,"Brightness")

    x_px = pixel_control(y_offset + 4*y_spacing, "Pixelate X")
    y_px = pixel_control(y_offset + 5*y_spacing, "Pixelate Y")
    pixelate = tk.Checkbutton(panel_menu, bg='green', text = "Pixelate")
    pixelate.place(x=10, y=y_offset + 3*y_spacing)

    mapping = tk.Checkbutton(panel_menu, bg='green', text = "Mapping")
    mapping.place(x=10, y=y_offset + 7*y_spacing)
    mapping_values = [0,1,2,3]

    mapping_0 = tk.Label(panel_menu, bg='green', text='000 ... ')
    mapping_0.place(x=30, y=y_offset + 8*y_spacing)
    mapping_0_val = mapping_entry(y_offset + 8*y_spacing,0)

    mapping_1 = tk.Label(panel_menu, bg='green', text='{:03d} ... '.format(mapping_values[1]))
    mapping_1.place(x=30, y=y_offset + 9 * y_spacing)
    mapping_1_val = mapping_entry(y_offset + 9 * y_spacing,1)

    mapping_2 = tk.Label(panel_menu, bg='green', text='{:03d} ... '.format(mapping_values[2]))
    mapping_2.place(x=30, y=y_offset + 10 * y_spacing)
    mapping_2_val = mapping_entry(y_offset + 10 * y_spacing,2)

    mapping_3 = tk.Label(panel_menu, bg='green', text='{:03d} ... '.format(mapping_values[3]))
    mapping_3.place(x=30, y=y_offset + 11 * y_spacing)
    mapping_3_val = mapping_entry(y_offset + 11 * y_spacing,3)

    image_filename_val = tk.StringVar()
    image_filename_val.set('C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\elephant.jpg')
    image_filename = tk.Entry(panel, width=100, textvariable=image_filename_val)
    image_filename.place(x=50, y=650)
    image_load = tk.Button(panel, text="Load", command=open_new_image)
    image_load.place(x=700, y=648)

    file_to_open = image_filename_val.get()
    imageTk = ImageTk.PhotoImage(Image.open(file_to_open))
    print('name:',file_to_open)
    panel_image = panel.create_image(5, 5, anchor="nw", image = imageTk)
    print(type(panel_image))



def change_brightness():
    pass

def change_contrast():
    pass

def modify_thresholds():
    pass

def pixelate():
    pass

# if __name__ == '__main__':
    # setup_screen()

root = tk.Tk()
w = Win(root, 'green')
print('main program running')
root.bind('<Escape>', closeAll)
root.mainloop()