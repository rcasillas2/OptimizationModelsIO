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
        opportunity_costs = []
        for i in range(len(allocations)):
            for j in range(len(allocations[0])):
                if allocations[i][j] == 0:
                    path = find_closed_path(i, j, allocations)
                    if path:
                        cost = calculate_opportunity_cost(path, cost_matrix)
                        opportunity_costs.append((cost, path))

        if not opportunity_costs:
            break  # No hay más mejoras posibles

        min_cost, best_path = min(opportunity_costs, key=lambda x: x[0])
        if min_cost >= 0:
            break  # La solución es óptima

        allocations = adjust_allocations(allocations, best_path)
        total_cost += min_cost
        steps.append({'allocations': [row.copy() for row in allocations],
                      'description': f"Mejora realizada, nuevo costo total: {total_cost}"})

    steps.append({'allocations': [row.copy() for row in allocations],
                  'description': "Solución óptima encontrada con el Método del Paso Secuencial."})

    return steps

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
        path = find_closed_path(i_min, j_min, allocations)
        allocations = adjust_allocations(allocations, path)
        total_cost = calculate_total_cost(allocations, cost_matrix)
        steps.append({'allocations': [row.copy() for row in allocations],
                      'description': f"Mejora realizada, nuevo costo total: {total_cost}"})

    steps.append({'allocations': [row.copy() for row in allocations],
                  'description': "Solución óptima encontrada con el Método MODI."})

    return steps

def calculate_total_cost(allocations, cost_matrix):
    total_cost = 0
    for i in range(len(allocations)):
        for j in range(len(allocations[0])):
            total_cost += allocations[i][j] * cost_matrix[i][j]
    return total_cost

def find_closed_path(i, j, allocations):
    # Implementación de búsqueda de camino cerrado (ciclo)
    m, n = len(allocations), len(allocations[0])
    visited = set()
    path = []

    def dfs(x, y, direction):
        if (x, y, direction) in visited:
            return None
        visited.add((x, y, direction))
        if direction == 'row':
            for k in range(n):
                if allocations[x][k] > 0 or (x == i and k == j):
                    if k != y:
                        result = dfs(x, k, 'col')
                        if result is not None:
                            return [(x, y)] + result
        else:
            for k in range(m):
                if allocations[k][y] > 0 or (k == i and y == j):
                    if k != x:
                        if k == i and y == j:
                            return [(x, y)]
                        result = dfs(k, y, 'row')
                        if result is not None:
                            return [(x, y)] + result
        visited.remove((x, y, direction))
        return None

    path = dfs(i, j, 'row')
    return path

def calculate_opportunity_cost(path, cost_matrix):
    even = True
    cost = 0
    for i, j in path:
        if even:
            cost += cost_matrix[i][j]
        else:
            cost -= cost_matrix[i][j]
        even = not even
    return cost

def adjust_allocations(allocations, path):
    quantities = [allocations[i][j] for idx, (i, j) in enumerate(path) if idx % 2 != 0]
    theta = min(quantities)
    for idx, (i, j) in enumerate(path):
        if idx % 2 == 0:
            allocations[i][j] += theta
        else:
            allocations[i][j] -= theta
    return allocations

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
