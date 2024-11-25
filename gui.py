# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from methods import (
    northwest_corner_method,
    vogel_approximation_method,
    minimum_cost_method,
    stepping_stone_method,
    modi_method,
    calculate_total_cost
)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solucionador de Problemas de Transporte")
        self.method_var = tk.StringVar()
        self.num_supply_var = tk.IntVar(value=3)
        self.num_demand_var = tk.IntVar(value=3)
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), background='#AED6F1')
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.configure(bg='#F0F8FF')

    def create_widgets(self):
        methods = [
            "1.1 Método de la esquina noroeste (MEN)",
            "1.2 Método por aproximación de Vogel (MAV)",
            "1.3 Método del costo mínimo (MCM)",
            "1.4 Método del paso secuencial",
            "1.5 DIMO (método de distribución modificada)",
        ]

        ttk.Label(self, text="Seleccione el método:", background='#F0F8FF').grid(row=0, column=0, sticky="w")
        self.method_combo = ttk.Combobox(self, values=methods, textvariable=self.method_var, state="readonly", font=('Arial', 12))
        self.method_combo.grid(row=0, column=1)
        self.method_combo.current(0)

        ttk.Label(self, text="Número de proveedores:", background='#F0F8FF').grid(row=1, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.num_supply_var).grid(row=1, column=1)

        ttk.Label(self, text="Número de consumidores:", background='#F0F8FF').grid(row=2, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.num_demand_var).grid(row=2, column=1)

        pastel_button_style = ttk.Style()
        pastel_button_style.configure('Pastel.TButton', font=('Arial', 12), background='#A9DFBF', foreground='black')

        ttk.Button(self, text="Ingresar datos", command=self.input_data, style='Pastel.TButton').grid(row=3, column=0, columnspan=2, pady=5)

    def input_data(self):
        num_supply = self.num_supply_var.get()
        num_demand = self.num_demand_var.get()

        if num_supply <= 0 or num_demand <= 0:
            messagebox.showerror("Error", "El número de proveedores y consumidores debe ser mayor a cero.")
            return

        self.data_window = tk.Toplevel(self)
        self.data_window.title("Ingresar datos")
        self.data_window.configure(bg='#F0F8FF')

        self.cost_entries = []
        for i in range(num_supply):
            row_entries = []
            for j in range(num_demand):
                e = ttk.Entry(self.data_window, width=5, font=('Arial', 12))
                e.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                row_entries.append(e)
            self.cost_entries.append(row_entries)

        for j in range(num_demand):
            ttk.Label(self.data_window, text=f"D{j+1}", background='#F0F8FF', font=('Arial', 12)).grid(row=0, column=j + 1)
        for i in range(num_supply):
            ttk.Label(self.data_window, text=f"S{i+1}", background='#F0F8FF', font=('Arial', 12)).grid(row=i + 1, column=0)

        ttk.Label(self.data_window, text="Oferta", background='#F0F8FF', font=('Arial', 12)).grid(row=0, column=num_demand + 1)
        self.supply_entries = []
        for i in range(num_supply):
            e = ttk.Entry(self.data_window, width=5, font=('Arial', 12))
            e.grid(row=i + 1, column=num_demand + 1, padx=2, pady=2)
            self.supply_entries.append(e)

        ttk.Label(self.data_window, text="Demanda", background='#F0F8FF', font=('Arial', 12)).grid(row=num_supply + 1, column=0)
        self.demand_entries = []
        for j in range(num_demand):
            e = ttk.Entry(self.data_window, width=5, font=('Arial', 12))
            e.grid(row=num_supply + 1, column=j + 1, padx=2, pady=2)
            self.demand_entries.append(e)

        pastel_button_style = ttk.Style()
        pastel_button_style.configure('Pastel.TButton', font=('Arial', 12), background='#A9DFBF', foreground='black')

        ttk.Button(self.data_window, text="Resolver", command=self.solve_problem, style='Pastel.TButton').grid(
            row=num_supply + 2, column=0, columnspan=num_demand + 2, pady=5
        )

    def solve_problem(self):
        try:
            cost_matrix = [
                [float(self.cost_entries[i][j].get()) for j in range(len(self.cost_entries[0]))]
                for i in range(len(self.cost_entries))
            ]
            supply = [float(e.get()) for e in self.supply_entries]
            demand = [float(e.get()) for e in self.demand_entries]
        except ValueError:
            messagebox.showerror("Error", "Todos los valores deben ser numéricos.")
            return

        # Verificar si el problema está balanceado
        total_supply = sum(supply)
        total_demand = sum(demand)
        if total_supply != total_demand:
            messagebox.showerror("Error", "El problema no está balanceado. La oferta total y la demanda total deben ser iguales.")
            return

        method = self.method_var.get()
        if method.startswith("1.1"):
            steps = northwest_corner_method(cost_matrix, supply, demand)
        elif method.startswith("1.2"):
            steps = vogel_approximation_method(cost_matrix, supply, demand)
        elif method.startswith("1.3"):
            steps = minimum_cost_method(cost_matrix, supply, demand)
        elif method.startswith("1.4"):
            initial_steps = northwest_corner_method(cost_matrix, supply, demand)
            initial_allocations = initial_steps[-1]['allocations']
            optimization_steps = stepping_stone_method(initial_allocations, cost_matrix)
            steps = initial_steps + optimization_steps
        elif method.startswith("1.5"):
            initial_steps = northwest_corner_method(cost_matrix, supply, demand)
            initial_allocations = initial_steps[-1]['allocations']
            optimization_steps = modi_method(initial_allocations, cost_matrix)
            steps = initial_steps + optimization_steps
        else:
            messagebox.showerror("Error", "Método no reconocido.")
            return

        self.steps = steps
        self.current_step = 0
        self.cost_matrix = cost_matrix
        self.display_solution()

    def display_solution(self):
        self.solution_window = tk.Toplevel(self)
        self.solution_window.title("Solución")
        self.solution_window.configure(bg='#F0F8FF')

        self.step_label = tk.Label(self.solution_window, font=('Arial', 12), bg='#F0F8FF')
        self.step_label.pack()
        self.table_frame = tk.Frame(self.solution_window, bg='#F0F8FF')
        self.table_frame.pack()
        self.description_label = tk.Label(self.solution_window, font=('Arial', 12), bg='#F0F8FF')
        self.description_label.pack()
        navigation_frame = tk.Frame(self.solution_window, bg='#F0F8FF')
        navigation_frame.pack()

        pastel_button_style = ttk.Style()
        pastel_button_style.configure('Pastel.TButton', font=('Arial', 12), background='#AED6F1', foreground='black')

        prev_button = ttk.Button(navigation_frame, text="Anterior", command=self.previous_step, style='Pastel.TButton')
        prev_button.grid(row=0, column=0, padx=5, pady=5)
        next_button = ttk.Button(navigation_frame, text="Siguiente", command=self.next_step, style='Pastel.TButton')
        next_button.grid(row=0, column=1, padx=5, pady=5)

        self.update_solution_display()

    def update_solution_display(self):
        step = self.steps[self.current_step]
        allocations = step['allocations']

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        m = len(allocations)
        n = len(allocations[0])

        for i in range(m):
            for j in range(n):
                value = allocations[i][j]
                text = f"{value}\n({self.cost_matrix[i][j]})" if value != 0 else f"({self.cost_matrix[i][j]})"
                label = tk.Label(self.table_frame, text=text, width=8, height=4, borderwidth=1, relief="solid", font=('Arial', 12))
                label.grid(row=i+1, column=j+1)

        for j in range(n):
            header = tk.Label(self.table_frame, text=f"D{j+1}", width=8, borderwidth=1, relief="solid", bg="#D6EAF8", font=('Arial', 12))
            header.grid(row=0, column=j+1)
        for i in range(m):
            header = tk.Label(self.table_frame, text=f"S{i+1}", width=8, borderwidth=1, relief="solid", bg="#D6EAF8", font=('Arial', 12))
            header.grid(row=i+1, column=0)

        self.step_label.config(text=f"Paso {self.current_step + 1} de {len(self.steps)}")
        self.description_label.config(text=step['description'])

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_solution_display()
        else:
            total_cost = calculate_total_cost(self.steps[-1]['allocations'], self.cost_matrix)
            messagebox.showinfo("Costo Total", f"El costo total (Z) es: {total_cost}")

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_solution_display()
