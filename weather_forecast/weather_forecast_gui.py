__author__ = 'sdaniels'

from tkinter import *
from tkinter import ttk

from weather_forecast import WeatherForecast

class WeatherForecastGUI(Tk):
    # GUI Window title
    WINDOW_TITLE = "Weather Forecaster"

    # widget text (label, checkboxes and buttons)
    LABEL_TEXT = 'Enter one of more location(s)\nMulitple locations are pipe delimited. ' \
                 '(Example: Ann Arbor, MI; London; 48198 and 49221|Springfield)'
    CHECKBOX_TEXT = ["Print to Console", "Output to HTML"]
    OK_BUTTON_TEXT = "Get Forecast"
    CANCEL_BUTTON_TEXT = "Cancel"

    # GUI Style
    BACKGROUND_COLOR = '#EBEBEB'

    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.title(self.WINDOW_TITLE)
        self.configure(background=self.BACKGROUND_COLOR)
        self.parent = parent
        self.initialize()

    def close(self):
        exit(0)

    def initialize(self):
        the_content = ttk.Frame(self)
        the_frame = ttk.Frame(the_content, borderwidth=3, relief="flat", height=400)

        # create the location input label
        entry_label = Label(the_frame,
                                    anchor="w",
                                    justify="left",
                                    bg=self.BACKGROUND_COLOR,
                                    text=self.LABEL_TEXT)

        # create location input
        self.entry = Entry(the_frame)

        # print_to_console/output_to_html_bool are BooleanVars initialized False
        self.print_to_console_bool = BooleanVar()
        self.output_to_html_bool = BooleanVar()
        self.print_to_console_bool.set(False)
        self.output_to_html_bool.set(False)

        # create the checkboxes for output types
        print_to_console_box = Checkbutton \
            (the_frame, bg=self.BACKGROUND_COLOR, text=self.CHECKBOX_TEXT[0], variable=self.print_to_console_bool,onvalue=1, offvalue=0, highlightcolor="blue")
        output_to_html_box = Checkbutton \
            (the_frame, bg=self.BACKGROUND_COLOR, text=self.CHECKBOX_TEXT[1], variable=self.output_to_html_bool,onvalue=1, offvalue=0)

        # create the ok buton
        ok_button = Button(the_frame, text=self.OK_BUTTON_TEXT, width=50, command=self.getForecast)

        # create the cancel button
        cancel_button = Button(the_frame, text=self.CANCEL_BUTTON_TEXT, width=50, command=self.close)

        # build the gui
        the_content.grid(column=0, row=0)
        the_frame.grid(column=0, row=0, columnspan=2, rowspan=2)
        entry_label.grid(column=0, columnspan=2,row=1)
        self.entry.grid(column=0, columnspan=2, row=2, sticky='EW')
        print_to_console_box.grid(column=0, columnspan=2, row=3)
        output_to_html_box.grid(column=0, columnspan=2, row=4)
        ok_button.grid(column=0, row=6, sticky='W')
        cancel_button.grid(column=1, row=6, sticky='W')


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

        exit(0)

if __name__ == '__main__':
    app = WeatherForecastGUI(None)
    app.mainloop()