""" Jaromir-hub146 """


import tkinter as tk
import numpy as np
from tkinter import Tk, Label, Button, ttk, IntVar, Checkbutton, Radiobutton, Entry, Toplevel, END, filedialog, \
    messagebox
import pathlib
import pandas as pd
from compare_rank import run_compare_1, run_compare_2
import matplotlib.pyplot as plt
import csv

class App:

    def __init__(self, master: Tk):
        self.master = master
        self.main_dict = None
        self.weights = None
        self.param_names = None
        self.uta_data = None
        self.max_min = None

        # main window
        w, h = 800, 600
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.title('GUI - Porównanie rankingów wykorzystanych metod')


        def _runcompare_1():
            run_compare_1(self.main_dict, self.weights, self.max_min, self.uta_data['UTA_DATA'])

        def _runcompare_2():
            run_compare_2(self.main_dict, self.weights, self.max_min, self.uta_data['UTA_DATA'])

        def button2_hit():
            top = Toplevel()
            top.geometry('%dx%d+%d+%d' % (w, h, x, y))
            top.pack_propagate(False)
            top.resizable(False, False)

            # treeview
            frame = tk.LabelFrame(top, text="Dane z pliku")
            frame.place(height=380, width=800)

            # frame open/load file dialog
            file_frame = tk.LabelFrame(top, text="Załadowany plik")
            file_frame.place(height=200, width=800, rely=0.65, relx=0)

            t_b1 = Button(file_frame, text="Wyszukaj", command=lambda: file_dialog())
            t_b1.place(rely=0.65, relx=0.5)

            t_b2 = Button(file_frame, text="Wczytaj", command=lambda: load_excel())
            t_b2.place(rely=0.65, relx=0.3)

            t_lab = ttk.Label(file_frame, text="Nie załadowano żadnego pliku")
            t_lab.place(rely=0, relx=0)

            # treeview widget
            t_tv1 = ttk.Treeview(frame)
            t_tv1.place(relheight=1, relwidth=1)
            # treeview scrolls
            t_ts_x = tk.Scrollbar(frame, orient="horizontal", command=t_tv1.xview)
            t_ts_y = tk.Scrollbar(frame, orient="vertical", command=t_tv1.yview)

            t_tv1.configure(xscrollcommand=t_ts_x.set, yscrollcommand=t_ts_y.set)
            t_ts_x.pack(side="bottom", fill="x")
            t_ts_y.pack(side="right", fill="y")

            # functions to laod file
            def file_dialog():
                init_dir = pathlib.Path().resolve()
                file_name = filedialog.askopenfilename(initialdir=init_dir, title="Wybierz jakiś plik",
                                                       filetypes=(('CSV files', "*.csv"), ("xlsx files", "*.xlsx"),
                                                                  ("All files", "*.*")))
                top.lift(master)
                t_lab["text"] = file_name
                return None

            def load_excel():
                file_path = t_lab["text"]
                try:
                    excel_file_name = r"{}".format(file_path)
                    self.File_name = excel_file_name
                    df = pd.read_csv(excel_file_name, delimiter=",", index_col=0, header=0)
                    rows = self._import_data_from_csv(excel_file_name)
                    rows = self._extract_only_data_to_consider(rows)
                    self._arrange_data(rows)

                except ValueError:
                    messagebox.showerror("Informacja", "Plik jest nieprawidłowy")
                    return None

                except FileNotFoundError:
                    messagebox.showerror("Informacja", f"Nie ma takiego pliku jak: {file_path}")
                    top.lift(master)
                    return None

                clear_win()

                t_tv1["column"] = list(df.columns)
                t_tv1["show"] = "headings"

                for column in t_tv1["columns"]:
                    t_tv1.heading(column, text=column)

                df_rows = df.to_numpy().tolist()

                for row in df_rows:
                    t_tv1.insert("", "end", values=row)

                return None

            def clear_win():
                t_tv1.delete(*t_tv1.get_children())

        b1 = Button(master, text='Compare method', command=_runcompare_1)
        b1.pack()

        b2 = Button(master, text='Compare with weights', command=_runcompare_2)
        b2.pack()

        b3 = Button(master, text='Wczytaj dane', command=button2_hit)
        b3.pack()

    def _import_data_from_csv(self, fname):
        rows = []
        with open(fname, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows

    def _get_mask(self, rows):
        for row in rows:
            if row[0] == "CONSIDER":
                mask = row[1:]
                break
        bool_mask = [True if cryt == "1" else False for cryt in mask]
        bool_mask = [True] + bool_mask
        return bool_mask

    def _extract_only_data_to_consider(self, rows):
        new_rows = []
        mask = self._get_mask(rows)
        for row in rows:
            new_row = []
            for nr, el in enumerate(row):
                if mask[nr] is True:
                    new_row.append(el)
            new_rows.append(new_row)
        return new_rows

    def _change_data_type(self, types, group):
        new_group = {}
        for key, vals in group.items():
            new_vals = []
            for nr in range(len(vals)):
                if types[nr] == "INT":
                    new_vals.append(float(vals[nr]))
                elif types[nr] == "BOOL":
                    if vals[nr] == "False":
                        new_vals.append(False)
                    if vals[nr] == "True":
                        new_vals.append(True)
            new_group.update({key: new_vals})
        return new_group

    def _arrange_data(self, rows):
        main_dict = {}
        A0 = {}
        A1 = {}
        weights = {}
        param_names = rows[0][1:]
        min_max = {}
        types = []
        uta_data = {}
        for row in rows[1:]:
            tag = row[0]
            vals = row[1:]
            if tag == "":
                continue
            if tag == "WEIGHTS":
                weights = list(map(float, vals))
            elif tag == "MAX MIN":
                min_max = list(map(int, vals))
            elif tag == "TYPE":
                types = vals
            elif tag == "UTA_DATA":
                uta_data.update({tag: list(map(int, vals))})
            elif "M" in tag:
                main_dict.update({tag: vals})
            elif "A0" in tag and "#" not in tag:
                A0.update({tag: vals})
            elif "A1" in tag and "#" not in tag:
                A1.update({tag: vals})

        main_dict = self._change_data_type(types, main_dict)
        if A0:
            A0 = self._change_data_type(types, A0)
            self.A0 = A0
        else:
            self.A0 = None
        if A1:
            A1 = self._change_data_type(types, A1)
            self.A1 = A1
        else:
            self.A1 = None

        self.main_dict = main_dict
        self.weights = weights
        self.param_names = param_names
        self.uta_data = uta_data
        self.max_min = min_max