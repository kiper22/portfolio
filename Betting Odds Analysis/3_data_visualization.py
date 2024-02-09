from tkinter import *
import tkinter as tk
import tkinter as ttk
from tkinter import filedialog
import ttkbootstrap as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import re
import random
import datetime

class ViewData:
    def __init__(self, root):
        self.root = root
        self.root.title("View Data")
        self.root.minsize(890, 520)
        self.root.state('zoomed')
        self.data = pd.read_csv('2024-01-26-filled.csv')
        self.create_widgets()
        self.history = []
        
    def create_widgets(self):
        # constants:
        px = 5 # padx
        py = 5 # pady
        w = 500 # width
        h = 500 # height
        
        # mainframes, left and right
        self.left_frame = tk.Frame(root, width=w, bg="grey")  
        self.left_frame.place(x=10, y=10)
        self.right_frame = tk.Frame(root, width=w+2*px, bg='grey') 
        self.right_frame.place(x=w, y=-50)
        
        # in left frame:
        self.left_frame_load_data_button = tk.Button(self.left_frame, text="Load CSV", command=self.select_file)
        self.left_frame_load_data_button.grid(row=0, column=0, sticky=NSEW)
        
        self.left_frame_ligue_frame = tk.LabelFrame(self.left_frame, text="Wybierz Ligi")
        self.left_frame_ligue_frame.grid(row=1, column=0, padx=px, pady=py)
        self.create_ligues_checkbox()
        
        self.left_frame_bets_type_frame = tk.LabelFrame(self.left_frame, text='Rodzaje zakładów')
        self.left_frame_bets_type_frame.grid(row=2, column=0, padx=px, pady=py)
        self.create_bets_type_checkbox()
        
        self.left_frame_intervals_frame = tk.LabelFrame(self.left_frame, text="Wybierz zakres zakładów i podziałkę")
        self.left_frame_intervals_frame.grid(row=3, column=0, padx=px, pady=py)
        self.create_intervals()
        
        self.left_frame_chart_options = tk.LabelFrame(self.left_frame, text = "Wybierz opcje rysowania wykresów")
        self.left_frame_chart_options.grid(row=4, column=0, padx=px, pady=py)
        self.create_chart_options()
        
        self.left_frame_propability_chart = tk.Button(self.left_frame, text="Propab. chart", command=self.draw_chart)
        self.left_frame_propability_chart.grid(row=5, column=0, padx=px, pady=py, sticky=NSEW)
        
        self.left_frame_failure_list = tk.Button(self.left_frame, text="Failure list", command=self.list_of_failures)
        self.left_frame_failure_list.grid(row=6, column=0, padx=px, pady=py, sticky=NSEW)

    def select_file(self):
        self.data_path = filedialog.askopenfile()
        self.data = pd.read_csv(self.data_path)
        self.create_widgets()
    
    def create_ligues_checkbox(self):
        try:
            ligues = self.data['Liga'].unique()
            self.checkbox_ligues_vars = {ligue: IntVar() for ligue in ligues}
            self.ligue_checkboxes = {ligue: Checkbutton(self.left_frame_ligue_frame, text=ligue, variable=self.checkbox_ligues_vars[ligue]) for ligue in ligues}

            for checkbox in self.ligue_checkboxes.values():
                checkbox.select()
                    
            for idx, (ligue, checkbox) in enumerate(self.ligue_checkboxes.items()):
                row, col = divmod(idx, 2)
                checkbox.grid(row=row, column=col, sticky=W)
        except:
            print("RaiseError invalid file!")
            
    def on_checkbox_change(self):
        selected_ligues = [ligue for ligue, var in self.checkbox_ligues_vars.items() if var.get() == 1]
        return selected_ligues   
    
    def create_bets_type_checkbox(self):
        bets_types = ['1', '0', '2', '10', '02', '12']
        self.checkbox_bets_type_vars = {t: IntVar() for t in bets_types}
        self.bets_type_checkboxes = {t: Checkbutton(self.left_frame_bets_type_frame, text=t, variable=self.checkbox_bets_type_vars[t]) for t in bets_types}
        
        for checkbox in self.bets_type_checkboxes.values():
            checkbox.select()
        
        for idx, (bet, checkbox) in enumerate(self.bets_type_checkboxes.items()):
            row, col = divmod(idx, 2)
            checkbox.grid(row=row, column=col, sticky=W)
        
    def on_bets_checkbox_change(self):
        selected_bets = [ligue for ligue, var in self.checkbox_bets_type_vars.items() if var.get() == 1]
        return selected_bets
     
    def create_intervals(self):
        self.left_frame_intervals_frame.rowconfigure((0, 1, 2), weight=1)
        self.left_frame_intervals_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.interval_entry_min_var = tk.StringVar(value="1.0")
        self.interval_entry_max_var = tk.StringVar(value="2.0")
        self.intervals_number_var = tk.StringVar(value="10")
        vcmd = (self.left_frame_intervals_frame.register(self.intervals_callback), '%P')
        
        ttk.Label(self.left_frame_intervals_frame, text="Min:").grid(row=0, column=0, padx=5, pady=5)
        self.left_frame_interval_entry_min = ttk.Entry(self.left_frame_intervals_frame, validatecommand=vcmd, textvariable=self.interval_entry_min_var)
        self.left_frame_interval_entry_min.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.left_frame_intervals_frame, text="Max:").grid(row=0, column=2, padx=5, pady=5)
        self.left_frame_interval_entry_max = ttk.Entry(self.left_frame_intervals_frame, validatecommand=vcmd, textvariable=self.interval_entry_max_var)
        self.left_frame_interval_entry_max.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.left_frame_intervals_frame, text="Number of Intervals:").grid(row=1, column=0, padx=5, pady=5)
        self.left_frame_intervals_number = ttk.Entry(self.left_frame_intervals_frame, validatecommand=vcmd, textvariable=self.intervals_number_var)
        self.left_frame_intervals_number.grid(row=1, column=1, padx=5, pady=5, columnspan=3)
    
    def intervals_callback(self, P):
        if re.match(r'^[0-9]*\.?[0-9]*$', P) or P == "":
            return True
        else:
            return False
        
    def return_intervals_values(self):
        try:
            min_val = float(self.interval_entry_min_var.get())
            max_val = float(self.interval_entry_max_var.get())
            num_val = int(self.intervals_number_var.get())
            return(min_val, max_val, num_val)
        except ValueError:
            return(0, 0, 0)
    
    def create_chart_options(self):
        self.checkbox_chart_normal_var = tk.BooleanVar()
        self.checkbox_chart_normal = tk.Checkbutton(self.left_frame_chart_options, text = "Normalny wykres [N]", variable=self.checkbox_chart_normal_var)
        self.checkbox_chart_normal.grid(row=0, column=0)
        self.checkbox_chart_normal.select()
        self.checkbox_chart_smooth_var = tk.BooleanVar()
        self.checkbox_chart_smooth = tk.Checkbutton(self.left_frame_chart_options, text = "Wygładzany wykres [S]", variable=self.checkbox_chart_smooth_var)
        self.checkbox_chart_smooth.grid(row=1, column=0)
        self.checkbox_chart_smooth.select()
        self.checkbox_chart_history_var = tk.BooleanVar()
        self.checkbox_chart_history = tk.Checkbutton(self.left_frame_chart_options, text="Zapamiętaj poprzedni wykres", variable=self.checkbox_chart_history_var)
        self.checkbox_chart_history.grid(row=2, column=0)
    
    def draw_chart(self):
        fulfilled_condition, unfulfilled_condition, midpoints = self.calculate_wins_and_loses()
        profitability = self.calculate_profitability(fulfilled_condition, unfulfilled_condition, midpoints)

        fig = Figure(figsize=(14, 6), dpi=100)
        plot = fig.add_subplot(111)
        
        # get color and calculate values for history
        col = self.get_random_color()
        ligues = self.on_checkbox_change()
        ligues = [l.replace('1-', '') for l in ligues]
        ligues = [l[:2] if '-' not in l else f"{l.split('-')[0][:2]}-{l.split('-')[1][:2]}" for l in ligues]
        result_ligues_string = ', '.join(ligues)
        bets = self.on_bets_checkbox_change()
        result_bets = ', '.join(bets)
        
        if not self.checkbox_chart_history_var.get():
            self.history.clear()
        else:
            for i in range(0, len(self.history), 4):
                plot.plot(self.history[i], self.history[i+1], label=f'{self.history[i+2]}', color=self.history[i+3])
                plot.scatter(self.history[i], self.history[i+1], color=self.history[i+3], marker='o')
            
        if self.checkbox_chart_normal_var.get():
            self.history.append(midpoints)
            self.history.append(profitability)
            self.history.append(f'N::{result_ligues_string}::{result_bets}')
            self.history.append(col)
            
            for i in range(len(self.history)-4, len(self.history), 4):
                plot.plot(self.history[i], self.history[i+1], label=f'{self.history[i+2]}', color=self.history[i+3])
                plot.scatter(self.history[i], self.history[i+1], color=self.history[i+3], marker='o')
        
        if self.checkbox_chart_smooth_var.get():
            combined_matches = zip(fulfilled_condition, unfulfilled_condition)
            matches = [x+y for x, y in combined_matches]
            smooth_profitability = self.calculate_smooth_profitability(profitability, matches)
            
            col = self.get_random_color()
            
            self.history.append(midpoints)
            self.history.append(smooth_profitability)
            self.history.append(f'S::{result_ligues_string}::{result_bets}')
            self.history.append(col)
            
            plot.plot(midpoints, smooth_profitability, label=self.history[-2], color=col)
            plot.scatter(midpoints, smooth_profitability, color=col, marker='o')

        plot.axhline(0, color='orange', linestyle='--')

        plot.set_xlabel('Midpoints')
        plot.set_ylabel('Profitability')
        plot.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.draw()
        self.chart_info(fulfilled_condition, unfulfilled_condition, profitability, midpoints)
        
        for i in range(0, len(self.history), 5):
            pass
        
    def chart_info(self, fulfilled_condition, unfulfilled_condition, profitability, midpoints):
        self.tree_frame = tk.Frame(self.right_frame)
        self.tree_frame.grid(row=1, column=0)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Interval", "Profitability", "Fulfilled Conditions", "Unfulfilled Conditions", "Matches", "Propability"))
        self.tree['displaycolumns'] = (0, 1, 2, 3, 4)

        self.tree.heading("#0", text="Interval", anchor=CENTER)
        self.tree.heading("#1", text="Profitability", anchor=CENTER)
        self.tree.heading("#2", text="Fulfilled Conditions", anchor=CENTER)
        self.tree.heading("#3", text="Unfulfilled Conditions", anchor=CENTER)
        self.tree.heading("#4", text="Matches", anchor=CENTER)
        self.tree.heading('#5', text="Propability", anchor=CENTER)

        for i, midpoint in enumerate(midpoints):
            interval_str = f"{round(midpoints[i]-self.half_interval, 2)} - {round(midpoints[i]+self.half_interval, 2)}"
            matches = fulfilled_condition[i] + unfulfilled_condition[i]
            propability = round(fulfilled_condition[i] / matches * 100, 2) if matches != 0 else 0.0
            self.tree.insert("", index='end',text=interval_str, values=(profitability[i], fulfilled_condition[i], unfulfilled_condition[i], matches, f'{propability}%'))

        self.tree.column('#0', width=100, stretch=False, anchor=CENTER)
        self.tree.column('#1', width=100, stretch=False, anchor=CENTER)
        self.tree.column('#2', width=150, stretch=False, anchor=CENTER)
        self.tree.column('#3', width=150, stretch=False, anchor=CENTER)
        self.tree.column('#4', width=100, stretch=False, anchor=CENTER)
        self.tree.column('#5', width=100, stretch=False, anchor=CENTER)
        
        self.tree.grid(row=1, column=0)
    
    def calculate_wins_and_loses(self):
        success = []
        failure = []
        self.failed_rows = []
        selected_ligues = self.on_checkbox_change()
        selected_bets = self.on_bets_checkbox_change()        
        
        for idx, row in self.data.iterrows():
            if row["Liga"] in selected_ligues:
                for col in selected_bets:
                    if col in self.data.columns:
                        try:
                            win = int(row["Wygrany"])
                        except:
                            pass
                        
                        if str(win) in col:
                            success.append(row[col])
                        else:
                            failure.append(row[col])
                            self.failed_rows.append(row)
        
        min_val, max_val, num_val = self.return_intervals_values()
        
        intervals = np.linspace(min_val, max_val, num_val+1)
        self.half_interval = (max_val - min_val) / (2 * num_val)
        midpoints = (intervals[1:] + intervals[:-1])/2

        fulfilled_condition = [0] * (len(intervals) - 1)
        unfulfilled_condition = [0] * (len(intervals) - 1)
        
        for s in success:
            for i in range(len(intervals)-1):
                if intervals[i] <= s < intervals[i + 1]:
                    fulfilled_condition[i] += 1

        for f in failure:
            for i in range(len(intervals)-1):
                if intervals[i] <= f < intervals[i + 1]:
                    unfulfilled_condition[i] += 1
        
        
        return fulfilled_condition, unfulfilled_condition, midpoints
    
    def calculate_profitability(self, fulfilled, unfulfilled, midpoints):
        combined_matches = zip(fulfilled, unfulfilled)
        matches = [x+y for x, y in combined_matches]
        
        profitability = [0] * len(fulfilled)
        
        for idx, mid in enumerate(midpoints):
            try:
                profitability[idx] = fulfilled[idx] / (fulfilled[idx] + unfulfilled[idx]) * mid - 1
                profitability[idx] = round(profitability[idx], 3)
            except:
                pass
        
        return profitability

    def calculate_smooth_profitability(self, profitability, matches):
        smooth = [0] * len(profitability)
        for idx, mid in enumerate(profitability):
            try:
                if idx == 0:
                    smooth[idx] = (2*profitability[idx]*matches[idx] + profitability[idx+1]*matches[idx+1]) / (2*matches[idx] + matches[idx+1])
                elif idx == len(profitability) - 1:
                    smooth[idx] = (profitability[idx-1]*matches[idx-1] + 2*profitability[idx]*matches[idx]) / (matches[idx-1] + 2*matches[idx])
                else:
                    smooth[idx] = (profitability[idx-1]*matches[idx-1] + 2 * profitability[idx]*matches[idx] + profitability[idx+1]*matches[idx+1]) / (matches[idx-1] + 2*matches[idx] + matches[idx+1])
            except:
                pass
        return smooth

    def list_of_failures(self):
        selected_ligues = self.on_checkbox_change()
        selected_bets = self.on_bets_checkbox_change()
        min_val, max_val, _ = self.return_intervals_values()

        filtered_rows = []

        for idx, row in self.data.iterrows():
            if row["Liga"] in selected_ligues:
                row_append = False
                for bet in selected_bets:
                    try:
                        if (min_val <= float(row[bet]) <= max_val):
                            if str(int(row["Wygrany"])) not in str(bet):
                                row_append = True
                    except ValueError:
                        pass
                if row_append:
                    filtered_rows.append(row)

        if not filtered_rows:
            return

        columns = self.data.columns.tolist()
        data_dict = {col: [] for col in columns}

        for row in filtered_rows:
            for col, val in zip(columns, row):
                data_dict[col].append(val)

        data = pd.DataFrame(data_dict)

        top = ttk.Toplevel(self.root)
        top.title("List of Failures")

        tree = ttk.Treeview(top, columns=columns, show="headings", selectmode='none')
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(tree, c, False))
            tree.column(col, width=100, anchor="center")

        unique_ligues = self.data['Liga'].unique()
        for i, row in data.iterrows():
            values = row.tolist()
            tree.insert("", "end", values=values)

            liga_value = row['Liga']
            background_color = self.get_random_color()
            tree.tag_configure(liga_value, background=background_color)
            tree.item(tree.get_children()[-1], tags=(liga_value,))

        tree.pack(expand=YES, fill=BOTH)

    def sort_treeview(self, tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        data.sort(reverse=reverse)
        for i, item in enumerate(data):
            tree.move(item[1], "", i)

        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))

    def get_random_color(self):
        min = 64 # min brightness
        max = 256-min/2 # max brightness
        color = "#{:02x}{:02x}{:02x}".format(random.randint(min, max), random.randint(min, max), random.randint(min, max))
        return color
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ViewData(root)
    root.mainloop()