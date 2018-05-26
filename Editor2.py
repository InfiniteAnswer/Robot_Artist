import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import threading
from time import sleep
import cv2
import sys
import numpy as np

# class slider_control():
#     def __init__(self,y_pos, label):
#         y_offset = 0
#         self.enable = tk.Checkbutton(panel_menu, bg='green', text = label)
#         self.enable.place(x=10, y=y_pos+y_offset)
#         self.slider = tk.Scale(panel_menu, from_=-100, to=100, orient = tk.HORIZONTAL, bg='green', relief=tk.RAISED)
#         self.slider.place(x=100, y=y_pos-10+y_offset)
#
# class pixel_control():
#     def __init__(self,y_pos, label):
#         y_offset = 0
#         self.label = tk.Label(panel_menu, bg='green', text=label)
#         self.label.place(x=30, y=y_pos+y_offset)
#         self.value = tk.Entry(panel_menu, width=10)
#         self.value.place(x=100, y=y_pos+y_offset)
#
# class mapping_entry():
#     def __init__(self,y_pos,step):
#         y_offset = 0
#         self.value = tk.Entry(panel_menu, width=4)
#         self.value.insert(tk.END, '{:03d}'.format(mapping_values[step]))
#         self.value.place(x=70, y=y_pos + y_offset)

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

class MappingX():
    def __init__(self,widget, y_pos, i, i_val):
        y_offset = 0
        if i == 0:
            self.label = tk.Label(widget, bg='green', text='000 ... ')
        else:
            self.label = tk.Label(widget, bg='green', text='{:03d} ... '.
                                  format(i_val))
        self.label.place(x=30, y=y_pos+y_offset)
        self.slider = tk.Scale(widget, from_=0, to=255, orient=tk.HORIZONTAL, bg='green', relief=tk.RAISED)
        self.slider.set(i_val)
        self.slider.place(x=100, y=y_pos + y_offset-10)

