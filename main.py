#!/usr/bin/python

from pprint import pprint

from constants import round_constants
from constants import sbox

matrix_size = 4


def hex_to_matrix(hex_array):
    """
    Converts hex arrays to 4x4 matrices
    :param hex_array: Array of 16 hex chars
    :return: 4x4 matrix representation
    """
    matrix = []
    for i in range(16):
        if i % matrix_size == 0:
            matrix.append([hex_array[i]])
        else:
            matrix[int(i / matrix_size)].append(hex_array[i])
    return matrix


def text_to_hex(text):
    """
    Converts text to a array-hex representation
    :param text: String/ASCII/UNICODE text
    :return: Array of hex chars
    """
    hex_array = []
    for char in text:
        hex_array.append(ord(char))
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
        new_key = round_key.copy()
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
    :return: Encrypted text
    """
    key_matrix = hex_to_matrix(text_to_hex(passphrase))
    text_matrix = hex_to_matrix(text_to_hex(text))
    round_keys = key_expansion(key_matrix)
    merged_matrix = xor_matrices(key_matrix, text_matrix)
    # 9 intermediate rounds for 128 Bit key size
    for i in range(1):
        confused_matrix = confusion(merged_matrix)
        diffused_matrix = diffusion(confused_matrix)
        mixed_matrix = mix_columns(diffused_matrix)
        merged_matrix = xor_matrices(merged_matrix, mixed_matrix)


def confusion(merged_matrix):
    """
    Applies confusion by running bytes through sbox
    :param merged_matrix: Merged matrix of key and text
    :return: New "confused" matrix
    """
    pprint(merged_matrix)
    merged_matrix = merged_matrix.copy()
    for i in range(matrix_size):
        for j in range(matrix_size):
            merged_matrix[i][j] = sbox[merged_matrix[i][j]]
    pprint(merged_matrix)
    return merged_matrix


def diffusion(merged_matrix):
    """
    Shifts the merged matrix to the left
    :param merged_matrix: Merged matrix of key and text
    :return: New "diffused" matrix
    """
    merged_matrix = merged_matrix.copy()
    for i in range(matrix_size):
        merged_matrix[i] = merged_matrix[i][-i:] + merged_matrix[i][:-i]
    pprint(merged_matrix)
    return merged_matrix


def mix_columns(merged_matrix):
    """
    Mixes columns with AES MixColumns algorithm
    :param merged_matrix: Merged matrix of key and text
    :return: New "mixed" matrix
    """
    return merged_matrix  # TODO


def xor_matrix(first, second):
    """
    XORs 1-dimensional matrices
    :param first: First matrix
    :param second: Second matrix
    :return: XORed (first) matrix
    """
    first = first.copy()
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
    first = first.copy()
    for i in range(len(first)):
        first[i] = xor_matrix(first[i], second[i])
    return first


test_key = text_to_hex("Thats my Kung Fu")
test_text = text_to_hex("Two One Nine Two")

encrypt("ATTACK AT DAWN! ", "SOME 128 BIT KEY")
