from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from CSR.CSR import CSR, Vector
from LU_decomposition.LU_decomposition import LU_decompose
from LU_decomposition.tests import test
from read_matrix_collection import read_data
from tabulate import tabulate
from time import process_time
from functools import partial
from pivoting_methods.exact_local_filling_estimate import get_pivot_with_lowest_local_filling
from pivoting_methods.rough_local_filling_estimate import (
    get_pivot_with_lowest_local_filling_estimate,
    get_estimation,
    get_estimation_2,
    get_estimation_3,
    get_pivot_from_min_column_row_count,
    get_pivot_from_min_row_column_count,
    without_pivoting,
)
from pivoting_methods.absolute_maximum import get_abs_max_pivot
from QR_decomposition.QR_decomposition import QR_decompose

LU_PIVOTING_METHODS = [
    ('absolute maximum', get_abs_max_pivot),
    ('exact estimation', get_pivot_with_lowest_local_filling),
    ('minimizing row count * column count',
        partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation)),
    ('minimizing row count + column count',
        partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_2)),
    ('minimizing row count * column count^2',
        partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_3)),
    ('min_row_column_count', get_pivot_from_min_row_column_count),
    ('min_column_row_count', get_pivot_from_min_column_row_count),
]
QR_PIVOTING_METHODS = [
    ('without pivoting', without_pivoting),
    ('minimizing row count * column count',
        partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation)),
    ('minimizing row count + column count',
        partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_2)),
    ('minimizing row count * column count^2',
        partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_3)),
    ('min_row_column_count', get_pivot_from_min_row_column_count),
    ('min_column_row_count', get_pivot_from_min_column_row_count),
]

def output(table):
    with open("output.txt", "w") as f:
        f.write(table)


def main():
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('sizes', type=int, nargs='+', help='a size of matrix')
    parser.add_argument("--lu", dest='run_lu', const=True, default=False, action='store_const', help="Run LU")
    parser.add_argument("--qr", dest='run_qr', const=True, default=False, action='store_const', help="Run QR")
    args = parser.parse_args()

    collection = read_data()
    for i in range(len(collection)):
        collection[i] = CSR(*collection[i])

    table = [['Size', 'Pivoting method', 'Filling before decomposition', 'Filling after decomposition', 'Filling increase', 'Time']]

    for matrix in collection:

        if matrix.n in args.sizes:
            print(matrix.n)
            if args.run_qr:
                print('start QR decomposition')
                for method_name, method in QR_PIVOTING_METHODS:
                    start = process_time()
                    Q, R, P, C = QR_decompose(matrix, method)
                    end = process_time()
                    table.append([
                        f'{matrix.n}',
                        method_name,
                        f'{len(matrix.values) / matrix.n**2}',
                        f'{len(R.values) / R.n**2}',
                        # f'{len(R.values) / len(matrix.values)}',
                        f'{len([value for value in R.values if abs(value) > 1e-9]) / len(matrix.values)}',
                        f'{end - start}'
                    ])
                    print(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))
                print('finish QR decomposition')

            if args.run_lu:
                print('start LU decomposition')
                for method_name, method in LU_PIVOTING_METHODS:
                    start = process_time()
                    LU, P, Q = LU_decompose(matrix, method)
                    end = process_time()
                    table.append([
                        f'{matrix.n}',
                        method_name,
                        f'{len(matrix.values) / matrix.n**2}',
                        f'{len(LU.values) / LU.n**2}',
                        f'{len(LU.values) / len(matrix.values)}',
                        f'{end - start}'
                    ])
                    print(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))
                    print(test(matrix, P, Q, LU))
                print('finish LU decomposition')

    output(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))


if __name__ == '__main__':
    main()