class Win():
    def __init__(self, win, background_colour):
        y_spacing = 40
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

        self.mapping_object_list = []
        for i,i_val in enumerate(self.mapping_values):
            new_object = MappingX(self.menu_panel, y_offset + (8+i)*y_spacing,i,i_val)
            self.mapping_object_list.append(new_object)
        print('mapping object list:',self.mapping_object_list)

        # Add controls to load an image
        self.image_filename_val = tk.StringVar()
        self.image_filename_val.set('C:\\Users\\Victor\\Documents\\Python\\openCV\\Images\\elephant.jpg')
        self.image_filename = tk.Entry(self.image_panel, width=100, textvariable=self.image_filename_val)
        self.image_filename.place(x=50, y=650)
        self.image_np_original = self.load_master()
        self.image_np_modified = self.image_np_original
        self.image_np_modified_unexpanded = self.image_np_modified
        # self.imageTk = resize_numpy_image(cv2.imread(self.image_filename_val.get(),cv2.IMREAD_GRAYSCALE),790.0)
        self.imageTk = ImageTk.PhotoImage(Image.fromarray(self.image_np_modified))
        self.imge = self.image_panel.create_image(5, 5, anchor="nw", image = self.imageTk)
        # handler = lambda \
        #     img_np=cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE), img=resize_numpy_image(
        #     cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE), 790.0): load_image(
        #     self.image_panel, self.imge, img, self.image_filename_val.get(), img_np)

        self.image_browse = tk.Button(self.image_panel, text="Browse", command=self.open_browser)
        self.image_browse.place(x=665, y=648)
        self.image_load = tk.Button(self.image_panel, text="Load", command=self.update_all)
        self.image_load.place(x=720, y=648)
        root.bind('<Return>', self.update_event_handler)
        root.bind('<Tab>', self.update_event_handler)
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
        target_width = 790
        ratio = target_width / numpy_image.shape[1]
        target_dim = (int(target_width), int(numpy_image.shape[0] * ratio))
        return cv2.resize(numpy_image, target_dim, interpolation=cv2.INTER_AREA)

    def modify_con_bri(self):
        if self.contrast_check.enable_val.get()==1:
            multiply_array = np.ones_like(self.image_np_modified,dtype=np.float) * self.contrast_check.slider.get() /100 + 1
            print('Contrast:', self.contrast_check.slider.get())
            print(multiply_array)
            print(self.image_np_modified)
            self.image_np_modified = np.multiply(self.image_np_modified, multiply_array)
            self.image_np_modified = self.image_np_modified.astype(int)
            print(self.image_np_modified)
        if self.brightness_check.enable_val.get()==1:
            print('Brightness: ', self.brightness_check.slider.get())
            self.image_np_modified += self.brightness_check.slider.get()

    def pixelate_image(self):
        if self.pixelate_val.get() == 1:
            target_width=790
            ratio = target_width / self.image_np_modified.shape[1]
            target_dim = (int(target_width), int(self.image_np_modified.shape[0] * ratio))
            dim_original = (self.image_np_modified.shape[1], self.image_np_modified.shape[0])
            dim = (int(self.x_px.value_val.get()), int(self.y_px.value_val.get()))
            self.image_np_modified = cv2.resize(self.image_np_modified, dim, interpolation=cv2.INTER_AREA)
            print('pixelate image')
            print(self.image_np_modified)
            self.image_np_modified_unexpanded = self.image_np_modified
            print('dimensions')
            print(dim_original)
            print(target_dim)
            self.image_np_modified = cv2.resize(self.image_np_modified_unexpanded, target_dim, interpolation=cv2.INTER_NEAREST)

    def mapping_imageX(self):
        # Update list that stores slider values (note: this is linked to sliders so cannot delete first)
        for x,i in enumerate(self.mapping_object_list):
            self.mapping_values[x] =i.slider.get()
            print('getting value:', i.slider.get())
        print(self.mapping_values)

        # Make sure sliders are not higher than their predecessor
        for x,i in enumerate(self.mapping_object_list):
            if x>0:
                i.label.config(text='{:03d} ... '.format(self.mapping_values[x-1]))
                if self.mapping_values[x]<self.mapping_values[x-1]:
                    self.mapping_values[x] = self.mapping_values[x-1]+1
                    i.slider.set(self.mapping_values[x])

        # Create list of logical maps for each mapped colour
        logic_map = []
        for x,i in enumerate(self.mapping_values):
            if x==0:
                logic_map.append(self.image_np_modified<=self.mapping_values[0])
            else:
                logic_map.append(np.logical_and (self.image_np_modified>self.mapping_values[x-1], self.image_np_modified<=self.mapping_values[x]))
        logic_map.append(self.image_np_modified>self.mapping_values[-1])

        # Remap
        if self.mapping_val.get() == 1:
            # print('Remapping values:',self.mapping_values)
            for x,i in enumerate(logic_map):
                    self.image_np_modified[i] = int(x*255/len(self.mapping_values))
                    print(int(x*255/len(self.mapping_values)))
                    print(i)

    def get_palette(self):
        palette = dict()
        if self.pixelate_val.get() == 1:
            logic_map = []
            for x, i in enumerate(self.mapping_values):
                if x == 0:
                    logic_map.append(self.image_np_modified_unexpanded <= self.mapping_values[0])
                else:
                    logic_map.append(np.logical_and(self.image_np_modified_unexpanded > self.mapping_values[x - 1],
                                                    self.image_np_modified_unexpanded <= self.mapping_values[x]))
            logic_map.append(self.image_np_modified_unexpanded > self.mapping_values[-1])

            # Remap
            if self.mapping_val.get() == 1:
                print('Remapping values:', self.mapping_values)
                for x, i in enumerate(logic_map):
                    self.image_np_modified_unexpanded[i] = int(x * 255 / len(self.mapping_values))

        print(self.image_np_modified_unexpanded)
        for r in self.image_np_modified_unexpanded:
            for c in r:
                if c in palette:
                    palette[c] += 1
                if not(c in palette):
                    palette.update({c:1})

        print('pallette:',palette)

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
        self.mapping_imageX()
        self.get_palette()
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

if __name__ == '__main__':
    root = tk.Tk()
    w = Win(root, 'green')
    print('main program running')
    root.bind('<Escape>', closeAll)
    root.mainloop()