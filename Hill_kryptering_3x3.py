# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:03:32 2024

@author: gabri
"""

import random
import numpy as np
import string
from math import gcd

# Define the alphabet dictionary and its inverse
alphabet_dict = {chr(i): i - 65 for i in range(65, 91)}  # A=65 in ASCII, Z=90
inverse_alphabet_dict = {v: k for k, v in alphabet_dict.items()}  # Reverse mapping

# Function to generate a valid key matrix
def generate_valid_key(text_length):
    while True:
        key = [random.randint(0, 25) for _ in range(9)]  # Random numbers for 3x3 key matrix
        key_matrix = np.array(key).reshape(3, 3)
        determinant = int(np.round(np.linalg.det(key_matrix)))  # Determinant of the matrix

        # Check conditions: non-zero determinant and coprime with 26
        if determinant != 0 and gcd(determinant, 26) == 1:
            return key_matrix

# Function to clean the input text
def clean_text(input_text):
    input_text = input_text.upper()
    cleaned_text = ''.join(char for char in input_text if char in alphabet_dict)
    return cleaned_text

# Function to serialize the cleaned text
def serialize_message(input_text, alphabet_dict):
    cleaned_text = clean_text(input_text)
    serialized = [alphabet_dict[char] for char in cleaned_text]
    while len(serialized) % 3 != 0:
        serialized.append(alphabet_dict['X'])  # Pad with 'X' if necessary
    grouped = [serialized[i:i+3] for i in range(0, len(serialized), 3)]
    return grouped, len(cleaned_text)

# Function to perform matrix multiplication and encryption
def encrypt_groups(key_matrix, grouped_message):
    encrypted_groups = []
    for group in grouped_message:
        group_vector = np.array(group).reshape(3, 1)  # Convert to column vector
        encrypted_vector = np.dot(key_matrix, group_vector) % 26  # Matrix multiplication
        encrypted_groups.append(encrypted_vector.flatten().astype(int).tolist())
    return encrypted_groups

# Function to calculate the modular inverse of a number
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Function to find the inverse of the key matrix modulo 26
def invert_key_matrix(key_matrix):
    determinant = int(np.round(np.linalg.det(key_matrix)))  # Determinant of the matrix
    determinant_mod_inv = mod_inverse(determinant % 26, 26)  # Modular inverse of the determinant

    if determinant_mod_inv is None:
        raise ValueError("The key matrix is not invertible modulo 26.")

    # Calculate the adjugate matrix
    adjugate = np.linalg.inv(key_matrix) * determinant
    adjugate = np.round(adjugate).astype(int)  # Round and convert to integers
    adjugate_mod = adjugate % 26  # Take modulo 26

    # Modular inverse matrix
    key_matrix_inv = (determinant_mod_inv * adjugate_mod) % 26
    key_matrix_inv = key_matrix_inv.astype(int)  # Ensure all values are integers
    return key_matrix_inv

# Function to decrypt encrypted groups
def decrypt_groups(key_matrix_inv, encrypted_message):
    decrypted_groups = []
    for group in encrypted_message:
        group_vector = np.array(group).reshape(3, 1)  # Convert to column vector
        decrypted_vector = np.dot(key_matrix_inv, group_vector) % 26  # Matrix multiplication
        decrypted_groups.append(decrypted_vector.flatten().astype(int).tolist())
    return decrypted_groups

# Function to convert numbers back to text
def numbers_to_text(message, inverse_alphabet_dict):
    text = ''.join(inverse_alphabet_dict[num] for group in message for num in group)
    return text

# Input from the user
Plaintext = input("Write the secret message you want encrypted: ")

# Clean, serialize, and group the plaintext
grouped_message, text_length = serialize_message(Plaintext, alphabet_dict)

# Generate a valid 3x3 key matrix
key_matrix = generate_valid_key(text_length)

# Encrypt the grouped message
encrypted_message = encrypt_groups(key_matrix, grouped_message)

# Convert encrypted numbers to ciphertext
ciphertext = numbers_to_text(encrypted_message, inverse_alphabet_dict)

# Decrypt the ciphertext
key_matrix_inv = invert_key_matrix(key_matrix)
decrypted_message = decrypt_groups(key_matrix_inv, encrypted_message)
plaintext_decrypted = numbers_to_text(decrypted_message, inverse_alphabet_dict)

# Output results
print("\nResults:")
print("Key Matrix (3x3):\n", key_matrix)
print("Key Matrix Inverse Modulo 26:\n", key_matrix_inv)
print("Grouped Message:", grouped_message)
print("Encrypted Message (numbers):", encrypted_message)
print("Ciphertext:", ciphertext)
print("Decrypted Message (numbers):", decrypted_message)
print("Decrypted Plaintext:", plaintext_decrypted)
