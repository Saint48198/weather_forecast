__author__ = 'sdaniels'

import tkinter

from weather_forecast import WeatherForecast

class WeatherForecastGUI(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def close(self):
        exit(0)

    def initialize(self):
        self.grid()

        entry_label = tkinter.Label(self, anchor="w", text='Enter Location(s) (Example: Ann Arbor, MI; London; 48198 and etc.)')
        entry_label.grid(column=0,row=1)

        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0, columnspan=2, row=2,sticky='EW')

        ok_button = tkinter.Button(self, text="Get Forecast", command=self.getForecast)
        ok_button.grid(column=0,row=3)

        cancel_button = tkinter.Button(self, text="Cancel", command=self.close)
        cancel_button.grid(column=1,row=3)

        self.grid_columnconfigure(0,weight=1)


    def getForecast(self):
        a_location = WeatherForecast(self.entry.get())
        a_location.get_weather_forecast()

if __name__ == '__main__':
    app = WeatherForecastGUI(None)
    app.title("Weather Forecaster")
    app.mainloop()