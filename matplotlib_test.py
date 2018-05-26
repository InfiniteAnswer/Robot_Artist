import matplotlib.pyplot as plt
import numpy as np

class make_figs():
    def __init__(self):
        self.fig_list = list()
        for i in range(3):
            self.fig_list.append(plt.figure(i))
            self.fig_list[i].ax = self.fig_list[i].add_axes([0.2+i/10,0.2,0.6,0.6])
        self.add_data()
        plt.show()
        plt.pause(1)

    def add_data(self):
        x = np.linspace(0, 10,10)
        y = x**2
        print(x,y)
        for i,obj in enumerate(self.fig_list):
            print(i)
            print(type(obj))
            print(obj.ax)
            obj.ax.plot(x,y)
            if i%2==1:
                print('removing')
                obj.ax.set_visible(False)

p = make_figs()

