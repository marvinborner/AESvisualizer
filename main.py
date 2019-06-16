#!/usr/bin/python

from pprint import pprint

from constants import round_constants
from constants import sbox

matrix_size = 4


def hex_to_matrix(hex_array):
    matrix = []
    for i in range(16):
        if i % matrix_size == 0:
            matrix.append([hex_array[i]])
        else:
            matrix[int(i / 4)].append(hex_array[i])
    return matrix


def text_to_hex(text):
    hex_array = []
    for char in text:
        hex_array.append(ord(char))
    return hex_array


def shift_matrix(matrix):
    for i in range(matrix_size):
        matrix[i] = matrix[i][-i:] + matrix[i][:-i]
    return matrix


def key_expansion(round_key):
    round_keys = [round_key]
    print(round_key)
    for r in range(0, 10):
        last = round_key[3]

        round_key[3] = round_last(round_key[3], r)
        round_key[0] = xor_matrix(round_key[0], round_key[3])
        round_key[1] = xor_matrix(round_key[1], round_key[0])
        round_key[2] = xor_matrix(round_key[2], round_key[1])
        round_key[3] = xor_matrix(last, round_key[2])

        print(round_key)
        round_keys.append(round_key)


def xor_matrix(first, second):
    for i in range(4):
        first[i] = first[i] ^ second[i]
    return first


def round_last(round_key, r):
    # Shift bottom row
    last_column = round_key[1:] + round_key[:1]

    # Byte substitution (sbox uses hex representation as index)
    for column in range(matrix_size):
        last_column[column] = sbox[last_column[column]]

    # Adding round constant
    last_column[0] = last_column[0] ^ round_constants[r]
    return last_column


test_key = text_to_hex("Thats my Kung Fu")
test_text = text_to_hex("Two One Nine Two")

pprint(hex_to_matrix(test_key))
print("\n\n")
pprint(key_expansion(hex_to_matrix(test_key)))
