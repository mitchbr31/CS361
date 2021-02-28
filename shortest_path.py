import numpy as np
from scipy.optimize import linprog

edges = [
    (0, 1, 10),
    (1, 2, 2),
    (4, 0, 1),
    (0, 3, 5),
    (4, 1, 1),
    (3, 4, 2),
    (4, 2, 4),
    (3, 5, 10),
    (5, 4, 2),
    (5, 6, 7),
    (6, 4, 4),
    (6, 2, 2),
    (2, 6, 2),
    (2, 7, 8),
    (6, 7, 3),
    (7, 8, 100)
]

s, t = 0, 7

nodes = set()
for edge in edges:
    if edge[0] not in nodes:
        nodes.add(edge[0])
    if edge[1] not in nodes:
        nodes.add(edge[1])
nodes = sorted(nodes)

n_nodes = len(nodes)
n_edges = len(edges)
edge_matrix = np.zeros((n_nodes, n_nodes), dtype=int)

for edge in edges:
    u, v, w = edge
    u_index = nodes.index(u)
    v_index = nodes.index(v)
    edge_matrix[u_index, v_index] = w

nonzero_edges = np.nonzero(edge_matrix)
edge_dict = {}
dict_index = 0

for edge_index in range(n_edges):
    edge_u = nonzero_edges[0][edge_index]
    edge_v = nonzero_edges[1][edge_index]
    edge_dict[(edge_u, edge_v)] = dict_index
    dict_index += 1

s_index = nodes.index(s)
t_index = nodes.index(t)
print(nodes)
print(s_index)


bounds = [(0,1) for i in range(n_edges)]
c = [i[2] for i in edges]

A_rows = []
b_rows = []

for source in range(n_nodes):
    out_indices = np.flatnonzero(edge_matrix[source, :])
    in_indices = np.flatnonzero(edge_matrix[:, source])

    rhs = 0
    if source == s_index:
        rhs = 1
    elif source == t_index:
        rhs = -1

    n_out = len(out_indices)
    n_in = len(in_indices)

    out_edges = [edge_dict[edge_u, edge_v] for edge_u, edge_v in np.vstack((np.full(n_out, source), out_indices)).T]
    in_edges = [edge_dict[edge_u, edge_v] for edge_u, edge_v in np.vstack((in_indices, np.full(n_in, source))).T]

    A_row = np.zeros(n_edges)
    A_row[out_edges] = 1
    A_row[in_edges] = -1

    A_rows.append(A_row)
    b_rows.append(rhs)

A = np.vstack(A_rows)
b = np.array(b_rows)
result = linprog(c, A_eq=A, b_eq=b, bounds=bounds, method='simplex') 
print(result)