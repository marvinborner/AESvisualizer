#!/usr/bin/python

matrix_size = 4
round_constants = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


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
    for i in range(1, 11):
        # Move top byte to bottom
        top = round_key[0][3]
        for row in range(matrix_size - 1):
            round_key[row][3] = round_key[row + 1][3]
        # TODO: sBox
        round_key[3][3] = top ^ round_constants[i]
        # Modify first column by XORing it with the previous round key
        for column in range(matrix_size - 1):
            for row in range(matrix_size):
                round_key[row][column] = round_key[row][column] ^ round_keys[i - 1][row][column]
        round_keys.append(round_key)
    return round_keys


test_key = text_to_hex("Thats my Kung Fu")
test_text = text_to_hex("Two One Nine Two")

print(hex_to_matrix(test_key))
print(key_expansion(hex_to_matrix(test_key)))
print(shift_matrix(hex_to_matrix(test_key)))
