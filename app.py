import tkinter as tk
from tkcalendar import DateEntry
from datetime import date, timedelta

import sjsu_parking_db_reader as db_reader

# create a class called CanvasCoords
class ParkingApplication:

    # define an init function
    def __init__(self, root):

        self.plot_type = None
        self.start_date_custom = None
        self.end_date_custom = None

        self.root = root
        self.selection_frame = None
        self.select_option_frame = None
        self.custom_date_frame = None

        self.db_reader = None

        # add a title to the window
        root.title("SJSU Parking Status Visualizer")

        # make a frame and stick it to the sides
        title = tk.Label(root, text="Select the parking graph to view", font=("Arial", 14), fg="black")

        self.selection_frame = tk.Frame(self.root)
        self.build_selection_frame()
        self.build_custom_date_frame()
        self.select_option_frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)
        self.custom_date_frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)

        show_plot_button = tk.Button(root, width=10, height=2, text="Show Plot", font=("Arial", 12), fg='blue', command=self.show_plot)

        title.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)
        self.selection_frame.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)
        show_plot_button.pack(side=tk.BOTTOM, anchor='s', padx=10, pady=10)

        self.db_reader = db_reader.ParkingDBReader()

    def build_selection_frame(self):
        self.plot_type = tk.StringVar()

        self.select_option_frame = tk.Frame(self.selection_frame)
        options = ["Today", "Week", "Month", "Full", "Custom"]
        for option in options:
            radio = tk.Radiobutton(self.select_option_frame, text=option, variable=self.plot_type, value=option, command=self.selection_changed)
            radio.pack(side=tk.TOP, anchor='nw', padx=5, pady=5)

        self.plot_type.set("Week")

    def build_custom_date_frame(self):
        self.custom_date_frame = tk.Frame(self.selection_frame)

        custom_start_date_frame = tk.Frame(self.custom_date_frame)
        start_date_label = tk.Label(custom_start_date_frame, text="Start Date: ")
        self.start_date_custom = DateEntry(custom_start_date_frame, width=12, date_pattern='mm/dd/yyyy')
        start_date_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.start_date_custom.pack(side=tk.LEFT, padx=5, pady=5)

        custom_end_date_frame = tk.Frame(self.custom_date_frame)
        end_date_label = tk.Label(custom_end_date_frame, text="End Date:   ")
        self.end_date_custom   = DateEntry(custom_end_date_frame, width=12, date_pattern='mm/dd/yyyy')
        end_date_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.end_date_custom.pack(side=tk.TOP, padx=5, pady=5)

        custom_start_date_frame.pack(side=tk.TOP, padx=10, pady=10)
        custom_end_date_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.start_date_custom.set_date(date.today() + timedelta(-7))
        self.end_date_custom.set_date(date.today() + timedelta(0))

        self.start_date_custom.config(state="disabled")
        self.end_date_custom.config(state="disabled")

    def selection_changed(self):
        option = self.plot_type.get()
        if (option == "Custom"):
            self.start_date_custom.config(state="normal")
            self.end_date_custom.config(state="normal")
        else:
            self.start_date_custom.config(state="disabled")
            self.end_date_custom.config(state="disabled")

    def select_plot(self, type):
        self.plot_type = type
        print(self.plot_type)

    def show_plot(self):
        plot_option = self.plot_type.get()
        if plot_option == "Custom":
            print(f"Show plot of type {plot_option} start date {self.start_date_custom.get_date()} end date {self.end_date_custom.get_date()}")
        else:
            print(f"Show plot of type {plot_option}")


root = tk.Tk()
root.geometry("400x350")
root.resizable(False, False)

# create a WidgetDisplay object with the Tk root object as an argument
ParkingApplication(root)

# call the mainloop method on the Tk root object
root.mainloop()
