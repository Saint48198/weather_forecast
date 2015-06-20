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
        self.grid_columnconfigure(0, weight=1)

        # create the location input label
        entry_label = tkinter.Label(self,
                                    anchor="w",
                                    justify="left",
                                    text='Enter one of more location(s)\nMulitple '
                                         'locations are pipe delimited. (Example: Ann Arbor, MI; London; '
                                           '48198 and 49221|Springfield)')
        # place the label on the grid
        entry_label.grid(column=0, columnspan=2,row=1)

        # create and place the location input
        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0, columnspan=2, row=2, sticky='EW')


        # print_to_console/output_to_html_bool are BooleanVars initialized False
        self.print_to_console_bool = tkinter.BooleanVar()
        self.output_to_html_bool = tkinter.BooleanVar()
        self.print_to_console_bool.set(False)
        self.output_to_html_bool.set(False)

        # create the checkboxes for output types
        print_to_console_box = tkinter.Checkbutton \
            (self, text="Print to Console", variable=self.print_to_console_bool,onvalue=1, offvalue=0)
        output_to_html_box = tkinter.Checkbutton \
            (self, text="Output to HTML", variable=self.output_to_html_bool,onvalue=1, offvalue=0)

        # place the checkboxes on the grid
        print_to_console_box.grid(column=0, columnspan=2, row=3)
        output_to_html_box.grid(column=0, columnspan=2, row=4)

        # create and place the ok buton on the grid
        ok_button = tkinter.Button(self, text="Get Forecast", width=50, command=self.getForecast)
        ok_button.grid(column=0, row=6, sticky='W')

        # create and place the cancel button on the grid
        cancel_button = tkinter.Button(self, text="Cancel", width=50, command=self.close)
        cancel_button.grid(column=1, row=6, sticky='W')

        self.grid_columnconfigure(0,weight=1)


    def getForecast(self):
        a_location = WeatherForecast(self.entry.get())
        a_location.get_weather_forecast()

        # only show the selected report output type
        if self.print_to_console_bool.get():
            a_location.print_to_console();

        if self.output_to_html_bool.get():
            a_location.output_to_html();

        if (self.print_to_console_bool.get() == 0) and (self.output_to_html_bool.get() == 0):
            print('No report selected!')

if __name__ == '__main__':
    app = WeatherForecastGUI(None)
    app.title("Weather Forecaster")
    app.mainloop()