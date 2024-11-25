# methods.py

def northwest_corner_method(cost_matrix, supply, demand):
    steps = []
    allocations = [[0 for _ in demand] for _ in supply]
    i, j = 0, 0
    supply_copy = supply.copy()
    demand_copy = demand.copy()

    while i < len(supply) and j < len(demand):
        allocation = min(supply_copy[i], demand_copy[j])
        allocations[i][j] = allocation
        description = f"Asignar {allocation} unidades a la celda ({i+1},{j+1})"
        supply_copy[i] -= allocation
        demand_copy[j] -= allocation
        steps.append({'allocations': [row.copy() for row in allocations],
                      'description': description})

        if supply_copy[i] == 0 and i + 1 < len(supply):
            i += 1
        elif demand_copy[j] == 0 and j + 1 < len(demand):
            j += 1
        elif supply_copy[i] == 0 and demand_copy[j] == 0:
            i += 1
            j += 1
        else:
            break  # No se pueden hacer más asignaciones

    return steps

def vogel_approximation_method(cost_matrix, supply, demand):
    steps = []
    allocations = [[0 for _ in demand] for _ in supply]
    supply_copy = supply.copy()
    demand_copy = demand.copy()

    while sum(supply_copy) > 0 and sum(demand_copy) > 0:
        row_penalties = []
        for i in range(len(supply)):
            costs = [cost_matrix[i][j] for j in range(len(demand)) if demand_copy[j] > 0]
            if len(costs) >= 2:
                sorted_costs = sorted(costs)
                penalty = sorted_costs[1] - sorted_costs[0]
            elif len(costs) == 1:
                penalty = costs[0]
            else:
                penalty = None
            row_penalties.append(penalty)

        col_penalties = []
        for j in range(len(demand)):
            costs = [cost_matrix[i][j] for i in range(len(supply)) if supply_copy[i] > 0]
            if len(costs) >= 2:
                sorted_costs = sorted(costs)
                penalty = sorted_costs[1] - sorted_costs[0]
            elif len(costs) == 1:
                penalty = costs[0]
            else:
                penalty = None
            col_penalties.append(penalty)

        max_row_penalty = max([p for p in row_penalties if p is not None], default=None)
        max_col_penalty = max([p for p in col_penalties if p is not None], default=None)

        if max_row_penalty is None and max_col_penalty is None:
            break  # No se pueden hacer más asignaciones

        if (max_row_penalty or 0) >= (max_col_penalty or 0):
            i = row_penalties.index(max_row_penalty)
            costs = [(cost_matrix[i][j], j) for j in range(len(demand)) if demand_copy[j] > 0]
            min_cost, min_j = min(costs)
            allocation = min(supply_copy[i], demand_copy[min_j])
            allocations[i][min_j] = allocation
            description = f"Asignar {allocation} unidades a la celda ({i+1},{min_j+1})"
            supply_copy[i] -= allocation
            demand_copy[min_j] -= allocation
            steps.append({'allocations': [row.copy() for row in allocations],
                          'description': description})
        else:
            j = col_penalties.index(max_col_penalty)
            costs = [(cost_matrix[i][j], i) for i in range(len(supply)) if supply_copy[i] > 0]
            min_cost, min_i = min(costs)
            allocation = min(supply_copy[min_i], demand_copy[j])
            allocations[min_i][j] = allocation
            description = f"Asignar {allocation} unidades a la celda ({min_i+1},{j+1})"
            supply_copy[min_i] -= allocation
            demand_copy[j] -= allocation
            steps.append({'allocations': [row.copy() for row in allocations],
                          'description': description})

    return steps

