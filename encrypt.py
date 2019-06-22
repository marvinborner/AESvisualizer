#!/usr/bin/python
import copy
import sys

from constants import round_constants
from constants import sbox

matrix_size = 4


def hex_to_matrix(hex_array):
    """
    Converts hex arrays to 4x4 matrices
    :param hex_array: Array of 16 hex chars
    :return: 4x4 matrix representation
    """
    hex_matrix = []
    for i in range(16):
        if i % matrix_size == 0:
            hex_matrix.append([hex_array[i]])
        else:
            hex_matrix[int(i / matrix_size)].append(hex_array[i])
    return hex_matrix


def int_to_hex_string(number):
    """
    Converts an integer to it's regarding hex representation
    :param number: Number to convert as base-10 integer
    :return: string of hex representation
    """
    if type(number) == int:
        return "%0.2X" % number
    else:
        return str(number)


def text_to_hex(text):
    """
    Converts text to a array-hex representation
    :param text: String/ASCII/UNICODE text
    :return: Array of hex chars
    """
    hex_array = []
    for char in text:
        hex_array.append(ord(char))
    hex_array = hex_array + [0x01] * (16 - len(hex_array))
    return hex_array


def key_expansion(key_matrix):
    """
    Expands a single key matrix to 11 distinct ones
    :param key_matrix: Matrix of master passphrase
    :return: Array of 11 round keys
    """
    round_keys = [key_matrix]
    round_key = key_matrix[:]
    for r in range(0, 10):
        new_key = copy.deepcopy(round_key)
        last = round_key[3]
        new_key[3] = round_last(new_key[3], r)
        new_key[0] = xor_matrix(new_key[0], new_key[3])
        new_key[1] = xor_matrix(new_key[1], new_key[0])
        new_key[2] = xor_matrix(new_key[2], new_key[1])
        new_key[3] = xor_matrix(last, new_key[2])
        round_key = new_key
        round_keys += [new_key]
    return round_keys


def round_last(round_key, r):
    """
    Applies special actions for bottom row
    :param round_key: Complete matrix round key
    :param r: Round index
    :return: Modified bottom row (last column)
    """
    # Shift bottom row
    last_column = round_key[1:] + round_key[:1]

    # Byte substitution (sbox uses hex representation as index)
    for column in range(matrix_size):
        last_column[column] = sbox[last_column[column]]

    # Adding round constant
    last_column[0] = last_column[0] ^ round_constants[r]
    return last_column


def encrypt(text, passphrase):
    """
    Encrypts a text using a 128-Bit passphrase
    :param text: Plain text
    :param passphrase: 128-Bit passphrase (16 chars)
    :return: Encrypted text as hex
    """
    key_matrix = hex_to_matrix(text_to_hex(passphrase))
    text_matrix = hex_to_matrix(text_to_hex(text))
    round_keys = key_expansion(key_matrix)
    merged_matrix = xor_matrices(key_matrix, text_matrix)

    # 9 intermediate rounds (+1 round without mixing) for 128 Bit key size
    for r in range(10):
        confused_matrix = confusion(copy.deepcopy(merged_matrix))
        diffused_matrix = diffusion(copy.deepcopy(confused_matrix))

        if r == 9:
            merged_matrix = xor_matrices(diffused_matrix, round_keys[r + 1])
        else:
            mixed_matrix = mix_columns(diffused_matrix)
            merged_matrix = xor_matrices(mixed_matrix, round_keys[r + 1])
            print(" ".join([int_to_hex_string(item) for sublist in merged_matrix for item in sublist]))
    flat_matrix = [int_to_hex_string(item) for sublist in merged_matrix for item in sublist]
    print(" ".join(flat_matrix))


def confusion(merged_matrix):
    """
    Applies confusion by running bytes through sbox (SubBytes)
    :param merged_matrix: Merged matrix of key and text
    :return: New "confused" matrix
    """
    merged_matrix = copy.deepcopy(merged_matrix)
    for i in range(matrix_size):
        for j in range(matrix_size):
            merged_matrix[i][j] = sbox[merged_matrix[i][j]]
    return merged_matrix


def diffusion(merged_matrix):
    """
    Shifts the merged matrix to the left (ShiftRows)
    :param merged_matrix: Merged matrix of key and text
    :return: New "diffused" matrix
    """
    merged_matrix = copy.deepcopy(merged_matrix)
    # Rotate matrix CCW
    merged_matrix = [list(element) for element in list(zip(*reversed(merged_matrix)))]
    # Shift matrix
    for i in range(matrix_size):
        merged_matrix[i] = merged_matrix[i][-i:] + merged_matrix[i][:-i]
    # Rotate matrix back (CW)
    merged_matrix = [list(element)[::-1] for element in list(zip(*reversed(merged_matrix)))][::-1]
    return merged_matrix


def mix_columns(merged_matrix):
    """
    Mixes columns with AES MixColumns algorithm (MixColumns)
    :param merged_matrix: Merged matrix of key and text
    :return: New "mixed" matrix
    """
    merged_matrix = copy.deepcopy(merged_matrix)
    magic = lambda x: (((x << 1) ^ 0x1B) & 0xFF) if (x & 0x80) else (x << 1)
    for i in range(4):
        a = merged_matrix[i]
        t = a[0] ^ a[1] ^ a[2] ^ a[3]
        u = a[0]
        a[0] ^= t ^ magic(a[0] ^ a[1])
        a[1] ^= t ^ magic(a[1] ^ a[2])
        a[2] ^= t ^ magic(a[2] ^ a[3])
        a[3] ^= t ^ magic(a[3] ^ u)
    return merged_matrix


def xor_matrix(first, second):
    """
    XORs 1-dimensional matrices
    :param first: First matrix
    :param second: Second matrix
    :return: XORed (first) matrix
    """
    first = copy.deepcopy(first)
    for i in range(4):
        first[i] = first[i] ^ second[i]
    return first


def xor_matrices(first, second):
    """
    XORs 2-dimensional matrices
    :param first: First matrix
    :param second: Second matrix
    :return: XORed (first) matrix
    """
    first = copy.deepcopy(first)
    for i in range(len(first)):
        first[i] = xor_matrix(first[i], second[i])
    return first


encrypt(sys.argv[1], sys.argv[2])
