# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from methods import (
    northwest_corner_method,
    vogel_approximation_method,
    minimum_cost_method,
    stepping_stone_method,
    modi_method,
)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solucionador de Problemas de Transporte")
        self.method_var = tk.StringVar()
        self.num_supply_var = tk.IntVar()
        self.num_demand_var = tk.IntVar()
        self.create_widgets()

    def create_widgets(self):
        methods = [
            "1.1 Método de la esquina noroeste (MEN)",
            "1.2 Método por aproximación de Vogel (MAV)",
            "1.3 Método del costo mínimo (MCM)",
            "1.4 Método del paso secuencial",
            "1.5 DIMO (método de distribución modificada)",
        ]

        ttk.Label(self, text="Seleccione el método:").grid(
            row=0, column=0, sticky="w")
        self.method_combo = ttk.Combobox(
            self, values=methods, textvariable=self.method_var)
        self.method_combo.grid(row=0, column=1)
        self.method_combo.current(0)

        ttk.Label(self, text="Número de proveedores:").grid(
            row=1, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.num_supply_var).grid(row=1, column=1)

        ttk.Label(self, text="Número de consumidores:").grid(
            row=2, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.num_demand_var).grid(row=2, column=1)

        ttk.Button(self, text="Ingresar datos", command=self.input_data).grid(
            row=3, column=0, columnspan=2)

    def input_data(self):
        num_supply = self.num_supply_var.get()
        num_demand = self.num_demand_var.get()

        if num_supply <= 0 or num_demand <= 0:
            messagebox.showerror(
                "Error", "El número de proveedores y consumidores debe ser mayor a cero.")
            return

        self.data_window = tk.Toplevel(self)
        self.data_window.title("Ingresar datos")

        self.cost_entries = []
        for i in range(num_supply):
            row_entries = []
            for j in range(num_demand):
                e = ttk.Entry(self.data_window, width=5)
                e.grid(row=i + 1, column=j + 1)
                row_entries.append(e)
            self.cost_entries.append(row_entries)

        for j in range(num_demand):
            ttk.Label(self.data_window, text=f"D{
                      j+1}").grid(row=0, column=j + 1)
        for i in range(num_supply):
            ttk.Label(self.data_window, text=f"S{
                      i+1}").grid(row=i + 1, column=0)

        ttk.Label(self.data_window, text="Oferta").grid(
            row=0, column=num_demand + 1)
        self.supply_entries = []
        for i in range(num_supply):
            e = ttk.Entry(self.data_window, width=5)
            e.grid(row=i + 1, column=num_demand + 1)
            self.supply_entries.append(e)

        ttk.Label(self.data_window, text="Demanda").grid(
            row=num_supply + 1, column=0)
        self.demand_entries = []
        for j in range(num_demand):
            e = ttk.Entry(self.data_window, width=5)
            e.grid(row=num_supply + 1, column=j + 1)
            self.demand_entries.append(e)

        ttk.Button(self.data_window, text="Resolver", command=self.solve_problem).grid(
            row=num_supply + 2, column=0, columnspan=num_demand + 2
        )

    def solve_problem(self):
        try:
            cost_matrix = [
                [float(self.cost_entries[i][j].get())
                 for j in range(len(self.cost_entries[0]))]
                for i in range(len(self.cost_entries))
            ]
            supply = [float(e.get()) for e in self.supply_entries]
            demand = [float(e.get()) for e in self.demand_entries]
        except ValueError:
            messagebox.showerror(
                "Error", "Todos los valores deben ser numéricos.")
            return

        # Verificar si el problema está balanceado
        total_supply = sum(supply)
        total_demand = sum(demand)
        if total_supply != total_demand:
            messagebox.showerror(
                "Error", "El problema no está balanceado. La oferta total y la demanda total deben ser iguales.")
            return

        method = self.method_var.get()
        if method.startswith("1.1"):
            steps = northwest_corner_method(cost_matrix, supply, demand)
        elif method.startswith("1.2"):
            steps = vogel_approximation_method(cost_matrix, supply, demand)
        elif method.startswith("1.3"):
            steps = minimum_cost_method(cost_matrix, supply, demand)
        elif method.startswith("1.4"):
            # Obtener solución inicial
            initial_steps = northwest_corner_method(
                cost_matrix, supply, demand)
            initial_allocations = initial_steps[-1]['allocations']
            # Optimizar con Método del Paso Secuencial
            steps = initial_steps + \
                stepping_stone_method(initial_allocations, cost_matrix)
        elif method.startswith("1.5"):
            # Obtener solución inicial
            initial_steps = northwest_corner_method(
                cost_matrix, supply, demand)
            initial_allocations = initial_steps[-1]['allocations']
            # Optimizar con Método MODI
            steps = initial_steps + \
                modi_method(initial_allocations, cost_matrix)
        else:
            messagebox.showerror("Error", "Método no reconocido.")
            return

        self.solution_window = tk.Toplevel(self)
        self.solution_window.title("Solución")
        self.current_step = 0
        self.steps = steps
        self.display_step()

        ttk.Button(self.solution_window, text="Anterior",
                   command=self.previous_step).grid(row=1, column=0)
        ttk.Button(self.solution_window, text="Siguiente",
                   command=self.next_step).grid(row=1, column=1)

    def display_step(self):
        for widget in self.solution_window.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        step = self.steps[self.current_step]
        frame = tk.Frame(self.solution_window)
        frame.grid(row=0, column=0, columnspan=2)

        allocations = step["allocations"]
        for i in range(len(allocations)):
            for j in range(len(allocations[0])):
                value = allocations[i][j]
                text = str(value) if value != 0 else ""
                tk.Label(frame, text=text, width=5, borderwidth=1,
                         relief="solid").grid(row=i + 1, column=j + 1)

        for j in range(len(allocations[0])):
            tk.Label(frame, text=f"D{
                     j+1}", width=5, borderwidth=1, relief="solid").grid(row=0, column=j + 1)
        for i in range(len(allocations)):
            tk.Label(frame, text=f"S{
                     i+1}", width=5, borderwidth=1, relief="solid").grid(row=i + 1, column=0)

        tk.Label(self.solution_window, text=step["description"]).grid(
            row=2, column=0, columnspan=2)

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.display_step()

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.display_step()
