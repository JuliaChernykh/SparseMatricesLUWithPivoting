import ssgetpy
import os
import tarfile

def download_data():
    ssgetpy.search(rowbounds=(50, 100)).download(destpath='data_zipped')


def reformat_to_csr(lines):
    comment_length = 12
    n = list(map(int, lines[comment_length + 1].split(' ')))[0]
    lines = lines[comment_length + 2:]
    values, cols, next_row = [], [], []
    prev_i = -1
    values_in_row_counter = 0
    for idx, line in enumerate(lines):
        j, i, value = map(float, line.split(' '))
        i = int(i)
        j = int(j)
        if value != 0:
            if i - 1 == prev_i + 1:
                next_row.append(values_in_row_counter)
                prev_i = i - 1
            elif i - 1 != prev_i:
                next_row.append(next_row[-1])
                prev_i = i - 1

            values.append(value)
            cols.append(j - 1)
            values_in_row_counter += 1

            if idx + 1 == len(lines):
                next_row.append(values_in_row_counter)

    return values, cols, next_row, n


def read_data():
    collection = []

    for root, dirs, files in os.walk("data_zipped"):
        for file in files:
            with tarfile.open(f'data_zipped/{file}', mode='r') as f:
                f.extractall(path='data_unzipped')

    for root, dirs, _ in os.walk("data_unzipped"):
        for dir in dirs:
            for _, _, files in os.walk(f"data_unzipped/{dir}"):
                with open(f'data_unzipped/{dir}/{files[0]}', mode='r') as f:
                    collection.append(reformat_to_csr(f.readlines()))

    return collection
