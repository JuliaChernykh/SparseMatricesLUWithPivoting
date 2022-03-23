from CSR import CSR
from LU_decompose import LU_decompose
from read_matrix_collection import read_data
from tabulate import tabulate
import time
from pivoting_methods.exact_local_filling_estimate import get_pivot_with_lowest_local_filling
from pivoting_methods.rough_local_filling_estimate import get_pivot_with_lowest_local_filling_estimate
from pivoting_methods.rough_local_filling_estimate import get_pivot_with_lowest_local_filling_estimate_2
from pivoting_methods.absolute_maximum import get_abs_max_pivot

def output(table):
    with open("output.txt", "w") as f:
        f.write(table)


collection = read_data()
for i in range(len(collection)):
    collection[i] = CSR(*collection[i])

table = [['Size', 'Pivoting method', 'Filling after decomposition', 'Time', 'Algorithm complexity']]
pivoting_methods_names = ['Absolute maximum', 'Exact local filling estimate', 'Rough local filling estimate I', 'Rough local filling estimate II']
pivoting_methods = [get_abs_max_pivot, get_pivot_with_lowest_local_filling, get_pivot_with_lowest_local_filling_estimate, get_pivot_with_lowest_local_filling_estimate_2]

for matrix in collection:
    for idx, method in enumerate(pivoting_methods):
        start = time.time()
        LU, P, Q = LU_decompose(matrix, method)
        end = time.time()
        table.append([f'{matrix.n}', pivoting_methods_names[idx], f'{(len(LU.values) - len(matrix.values)) / len(matrix.values)}', f'{end - start}', ''])
        print(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))

output(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))

