import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import *
from PIL import ImageTk, Image
import threading
from time import sleep
import cv2
import sys
import numpy as np
import pickle
from matplotlib import pyplot as plt



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
        # Convert slider set point to a gray scale value between 0 and 255
        grayscale = i_val
        # Convert grayscale value to RGB tuple
        v = int(grayscale / 1)
        # RGBtuple = (v, v, v)
        # Convert RGB tuple to a Hex string
        self.button_color = "#{0:02x}{1:02x}{2:02x}".format(v, v, v)
        self.button_color_dec = (v, v, v)
        self.button = tk.Button(widget, width=2, bg = self.button_color, command = self.getColor)
        self.button.place(x = 220, y=y_pos + y_offset)

    def getColor(self):
        selection = askcolor()
        self.button_color_dec = selection[0]
        self.button_color = selection[1]
        # print('New color confirmed:', self.button_color, self.button_color_dec)

class Win():
    def __init__(self, win, background_colour):
        y_spacing = 40
        y_offset = 80
        win.geometry('1065x760+50+10')
        self.lines = []
        # Setup 2 panels in the window and open a starting image
        self.image_panel = tk.Canvas(win, width=800, height=750, cursor="cross", bg=background_colour)
        self.menu_panel = tk.Canvas(win, width=250, height=750, cursor="cross", bg=background_colour)
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

        self.grid_val = tk.IntVar()
        self.grid = tk.Checkbutton(self.menu_panel, bg=background_colour, text="Grid",
                                   variable=self.grid_val)
        self.grid.place(x=100, y=y_offset + 3*y_spacing)

        self.x_px = PixelControl(self.menu_panel, y_offset + 4*y_spacing, "Pixelate X")
        self.y_px = PixelControl(self.menu_panel, y_offset + 5*y_spacing, "Pixelate Y")

        # Add the controls for mapping grays to tile colours
        self.mapping_val = tk.IntVar()
        self.mapping = tk.Checkbutton(self.menu_panel, bg=background_colour, text = "Mapping",
                                      variable=self.mapping_val)
        self.mapping.place(x=10, y=y_offset + 7*y_spacing)

        # Option to set number of values
        self.mapping_values_length = tk.StringVar()
        self.mapping_values_length_old = tk.StringVar()
        self.mapping_values_length.set('5')
        self.mapping_values_length_old.set(self.mapping_values_length.get())
        self.mapping_values_label = tk.Label(self.menu_panel, bg='green', text='Levels')
        self.mapping_values_label.place(x=30, y=20)
        self.mapping_values_value = tk.Entry(self.menu_panel, width=10, textvariable=self.mapping_values_length)
        self.mapping_values_value.place(x=100, y=20)
        self.mapping_values = []
        l = int(self.mapping_values_length.get())
        for i in range(l):
            if i<l-1:
                self.mapping_values.append(int(255/l)*i)
            else:
                self.mapping_values.append(255)

        #self.mapping_values = [1,2,3,4,5]

        self.mapping_object_list = []
        for i,i_val in enumerate(self.mapping_values):
            new_object = MappingX(self.menu_panel, y_offset + (8+i)*y_spacing,i,i_val)
            self.mapping_object_list.append(new_object)
        # print('mapping object list:',self.mapping_object_list)

        # Add controls to load an image
        self.image_filename_val = tk.StringVar()
        self.image_filename_val.set('C:\\Users\\v_sam\\Documents\\Python\\openCV\\Images\\lady_face.jpg')
        self.image_filename = tk.Entry(self.image_panel, width=100, textvariable=self.image_filename_val)
        self.image_filename.place(x=30, y=650)
        self.image_np_original = self.load_master()
        self.image_np_modified = self.image_np_original
        self.image_np_modified_unexpanded = self.image_np_modified
        self.image_np_modified_BGR = np.stack((self.image_np_modified, self.image_np_modified, self.image_np_modified))

        # plt.ion()
        # self.fig = plt.figure()
        # self.ax = self.fig.add_subplot(111)
        # [n, X, V] = self.ax.hist(self.image_np_modified, bins=256, normed=True)
        # self.params = [n, X, V]
        # # hist_full = cv2.calcHist(self.image_np_modified_unexpanded, [0], None, [256], [0, 256])
        # self.hist_chart = ax.plot(hist_full)
        # self.fig.canvas.draw()

        self.imageTk = ImageTk.PhotoImage(Image.fromarray(self.image_np_modified))
        self.imge = self.image_panel.create_image(400,325, anchor="center", image = self.imageTk)

        # handler = lambda \
        #     img_np=cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE), img=resize_numpy_image(
        #     cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE), 790.0): load_image(
        #     self.image_panel, self.imge, img, self.image_filename_val.get(), img_np)

        self.image_browse = tk.Button(self.image_panel, text="Browse", command=self.open_browser)
        self.image_browse.place(x=645, y=648)
        self.image_load = tk.Button(self.image_panel, text="Load", command=self.update_all)
        self.image_load.place(x=700, y=648)


        # Add controls to load a configuration
        self.configuration_filename_val = tk.StringVar()
        self.configuration_filename_val.set('')
        self.configuration_filename = tk.Entry(self.image_panel, width=100, textvariable = self.configuration_filename_val)
        self.configuration_filename.place(x=30, y=680)
        self.configuration_browse = tk.Button(self.image_panel, text="Browse", command=self.open_configuration_browser)
        self.configuration_browse.place(x=645, y=678)
        self.configuration_load = tk.Button(self.image_panel, text="Load", command=self.load_configuration)
        self.configuration_load.place(x=700, y=678)
        self.configuration_save = tk.Button(self.image_panel, text="Save", command=self.save_configuration)
        self.configuration_save.place(x=742, y=678)

        root.bind('<Return>', self.update_event_handler)
        root.bind('<Tab>', self.update_event_handler)
        root.bind("<ButtonRelease-1>", self.update_event_handler)

    def update_event_handler(self, event):
        self.update_all()

    def serialise_parameters(self):
        data_list = []
        data_list.append(self.mapping_values_length.get())
        # print ('Origianl value of number of levels:',data_list[0])
        data_list.append(self.contrast_check.enable_val.get())
        data_list.append(self.contrast_check.slider.get())
        data_list.append(self.brightness_check.enable_val.get())
        data_list.append(self.brightness_check.slider.get())
        data_list.append(self.pixelate_val.get())
        data_list.append(self.grid_val.get())
        data_list.append(self.x_px.value_val.get())
        data_list.append(self.y_px.value_val.get())
        data_list.append(self.mapping_val.get())
        data_list.append(self.mapping_values)
        list_colors_hex = []
        list_colors_dec = []
        for i in self.mapping_object_list:
            list_colors_hex.append(i.button_color)
            list_colors_dec.append(i.button_color_dec)
        data_list.append(list_colors_hex)
        data_list.append(list_colors_dec)
        return data_list

    def open_browser(self):
        self.image_filename_val.set(filedialog.askopenfilename(parent=root))
        self.image_np_original = self.load_master()
        self.image_np_modified = self.image_np_original
        self.image_np_modified_unexpanded = self.image_np_modified
        self.image_np_modified_BGR = np.stack((self.image_np_modified, self.image_np_modified, self.image_np_modified))
        # print('new image loaded')

    def open_configuration_browser(self):
        self.configuration_filename_val.set(filedialog.askopenfilename(parent=root))
        # print('new configuration loaded')

    def load_configuration(self):
        filename = self.configuration_filename_val.get()
        serialised_parameters = pickle.load(open(filename, "rb"))
        self.mapping_values_length.set(serialised_parameters[0])
        # print('saved number of levels:', serialised_parameters[0])
        self.mapping_values_length_old.set(serialised_parameters[0])
      #  self.menu_panel.itemconfigure(self.mapping_values_value, textvariable = serialised_parameters[0])
        self.contrast_check.enable_val.set(serialised_parameters[1])
        self.contrast_check.slider.set(serialised_parameters[2])
        self.brightness_check.enable_val.set(serialised_parameters[3])
        self.brightness_check.slider.set(serialised_parameters[4])
        self.pixelate_val.set(serialised_parameters[5])
        self.grid_val.set(serialised_parameters[6])
        self.x_px.value_val.set(serialised_parameters[7])
        self.y_px.value_val.set(serialised_parameters[8])
        self.mapping_val.set(serialised_parameters[9])
        self.mapping_values = serialised_parameters[10]
        print('erasing old configuration')
        for i in self.mapping_object_list:
            i.label.destroy()
            i.slider.destroy()
            i.button.destroy()
        self.mapping_object_list = []
        # print('New mapping values:',self.mapping_values)
        y_spacing = 40
        y_offset = 80
        for i, i_val in enumerate(self.mapping_values):
            new_object = MappingX(self.menu_panel, y_offset + (8 + i) * y_spacing, i, i_val)
            self.mapping_object_list.append(new_object)
            # print(i)
        # print('New mapping objects created')
        list_colors_hex = serialised_parameters[11]
        list_colors_dec = serialised_parameters[12]
        for i, val in enumerate(list_colors_hex):
            self.mapping_object_list[i].button_color = val
            self.mapping_object_list[i].button_color_dec = list_colors_dec[i]

    def save_configuration(self):
        self.configuration_filename_val.set(filedialog.asksaveasfilename(parent=root))
        serialised_parameters = self.serialise_parameters()
        filename = self.configuration_filename_val.get()
        with open(filename, 'wb') as f:
            pickle.dump(serialised_parameters, f)

    def update_mapping_values(self):
        if not(self.mapping_values_length.get() == self.mapping_values_length_old.get()):
            for i in self.mapping_object_list:
                i.label.destroy()
                i.slider.destroy()
                i.button.destroy()
            self.mapping_object_list = []
            self.mapping_values = []
            l = int(self.mapping_values_length.get())
            for i in range(l):
                if i < l - 1:
                    self.mapping_values.append(int(255 / l) * i)
                else:
                    self.mapping_values.append(255)
            y_spacing = 40
            y_offset = 80
            for i, i_val in enumerate(self.mapping_values):
                new_object = MappingX(self.menu_panel, y_offset + (8 + i) * y_spacing, i, i_val)
                self.mapping_object_list.append(new_object)
                # print(i)
            self.mapping_values_length_old.set(self.mapping_values_length.get())

    def load_master(self):
        numpy_image = cv2.imread(self.image_filename_val.get(), cv2.IMREAD_GRAYSCALE)
        temp = cv2.imread(self.image_filename_val.get())
        # print('temp array read shape:', temp.shape)
        if numpy_image.shape[1]>numpy_image.shape[0]:
            self.target_width = 790
        else:
            self.target_width = int(numpy_image.shape[0]/890*numpy_image.shape[1])
        ratio = self.target_width / numpy_image.shape[1]
        target_dim = (int(self.target_width), int(numpy_image.shape[0] * ratio))
        return cv2.resize(numpy_image, target_dim, interpolation=cv2.INTER_AREA)

    def modify_con_bri(self):
        # print('Entering modify con bri loop')
        if self.contrast_check.enable_val.get()==1:
            # print('element type')
            # print(type(self.image_np_modified[0, 0]))
            multiply_array = np.ones_like(self.image_np_modified,dtype=np.float) * self.contrast_check.slider.get() /100 + 1
            self.image_np_modified = np.multiply(self.image_np_modified, multiply_array)
            self.image_np_modified = np.clip(self.image_np_modified,0,255)
            self.image_np_modified = self.image_np_modified.astype(np.uint8)
            # print('element type')
            # print(type(self.image_np_modified[0,0]))
        if self.brightness_check.enable_val.get()==1:
            self.image_np_modified = self.image_np_modified.astype(int)
            # if self.brightness_check.slider.get()<0:
            k=self.brightness_check.slider.get()
            self.image_np_modified = np.add(self.image_np_modified, k)
            # if self.brightness_check.slider.get() >= 0:
            #     self.image_np_modified += self.brightness_check.slider.get()
            self.image_np_modified = np.clip(self.image_np_modified,0,255)
            self.image_np_modified = self.image_np_modified.astype(np.uint8)

    def pixelate_image(self):
        if self.pixelate_val.get() == 1:
            # print('entering pixelate')
            # print(self.image_np_modified)
            ratio = self.target_width / self.image_np_modified.shape[1]
            target_dim = (int(self.target_width), int(self.image_np_modified.shape[0] * ratio))
            dim_original = (self.image_np_modified.shape[1], self.image_np_modified.shape[0])
            dim = (int(self.x_px.value_val.get()), int(self.y_px.value_val.get()))
            self.image_np_modified = cv2.resize(self.image_np_modified, dim, interpolation=cv2.INTER_AREA)
            # print('pixelate image')
            # print(self.image_np_modified)
            self.image_np_modified_unexpanded = self.image_np_modified

            # convert image to range from 0 to tile number
            image_to_save = list()
            for r in self.image_np_modified_unexpanded:
                column_to_add = list()
                for c in r:
                    for i, x in enumerate(self.mapping_values):
                        if c<=x:
                            column_to_add.append(i)
                            break
                image_to_save.append(column_to_add)
            print('list', image_to_save)
            filename = "C:\\Users\\v_sam\\Desktop\list_save.pkl"
            with open(filename, 'wb') as f:
                pickle.dump(image_to_save, f)

            # print('dimensions')
            # print(dim_original)
            # print(target_dim)
            self.image_np_modified = cv2.resize(self.image_np_modified_unexpanded, target_dim, interpolation=cv2.INTER_NEAREST)

    def delete_grid(self):
        if len(self.lines) > 0:
            for obj in self.lines:
                self.image_panel.delete(obj)

    def draw_grid(self):
        self.delete_grid()
        x_delta = self.image_np_modified.shape[1] / self.image_np_modified_unexpanded.shape[1]
        y_delta = self.image_np_modified.shape[0] / self.image_np_modified_unexpanded.shape[0]
        x_offset=395-int(self.image_np_modified.shape[1]/2)
        y_offset=320-int(self.image_np_modified.shape[0]/2)
        if (self.grid_val.get()==1) and (self.image_np_modified_unexpanded.shape[1]<100):
            for x in range(self.image_np_modified_unexpanded.shape[1]+1,):
                self.lines.append(self.image_panel.create_line(int(5+x*x_delta+x_offset),5+y_offset,
                                                               int(5+x*x_delta+x_offset),int(5+self.image_np_modified.shape[0]+y_offset),
                                                               width=1, fill='black'))
                for y in range(self.image_np_modified_unexpanded.shape[0]+1):
                    self.lines.append(self.image_panel.create_line(5+x_offset, int(5+y*y_delta)+y_offset,
                                                              int(5 + self.image_np_modified.shape[1])+x_offset,int(5+y*y_delta)+y_offset,
                                                                   width=1, fill='black'))
        else:
            self.delete_grid()

    def draw_histogram(self):
        # self.ax.cla()
        # hist_full = cv2.calcHist(self.image_np_modified_unexpanded, [0], None, [256], [0, 256])
        # self.hist_chart.set_ydata(hist_full)
        # self.fig.canvas.draw()
        pass

    def mapping_imageX(self):
        # Update list that stores slider values (note: this is linked to sliders so cannot delete first)
        for x,i in enumerate(self.mapping_object_list):
            self.mapping_values[x] =i.slider.get()
            # print('getting value:', i.slider.get())
        # print(self.mapping_values)

        # Make sure sliders are not higher than their predecessor
        for x,i in enumerate(self.mapping_object_list):
            if x>0:
                i.label.config(text='{:03d} ... '.format(self.mapping_values[x-1]+1))
                if self.mapping_values[x]<self.mapping_values[x-1]+1:
                    self.mapping_values[x] = self.mapping_values[x-1]+2
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
            # print('Analysing array shapes...')
            # print(self.image_np_modified.shape)
            # print(self.image_np_modified_BGR[0].shape)
            # print('-----------------------------')
            for x,i in enumerate(logic_map):
                self.image_np_modified[i] = int(x*255/len(self.mapping_values))
                # print(int(x*255/len(self.mapping_values)))
                # print(i)
                # Temp work around for not defining last color in pallete (color without slider)
                # print('Length of logic map:', len(logic_map))
                if x<len(logic_map)-1:
                    # print('1st color array',self.image_np_modified_BGR[0])
                    self.image_np_modified_BGR[0][i] = int(self.mapping_object_list[x].button_color_dec[0])
                    self.image_np_modified_BGR[1][i] = int(self.mapping_object_list[x].button_color_dec[1])
                    self.image_np_modified_BGR[2][i] = int(self.mapping_object_list[x].button_color_dec[2])
                    self.image_np_modified_BGR = self.image_np_modified_BGR.astype(np.uint8)
                    # print('new BGR color maps')
                    # print(self.image_np_modified_BGR)
                    # print('-----------------------------')

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
                # print('Remapping values:', self.mapping_values)
                for x, i in enumerate(logic_map):
                    self.image_np_modified_unexpanded[i] = int(x * 255 / len(self.mapping_values))

        # print(self.image_np_modified_unexpanded)
        for r in self.image_np_modified_unexpanded:
            for c in r:
                if c in palette:
                    palette[c] += 1
                if not(c in palette):
                    palette.update({c:1})

        print('pallette:',palette)

    def update_color_pickers(self):
        for x, i in enumerate(self.mapping_object_list):
            i.button.configure(bg = i.button_color)

    def image_update(self):
        # self.image_panel.itemconfigure(self.imge, image=ImageTk.PhotoImage(Image.fromarray(self.image_np_modified)))
        # self.imageTk=ImageTk.PhotoImage(Image.fromarray(self.image_np_modified))
        # print('BGR image array shape:', self.image_np_modified_BGR.shape)
        image_to_show = np.dstack((self.image_np_modified_BGR[0],
                                  self.image_np_modified_BGR[1],
                                  self.image_np_modified_BGR[2]))
        # print('modified BGR image array shape:', image_to_show.shape)
        if self.mapping_val.get() == 1:
            self.imageTk = ImageTk.PhotoImage(Image.fromarray(image_to_show))
            self.image_panel.itemconfigure(self.imge, image=self.imageTk)
        else:
            self.imageTk = ImageTk.PhotoImage(Image.fromarray(self.image_np_modified))
            self.image_panel.itemconfigure(self.imge, image=self.imageTk)

    def update_all(self):
        print('entering update all loop')
        self.image_np_modified = self.load_master()
        # Update mapping values
        self.update_mapping_values()
        # If the brightness and contrast checkbutton is on, then modify the contrast and brightness
        self.modify_con_bri()
        # If the pixelate button is on, then modify the resolution
        self.pixelate_image()
        # Update color of all color picker buttons
        self.update_color_pickers()
        # If the mapping button is on, modify the mapping
        self.mapping_imageX()
        self.get_palette()
        # Update the image
        self.image_update()
        self.draw_grid()
        # self.draw_histogram()
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
