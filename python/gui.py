from __future__ import print_function
from __future__ import division
import time
import numpy as np
from pyqtgraph.Qt import QtWidgets
import pyqtgraph as pg
from pyqtgraph.dockarea import *


class GUI:
    plot = []
    curve = []

    def __init__(self, width=800, height=450, title=''):
        # Create GUI window
        self.app = QtWidgets.QApplication([])
        self.win = QtWidgets.QMainWindow()
        self.win.resize(width, height)
        self.win.setWindowTitle(title)

        # Create vertical layout
        layout = QtWidgets.QVBoxLayout()

        # Add layout to main window
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.win.setCentralWidget(central_widget)

    def add_plot(self, title):
        # Create plot widget
        plot_widget = pg.PlotWidget()
        plot_widget.setTitle(title)

        # Add plot widget to layout
        layout = self.win.centralWidget().layout()
        layout.addWidget(plot_widget)

        # Add plot widget to list of plots
        self.plot.append(plot_widget)

        # Return plot widget
        return plot_widget
        

    def add_curve(self, plot_index, pen=(255, 255, 255)):
        # Create curve item
        curve_item = self.plot[plot_index].plot(pen=pen)

        # Add curve item to list of curves
        self.curve.append(curve_item)

        # Return curve item
        return curve_item


if __name__ == '__main__':
    # Example test gui
    import numpy as np
    N = 48
    gui = GUI(title='Test')
    # Sin plot
    sin_plot = gui.add_plot(title='Sin Plot')
    sin_curve = gui.add_curve(plot_index=0)
    x = np.linspace(0, 2*np.pi, N)
    y = np.sin(x)
    sin_curve.setData(x, y)
    sin_plot.move(0, 0)  # Move sin plot to top-left corner
    # Cos plot
    cos_plot = gui.add_plot(title='Cos Plot')
    cos_curve = gui.add_curve(plot_index=1)
    y = np.cos(x)
    cos_curve.setData(x, y)
    cos_plot.move(0, sin_plot.height())  # Move cos plot below sin plot
    gui.win.show()
    gui.app.exec_()
        