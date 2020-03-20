#! /usr/bin/env python
#  -*- coding: utf-8 -*-
import os
import win32api

from gui.menubar import Menubar
from gui.utils.helper_methods import set_training_path, set_test_path, set_path, CROSS_WINDOWS_SETTINGS
from gui.widgets_configurations.helper_methods import set_copyright_configuration, set_logo_configuration, \
    set_button_configuration
from utils.shared.helper_methods import is_valid_directory
from tkinter import END

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


class NewModel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.menubar = Menubar(controller)
        self.controller.option_add('*tearOff', 'FALSE')  # Disables ability to tear menu bar into own window
        system_logo = CROSS_WINDOWS_SETTINGS.get('LOGO')
        photo_location = os.path.join(system_logo)
        global logo_img
        logo_img = tk.PhotoImage(file=photo_location)

        self.controller.geometry("700x550")
        self.controller.minsize(700, 550)
        self.controller.maxsize(700, 550)
        self.controller.resizable(1, 1)
        self.controller.title("Anomaly Detection Classifier")
        self.controller.configure(background="#eeeeee")

        self.logo_png = tk.Button(self)
        self.logo_png.place(relx=0.28, rely=0.029, height=172, width=300)
        set_logo_configuration(self.logo_png, image=logo_img)

        self.instructions = tk.Label(self)
        self.instructions.place(relx=0.005, rely=0.3, height=32, width=635)
        self.instructions.configure(
            text='''Please insert 'Mobilicom Ltd' simulated data / ADS-B dataset input files.''')

        self.training_label = tk.Label(self)
        self.training_label.place(relx=0.005, rely=0.4, height=32, width=146)
        self.training_label.configure(text='''Training directory''')

        self.training_input = tk.Entry(self)
        self.training_input.place(relx=0.195, rely=0.4, height=25, relwidth=0.624)

        self.training_btn = tk.Button(self, command=self.set_input_path)
        self.training_btn.place(relx=0.833, rely=0.4, height=25, width=60)
        set_button_configuration(self.training_btn, text='''Browse''')

        self.test_label = tk.Label(self)
        self.test_label.place(relx=0.005, rely=0.5, height=32, width=146)
        self.test_label.configure(text='''Test directory''')

        self.test_input = tk.Entry(self)
        self.test_input.place(relx=0.195, rely=0.5, height=25, relwidth=0.624)

        self.test_btn = tk.Button(self, command=self.set_test_path)
        self.test_btn.place(relx=0.833, rely=0.5, height=25, width=60)
        set_button_configuration(self.test_btn, text='''Browse''')

        self.results_label = tk.Label(self)
        self.results_label.place(relx=0.005, rely=0.6, height=32, width=146)
        self.results_label.configure(text='''Results directory''')

        self.results_input = tk.Entry(self)
        self.results_input.place(relx=0.195, rely=0.6, height=25, relwidth=0.624)

        self.results_btn = tk.Button(self, command=self.set_results_path)
        self.results_btn.place(relx=0.833, rely=0.6, height=25, width=60)
        set_button_configuration(self.results_btn, text='''Browse''')

        self.next_button = tk.Button(self, command=self.next_window)
        self.next_button.place(relx=0.859, rely=0.839, height=25, width=81)
        set_button_configuration(self.next_button, text='''Next''')

        self.back_button = tk.Button(self, command=self.back_window)
        self.back_button.place(relx=0.08, rely=0.839, height=25, width=81)
        set_button_configuration(self.back_button, text='''Back''')

        self.copyright = tk.Label(self)
        self.copyright.place(relx=0, rely=0.958, height=25, width=750)
        set_copyright_configuration(self.copyright)

    def set_input_path(self):
        self.training_input.delete(0, END)
        path = set_path()
        self.training_input.insert(0, path)
        self.controller.set_new_model_training_input_path(path)

    def set_test_path(self):
        self.test_input.delete(0, END)
        path = set_path()
        self.test_input.insert(0, path)
        self.controller.set_new_model_test_input_path(path)

    def set_results_path(self):
        self.results_input.delete(0, END)
        path = set_path()
        self.results_input.insert(0, path)
        self.controller.set_new_model_results_input_path(path)

    def back_window(self):
        self.controller.set_new_model_running(False)
        self.controller.show_frame("MainWindow")

    def next_window(self):
        if not is_valid_directory(self.training_input.get()) or not is_valid_directory(
                self.test_input.get()) or not is_valid_directory(self.results_input.get()):
            win32api.MessageBox(0, 'At least one of your inputs is invalid!', 'Invalid inputs', 0x00001000)
        else:
            self.controller.set_new_model_running(True)
            self.set_features_columns_options()
            self.controller.reinitialize_frame("AlgorithmsWindow")

    def set_features_columns_options(self):
        self.controller.set_features_columns_options()