def minimum_cost_method(cost_matrix, supply, demand):
    steps = []
    allocations = [[0 for _ in demand] for _ in supply]
    supply_copy = supply.copy()
    demand_copy = demand.copy()

    cost_positions = []
    for i in range(len(supply)):
        for j in range(len(demand)):
            cost_positions.append((cost_matrix[i][j], i, j))

    cost_positions.sort()
    allocation_made = True

    while allocation_made:
        allocation_made = False
        for cost, i, j in cost_positions:
            if supply_copy[i] > 0 and demand_copy[j] > 0:
                allocation = min(supply_copy[i], demand_copy[j])
                allocations[i][j] = allocation
                description = f"Asignar {allocation} unidades a la celda ({i+1},{j+1}) con costo {cost}"
                supply_copy[i] -= allocation
                demand_copy[j] -= allocation
                steps.append({'allocations': [row.copy() for row in allocations],
                              'description': description})
                allocation_made = True
                break  # Reiniciar el bucle para volver a verificar las posiciones de costo
        cost_positions = [cp for cp in cost_positions if supply_copy[cp[1]] > 0 and demand_copy[cp[2]] > 0]

    return steps

def stepping_stone_method(allocations, cost_matrix):
    steps = []
    total_cost = calculate_total_cost(allocations, cost_matrix)
    steps.append({'allocations': [row.copy() for row in allocations],
                  'description': f"Costo total inicial: {total_cost}"})

    while True:
        potentials = calculate_opportunity_costs(allocations, cost_matrix)
        max_reduction = 0
        best_path = None

        for (i, j), opportunity_cost in potentials.items():
            if opportunity_cost < max_reduction:
                max_reduction = opportunity_cost
                best_cell = (i, j)
                best_path = find_stepping_stone_path(allocations, i, j)

        if max_reduction >= 0:
            break  # La solución es óptima

        # Ajustar las asignaciones siguiendo el mejor camino encontrado
        allocations = adjust_allocations(allocations, best_path)
        total_cost += max_reduction
        description = f"Se realizó un ajuste, nuevo costo total: {total_cost}"
        steps.append({'allocations': [row.copy() for row in allocations],
                      'description': description})

    steps.append({'allocations': [row.copy() for row in allocations],
                  'description': "Solución óptima encontrada con el Método del Paso Secuencial."})

    return steps

def calculate_opportunity_costs(allocations, cost_matrix):
    potentials = {}
    for i in range(len(allocations)):
        for j in range(len(allocations[0])):
            if allocations[i][j] == 0:
                path = find_stepping_stone_path(allocations, i, j)
                if path:
                    opportunity_cost = calculate_path_cost(path, cost_matrix)
                    potentials[(i, j)] = opportunity_cost
    return potentials

def find_stepping_stone_path(allocations, start_i, start_j):
    m, n = len(allocations), len(allocations[0])
    path = [(start_i, start_j)]
    visited = set()

    def backtrack(i, j, direction):
        if (i, j, direction) in visited:
            return None
        visited.add((i, j, direction))
        if direction == 'row':
            for col in range(n):
                if col != j and allocations[i][col] > 0:
                    next_step = (i, col)
                    if next_step == (start_i, start_j):
                        return [next_step]
                    result = backtrack(i, col, 'col')
                    if result is not None:
                        return [next_step] + result
        else:
            for row in range(m):
                if row != i and allocations[row][j] > 0:
                    next_step = (row, j)
                    if next_step == (start_i, start_j):
                        return [next_step]
                    result = backtrack(row, j, 'row')
                    if result is not None:
                        return [next_step] + result
        visited.remove((i, j, direction))
        return None

    result = backtrack(start_i, start_j, 'row')
    if result:
        return path + result
    return None

def calculate_path_cost(path, cost_matrix):
    cost = 0
    sign = 1  # Iniciar con signo positivo
    for i, j in path:
        cost += sign * cost_matrix[i][j]
        sign *= -1  # Alternar signo
    return cost

def adjust_allocations(allocations, path):
    # Encontrar la cantidad máxima que se puede restar (theta)
    theta = min([allocations[i][j] for idx, (i, j) in enumerate(path) if idx % 2 != 0])
    # Ajustar las asignaciones
    for idx, (i, j) in enumerate(path):
        if idx % 2 == 0:
            allocations[i][j] += theta
        else:
            allocations[i][j] -= theta
    return allocations

