import bisect
import numpy as np


class Vector:
    def __init__(self, values=None, indicies=None):
        self.values = values if values is not None else []
        self.indicies = indicies if indicies is not None else []

    def add_element(self, val, index):
        self.values.append(val)
        self.indicies.append(index)

    def __mul__(self, other):
        result = 0
        l_pointer = 0
        r_pointer = 0
        while l_pointer < len(self.indicies) and r_pointer < len(other.indicies):
            if self.indicies[l_pointer] == other.indicies[r_pointer]:
                result += self.values[l_pointer]*other.values[r_pointer]
                l_pointer += 1
                r_pointer += 1
            elif self.indicies[l_pointer] < other.indicies[r_pointer]:
                l_pointer += 1
            else:
                r_pointer += 1
        return result

    def __str__(self):
        return str(self.values) + str(self.indicies)

    def __repr__(self):
        return str(self.values) + str(self.indicies)


class CSR:
    def __init__(self, values, cols, row_start, n):
        self.values = values
        self.cols = cols
        self.row_start = row_start
        self.n = n

    def get_element(self, row, col):
        ind = -1
        for k in range(self.row_start[row], self.row_start[row + 1]):
            if self.cols[k] == col:
                ind = k
        if ind == -1:
            return 0
        return self.values[ind]

    @staticmethod
    def is_permissible_value(value):
        eps = 1e-15
        return abs(value) > eps

    def set_value(self, value, row, col):
        old_value = self.get_element(row, col)
        if old_value != 0:
            if value != 0:
            # if self.is_permissible_value(value):
                self.change_element_value(value, row, col)
            else:
                self.remove_element(row, col)
        elif value != 0:
        # elif self.is_permissible_value(value):
            self.add_element(value, row, col)

    def change_element_value(self, value, row, col):
        for k in range(self.row_start[row], self.row_start[row + 1]):
            if self.cols[k] == col:
                ind = k
        self.values[ind] = value

    def add_element(self, value, row, col):
        if self.get_element(row, col) != 0:
            self.change_element_value(value, row, col)
        else:
            # inserting new col index
            new_cols = self.cols[self.row_start[row]: self.row_start[row + 1]]
            bisect.insort(new_cols, col)
            self.cols = self.cols[:self.row_start[row]] + new_cols + self.cols[self.row_start[row + 1]:]

            # inserting new value
            value_index = new_cols.index(col)
            self.values.insert(self.row_start[row] + value_index, value)

            # updating pointers list
            for i in range(row + 1, len(self.row_start)):
                self.row_start[i] += 1

    def remove_element(self, i, j):
        if self.get_element(i, j) != 0:
            for k in range(self.row_start[i], self.row_start[i + 1]):
                if self.cols[k] == j:
                    elem_ind = k
            self.values.pop(elem_ind)
            self.cols.pop(elem_ind)
            for k in range(i + 1, len(self.row_start)):
                self.row_start[k] -= 1

    def multiply_by_vector(self, b):
        col = [0] * (len(self.row_start) - 1)
        for i in range(len(self.row_start) - 1):
            for j in range(self.row_start[i], self.row_start[i + 1]):
                col[i] += self.values[j] * b[self.cols[j]]
        return col

    def multiply_by(self, m):
        return reformat_to_CSR(self.get_matrix() @ m.get_matrix())

    def get_row_vector(self, i):
        values = self.values[self.row_start[i]: self.row_start[i + 1]]
        cols = self.cols[self.row_start[i]: self.row_start[i + 1]]
        row = Vector(values, cols)

        return row

    def get_col_vector(self, j):
        col = Vector()
        for i in range(self.n):
            for k in range(self.row_start[i], self.row_start[i + 1]):
                if self.cols[k] == j:
                    col.add_element(self.values[k], i)

        return col

    def multiply_by_2(self, m):
        result = CSR([], [], [0], self.n)
        not_zero_cnt = 0
        for i in range(self.n):
            row = self.get_row_vector(i)
            for j in range(self.n):
                col = m.get_col_vector(j)
                i_j = row * col
                if i_j != 0:
                    result.values.append(i_j)
                    result.cols.append(j)
                    not_zero_cnt += 1
            result.row_start.append(not_zero_cnt)
        return result

    def add_in_row(self, row_1, row_2):
        # finding cols indices that contain non-zero elements by merging two lists
        start_1, end_1 = self.row_start[row_1], self.row_start[row_1 + 1]
        start_2, end_2 = self.row_start[row_2], self.row_start[row_2 + 1]
        positions = list(set(self.cols[start_1: end_1]).union(set(self.cols[start_2: end_2])))

        # finding non-zero elements after rows addition
        values = ['x'] * self.n
        for i in positions:
            values[i] = 0
        for i in range(start_1, end_1):
            values[self.cols[i]] += self.values[i]
        for i in range(start_2, end_2):
            values[self.cols[i]] += self.values[i]
        values = list(filter(lambda a: a != 'x', values))

        # updating matrix data_zipped
        for i in range(row_1 + 1, len(self.row_start)):
            self.row_start[i] += len(values) - len(self.values[start_1: end_1])
        self.values = values + self.values[end_1:]
        self.cols = positions + self.cols[end_1:]

    def add_row(self, row_ind_1, row_2_cols, row_2_values):
        # finding cols indexes that contain non-zero elements by merging two lists
        start_1, end_1 = self.row_start[row_ind_1], self.row_start[row_ind_1 + 1]
        positions = list(set(self.cols[start_1: end_1]).union(set(row_2_cols)))

        # finding non-zero elements after rows addition
        values = ['x'] * self.n
        for i in positions:
            values[i] = 0

        for i in range(start_1, end_1):
            values[self.cols[i]] += self.values[i]
        for i in range(len(row_2_values)):
            values[row_2_cols[i]] += row_2_values[i]
        values = list(filter(lambda a: a != 'x', values))

        # updating matrix data_zipped
        for i in range(row_ind_1 + 1, len(self.row_start)):
            self.row_start[i] += len(values) - len(self.values[start_1: end_1])
        self.values = self.values[:start_1] + values + self.values[end_1:]
        self.cols = self.cols[:start_1] + positions + self.cols[end_1:]

    def add_matrix(self, values, cols, row_start):
        for i in range(len(self.row_start) - 1):
            self.add_row(i, cols[row_start[i]:row_start[i + 1]], values[row_start[i]:row_start[i + 1]])

    def get_matrix(self):
        matrix = np.array([[float(0)] * self.n for i in range(len(self.row_start) - 1)])
        for i in range(len(self.row_start) - 1):
            for j in range(self.row_start[i], self.row_start[i + 1]):
                matrix[i][self.cols[j]] = self.values[j]
        return matrix

    def get_boolean_matrix(self):
        matrix = np.array([[float(0)] * self.n for i in range(len(self.row_start) - 1)])
        for i in range(len(self.row_start) - 1):
            for j in range(self.row_start[i], self.row_start[i + 1]):
                matrix[i][self.cols[j]] = 1
        return matrix

    def __get_structure(self):
        matrix = np.array([['0'] * self.n for i in range(len(self.row_start) - 1)])
        for i in range(len(self.row_start) - 1):
            for j in range(self.row_start[i], self.row_start[i + 1]):
                matrix[i][self.cols[j]] = 'x'
        return matrix

    def get_nonzero_n(self):
        return len(self.values)

    def get_row(self, col):
        for i in range(1, len(self.row_start)):
            if col < self.row_start[i]:
                row = i - 1
                return row

    def swap_rows(self, row1, row2):
        # использовать insert и pop
        # getting data_zipped of two rows
        values1 = self.values[self.row_start[row1]:self.row_start[row1 + 1]]
        cols1 = self.cols[self.row_start[row1]:self.row_start[row1 + 1]]
        values2 = self.values[self.row_start[row2]:self.row_start[row2 + 1]]
        cols2 = self.cols[self.row_start[row2]:self.row_start[row2 + 1]]

        # updating matrix data_zipped
        self.values = self.values[:self.row_start[row1]] + values2 + self.values[
                                                                     self.row_start[row1 + 1]:self.row_start[
                                                                          row2]] + values1 + self.values[
                                                                                             self.row_start[
                                                                                                 row2 + 1]:]
        self.cols = self.cols[:self.row_start[row1]] + cols2 + self.cols[self.row_start[row1 + 1]:self.row_start[
            row2]] + cols1 + self.cols[self.row_start[row2 + 1]:]
        tmp_ptr = 0
        for i in range(row1 + 1, len(self.row_start) - 1):
            cur_row_start = self.row_start[i]
            self.row_start[i] = self.row_start[i - 1] + tmp_ptr
            tmp_ptr = self.row_start[i + 1] - cur_row_start
            if i - 1 == row1:
                self.row_start[i] = self.row_start[i - 1] + len(values2)
            if i - 1 == row2:
                self.row_start[i] = self.row_start[i - 1] + len(values1)

    def swap_cols(self, col1, col2):
        for i in range(self.n):
            elem1 = self.get_element(i, col1)
            elem2 = self.get_element(i, col2)

            if elem1 != 0 and elem2 == 0:
                self.remove_element(i, col1)
                self.add_element(elem1, i, col2)
            if elem2 != 0 and elem1 == 0:
                self.remove_element(i, col2)
                self.add_element(elem2, i, col1)
            if elem2 != 0 and elem1 != 0:
                self.change_element_value(elem2, i, col1)
                self.change_element_value(elem1, i, col2)

    def transpose(self):
        transposed = self.copy()
        transposed.row_start = [0]*len(transposed.row_start)
        #  calculating non-zeroes in each column
        for i in range(len(transposed.cols)):
            transposed.row_start[transposed.cols[i] + 1] += 1
        # from count of non-zeroes in each column generating new row_start
        for i in range(2, len(transposed.row_start)):
            transposed.row_start[i] += transposed.row_start[i - 1]
        row_start_current = np.copy(transposed.row_start)
        # updating values and cols
        for i in range(len(transposed.row_start) - 1):
            for j in range(self.row_start[i], self.row_start[i + 1]):
                new_index = row_start_current[self.cols[j]]
                row_start_current[self.cols[j]] += 1
                transposed.values[new_index] = self.values[j]
                transposed.cols[new_index] = i

        return transposed

    def copy(self):
        values = self.values.copy()
        cols = self.cols.copy()
        row_start = self.row_start.copy()
        cols_n = self.n
        return CSR(values, cols, row_start, cols_n)

    def output(self):
        with open("matrix_repr.txt", "w") as f:
            m = self.get_matrix()
            for row in m:
                row_str = ' '.join(map(str, row)) + '\n'
                f.write(row_str)

    def output_structure(self):
        with open("matrix_repr.txt", "w") as f:
            f.write(str(self.__get_structure()))

    def __eq__(self, other):
        return self.n == other.n and \
               self.values == other.values and \
               self.cols == other.cols and \
               self.row_start == other.row_start


def is_permissible_value(value):
    eps = 1e-15
    return abs(value) > eps

def reformat_to_CSR(matrix):
    values = []
    cols = []
    row_start = [0]
    for i in range(len(matrix)):
        count = 0
        for j in range(len(matrix[i])):
            # if matrix[i][j] != 0:
            if is_permissible_value(matrix[i][j]):
                values.append(matrix[i][j])
                cols.append(j)
                count += 1
        row_start.append(row_start[i] + count)

    return CSR(values, cols, row_start, len(matrix))