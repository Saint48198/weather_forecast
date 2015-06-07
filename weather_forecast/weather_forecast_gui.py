__author__ = 'sdaniels'

import tkinter
from tkinter import ttk

from weather_forecast import WeatherForecast

class WeatherForecastGUI:
    def __init__(self, parent):
        self.parent = parent
        self.createUI()

    def close(self):
        exit(0)

    def createUI(self):
        the_content = ttk.Frame(root)
        the_frame = ttk.Frame\
            (the_content, borderwidth=5, relief="sunken", width=500, height=200)

        location_label = ttk.Label(the_content, text="Enter location(s)")
        self.the_location = ttk.Entry(the_content)

        ok_button = ttk.Button(the_content, text="Get Forecast", command=self.getForecast)
        cancel_button = ttk.Button(the_content, text="Cancel", command=self.close)

        the_content.grid(column=0, row=0)
        the_frame.grid(column=0, row=0, columnspan=10, rowspan=5)
        location_label.grid(column=3, row=1, columnspan=2)
        self.the_location.grid(column=3, row=2, columnspan=2)
        ok_button.grid(column=3, row=4)
        cancel_button.grid(column=4, row=4)


    def getForecast(self):
        a_location = WeatherForecast(self.the_location.get())
        a_location.get_weather_forecast()

if __name__ == '__main__':
    root =  tkinter.Tk()
    app = WeatherForecastGUI(root)
    root.mainloop()