def modi_method(allocations, cost_matrix):
    steps = []
    total_cost = calculate_total_cost(allocations, cost_matrix)
    steps.append({'allocations': [row.copy() for row in allocations],
                  'description': f"Costo total inicial: {total_cost}"})

    while True:
        u, v = calculate_potentials(allocations, cost_matrix)
        delta = calculate_delta(allocations, cost_matrix, u, v)
        min_delta = min([delta[i][j] for i in range(len(delta)) for j in range(len(delta[0])) if delta[i][j] < 0], default=0)

        if min_delta >= 0:
            break  # La solución es óptima

        i_min, j_min = [(i, j) for i in range(len(delta)) for j in range(len(delta[0])) if delta[i][j] == min_delta][0]
        path = find_loop(allocations, i_min, j_min)
        allocations = adjust_allocations_modi(allocations, path)
        total_cost = calculate_total_cost(allocations, cost_matrix)
        description = f"Se realizó un ajuste, nuevo costo total: {total_cost}"
        steps.append({'allocations': [row.copy() for row in allocations],
                      'description': description})

    steps.append({'allocations': [row.copy() for row in allocations],
                  'description': "Solución óptima encontrada con el Método MODI."})

    return steps

def calculate_potentials(allocations, cost_matrix):
    m, n = len(allocations), len(allocations[0])
    u = [None] * m
    v = [None] * n
    u[0] = 0  # Fijamos u[0] = 0
    basic_cells = [(i, j) for i in range(m) for j in range(n) if allocations[i][j] > 0]

    for _ in range(len(basic_cells)):
        for i, j in basic_cells:
            if u[i] is not None and v[j] is None:
                v[j] = cost_matrix[i][j] - u[i]
            elif u[i] is None and v[j] is not None:
                u[i] = cost_matrix[i][j] - v[j]

    return u, v

def calculate_delta(allocations, cost_matrix, u, v):
    m, n = len(allocations), len(allocations[0])
    delta = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if allocations[i][j] == 0:
                delta[i][j] = cost_matrix[i][j] - u[i] - v[j]
    return delta

def find_loop(allocations, start_i, start_j):
    m, n = len(allocations), len(allocations[0])
    path = [(start_i, start_j)]
    visited = set()

    def backtrack(i, j, direction):
        if (i, j, direction) in visited:
            return None
        visited.add((i, j, direction))
        if direction == 'row':
            for col in range(n):
                if col != j and (allocations[i][col] > 0 or (i == start_i and col == start_j)):
                    next_step = (i, col)
                    if next_step == (start_i, start_j):
                        return [next_step]
                    result = backtrack(i, col, 'col')
                    if result is not None:
                        return [next_step] + result
        else:
            for row in range(m):
                if row != i and (allocations[row][j] > 0 or (row == start_i and j == start_j)):
                    next_step = (row, j)
                    if next_step == (start_i, start_j):
                        return [next_step]
                    result = backtrack(row, j, 'row')
                    if result is not None:
                        return [next_step] + result
        visited.remove((i, j, direction))
        return None

    result = backtrack(start_i, start_j, 'row')
    if result:
        return path + result
    return None

def adjust_allocations_modi(allocations, path):
    # Encontrar la cantidad máxima que se puede restar (theta)
    theta = min([allocations[i][j] for idx, (i, j) in enumerate(path[1:], start=1) if idx % 2 != 0])
    # Ajustar las asignaciones
    for idx, (i, j) in enumerate(path):
        if idx % 2 == 0:
            allocations[i][j] += theta
        else:
            allocations[i][j] -= theta
    return allocations

def calculate_total_cost(allocations, cost_matrix):
    total_cost = 0
    for i in range(len(allocations)):
        for j in range(len(allocations[0])):
            total_cost += allocations[i][j] * cost_matrix[i][j]
    return total_cost
