from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, value, PULP_CBC_CMD
import matplotlib.pyplot as plt

# distance matrix (rows - regions, columns - representatives)
D = [
    [16.160, 24.080, 24.320, 21.120],
    [19.000, 26.470, 27.240, 17.330],
    [25.290, 32.490, 33.420, 12.250],
    [0.000, 7.930, 8.310, 36.120],
    [3.070, 6.440, 7.560, 37.360],
    [1.220, 7.510, 8.190, 36.290],
    [2.800, 10.310, 10.950, 33.500],
    [2.870, 5.070, 5.670, 38.800],
    [3.800, 8.010, 7.410, 38.160],
    [12.350, 4.520, 4.350, 48.270],
    [11.110, 3.480, 2.970, 47.140],
    [21.990, 22.020, 24.070, 39.860],
    [8.820, 3.300, 5.360, 43.310],
    [7.930, 0.000, 2.070, 43.750],
    [9.340, 2.250, 1.110, 45.430],
    [8.310, 2.070, 0.000, 44.430],
    [7.310, 2.440, 1.110, 43.430],
    [7.550, 0.750, 1.530, 43.520],
    [11.130, 18.410, 19.260, 25.400],
    [17.490, 23.440, 24.760, 23.210],
    [11.030, 18.930, 19.280, 25.430],
    [36.120, 43.750, 44.430, 0.000]
]

# labor intensity (for each region) - sum labor intensity for each representative should be in [0.9, 1.1]
P = [0.1609, 0.1164, 0.1026, 0.1516, 0.0939, 0.1320, 0.0687, 0.0930, 0.2116, 0.2529, 0.0868, 0.0828, 0.0975, 0.8177,
     0.4115, 0.3795, 0.0710, 0.0427, 0.1043, 0.0997, 0.1698, 0.2531]

# current assignment (one representative per region)
A = [
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
]

# current locations of representatives (indices of regions counting from one)
L = [4, 14, 16, 22]


# we aim to make the total effort involved with regions divided by each representative
# was similar and close 1
# calculations

def solve_epsilon_constrained(epsilon):
    problem = LpProblem("Pfizer", LpMinimize)

    nLoc = len(P)
    nRep = len(L)

    # === Variables ===
    x = LpVariable.dicts("x", ((i, j) for i in range(nLoc)
                               for j in range(nRep)), 0, 1, LpBinary)

    # === Objectives ===
    # Minimizing the distance f1
    problem += lpSum(D[i][j] * x[(i, j)]
                     for i in range(nLoc) for j in range(nRep))

    # Bounding f2 change (constraint)
    change_f2 = lpSum((1 - A[i][j]) * x[(i, j)] * P[i]
                      for i in range(nLoc) for j in range(nRep))
    problem += change_f2 <= epsilon

    # === Other constraints ===
    # Each region must have exactly one representative assigned
    for i in range(nLoc):
        problem += lpSum(x[(i, j)] for j in range(nRep)) == 1

    # Total labor intensity of the regions allocated to each representative it should
    # be in the range [0.9; 1.1]
    for j in range(nRep):
        repr_labor = lpSum(P[i] * x[(i, j)] for i in range(nLoc))
        problem += repr_labor >= 0.9
        problem += repr_labor <= 1.1

    status = problem.solve(PULP_CBC_CMD(msg=0))
    assignment = [[value(x[(i, j)]) for i in range(nLoc)]
                  for j in range(nRep)]
    distance_f1 = value(problem.objective)
    change_f2 = value(change_f2)
    return status, assignment, distance_f1, change_f2


eps = []
F1 = []
F2 = []

solutions = set()

epsilon = 0.0
for i in range(1000):
    status, assignment, f1, f2 = solve_epsilon_constrained(epsilon)
    if status == 1:
        F1.append(f1)
        F2.append(f2)
        eps.append(epsilon)
        if (f1, f2) not in solutions:
            print(f"{epsilon:.3f} - New solution ({f1:.3f}, {f2:.3f})")
        solutions.add((f1, f2))
    epsilon += 0.002


print(solutions)
plt.plot(F1, F2, marker='o')
plt.xlabel('f1 (Distance)')
plt.ylabel('f2 (Changes)')
plt.title('Pfizer - pareto front')
plt.show()
