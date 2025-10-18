"""
cipher tool
Author Dor Levek

Encryption/Decryption  (Cipher System)

The program is encrypting and decrypting messages.
 To run it, you must use either 'encrypt' or 'decrypt' as a parameter; otherwise, the program gives an error.
The core of the tool relies on two dictionaries that establish the character-to-number mapping: one for turning
   characters to numbers and one for the reverse.
Before starting, the check_tables() function runs two integrity tests (Assert 1 and 2) to ensure the codes are
 the same size and the process is reversible. If these tests fail, the program immediately stops working.

The encrypt function gets a message from the user, replaces supported characters with their number codes,
 ignores unsupported ones and warns the user,
 and saves the numbers to a file default: msg_encrypted.txt.
 The decrypt function reads the numbers from the file, turns them back into characters,
 and prints the result to the screen. If the file is not found, an error is given.
 All program activities, including starts, successful runs, and errors, are recorded in a log file named encryption.
 log.
 """



import sys
import logging

# Setting up a logging system
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='encryption.log',
    filemode='a'
)


def get_encryption_table():
    """
    Returns a dictionary used to encode characters into numbers
    """
    # Encryption dictionary
    return {
        'A': 56, 'B': 57, 'C': 58, 'D': 59, 'E': 40, 'F': 41, 'G': 42, 'H': 43, 'I': 44, 'J': 45,
        'K': 46, 'L': 47, 'M': 48, 'N': 49, 'O': 60, 'P': 61, 'Q': 62, 'R': 63, 'S': 64, 'T': 65,
        'U': 66, 'V': 67, 'W': 68, 'X': 69, 'Y': 10, 'Z': 11, 'a': 12, 'b': 13, 'c': 14, 'd': 15,
        'e': 16, 'f': 17, 'g': 18, 'h': 19, 'i': 30, 'j': 31, 'k': 32, 'l': 33, 'm': 34, 'n': 35,
        'o': 36, 'p': 37, 'q': 38, 'r': 39, 's': 90, 't': 91, 'u': 92, 'v': 93, 'w': 94, 'x': 95,
        'y': 96, 'z': 97, '.': 100, "'": 101, ',': 99, ' ': 98, '-': 103, '!': 102
    }


def get_decryption_table():
    """
    Returns a dictionary used to decode numbers back to characters
    """
    # Dictionary for decoding
    return {
        56: 'A', 57: 'B', 58: 'C', 59: 'D', 40: 'E', 41: 'F', 42: 'G', 43: 'H', 44: 'I', 45: 'J',
        46: 'K', 47: 'L', 48: 'M', 49: 'N', 60: 'O', 61: 'P', 62: 'Q', 63: 'R', 64: 'S', 65: 'T',
        66: 'U', 67: 'V', 68: 'W', 69: 'X', 10: 'Y', 11: 'Z', 12: 'a', 13: 'b', 14: 'c', 15: 'd',
        16: 'e', 17: 'f', 18: 'g', 19: 'h', 30: 'i', 31: 'j', 32: 'k', 33: 'l', 34: 'm', 35: 'n',
        36: 'o', 37: 'p', 38: 'q', 39: 'r', 90: 's', 91: 't', 92: 'u', 93: 'v', 94: 'w', 95: 'x',
        96: 'y', 97: 'z', 100: '.', 101: "'", 99: ',', 98: ' ', 103: '-', 102: '!'
    }


def encrypt(output_filename="msg_encrypted.txt"):
    """
    Receives a message from the user encrypts it and saves the result to a file
    """
    logging.info("Starting encryption process...")
    encrypt_table = get_encryption_table()
    message = input("Please enter the message you want to encrypt: ")

    if not message:
        print("The message is empty. An empty file will be created.")
        logging.warning("User provided an empty message for encryption.")
        with open(output_filename, "w") as file:
            file.write("")
        return

    encrypted_parts = []
    unsupported_chars = set()

    for char in message:
        if char in encrypt_table:
            encrypted_parts.append(str(encrypt_table[char]))
        else:
            unsupported_chars.add(char)

    encrypted_message = ",".join(encrypted_parts)

    with open(output_filename, "w") as file:
        file.write(encrypted_message)

    print(f"The message was encrypted and saved to '{output_filename}'")
    logging.info(f"Encryption successful. Output saved to '{output_filename}'.")

    if unsupported_chars:
        print(f"Warning: The following characters were not supported and were ignored: {' '.join(unsupported_chars)}")
        logging.warning(f"Unsupported characters were ignored during encryption: {unsupported_chars}")


def decrypt(input_filename="msg_encrypted.txt"):
    """
    Reads an encrypted message from a file decrypts it and prints the result
    """
    logging.info("Starting decryption process...")
    decrypt_table = get_decryption_table()

    try:
        with open(input_filename, "r") as file:
            encrypted_message = file.read()
        logging.info(f"Successfully read file '{input_filename}'.")

        if not encrypted_message:
            print("The decrypted message is:")
            print("")
            logging.warning("Decryption file was empty. Output is an empty string.")
            return

        encrypted_numbers = encrypted_message.split(',')
        decrypted_message = []

        for number_str in encrypted_numbers:
            if number_str:
                try:
                    number = int(number_str)
                    if number in decrypt_table:
                        decrypted_message.append(decrypt_table[number])
                    else:
                        decrypted_message.append('?')
                        logging.warning(f"Decryption found an unknown number code: {number}")
                except ValueError:
                    logging.error(f"Invalid content in encryption file. Could not convert '{number_str}' to a number.")
                    continue

        print("The decrypted message is:")
        print("".join(decrypted_message))
        logging.info("Decryption process completed successfully.")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found. You need to encrypt a message first.")
        logging.critical(f"Decryption failed because file '{input_filename}' was not found.")


def check_tables():

    logging.info("Performing integrity check on encryption/decryption tables.")
    encrypt_table = get_encryption_table()
    decrypt_table = get_decryption_table()

    # ASSERT 1: Length matching check: checks if there are the same amount of characters in both dictionaries
    assert len(encrypt_table) == len(decrypt_table), \
        "Critical Error (Assert 1): Table size mismatch. The number of characters and codes must be the same."

    # ASSERT 2: Reversibility check checks if A encrypts to 56, and 56 decrypts back to A;
    for key, value in encrypt_table.items():
        assert decrypt_table.get(value) == key, \
            f"Critical Error (Assert 2): Decryption inconsistency for key '{key}'. Expected '{key}', got '{decrypt_table.get(value)}'."

    logging.info("Integrity check passed successfully (2 checks passed).")


def main():
    """
    The main function of the program
    """
    logging.info("Program started.")
    try:
        check_tables()
    except AssertionError as e:
        print(f"FATAL INTEGRITY ERROR: {e}")
        logging.critical(f"Table integrity check failed: {e}. Program will exit.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Missing parameter. Please run the program with either 'encrypt' or 'decrypt'.")
        logging.error("Program was run without required parameters.")
    else:
        param = sys.argv[1].lower()
        if param == "encrypt":
            encrypt()
        elif param == "decrypt":
            decrypt()
        else:
            print(f"Unknown parameter '{param}'. Use 'encrypt' or 'decrypt'.")
            logging.error(f"Unknown parameter provided: '{param}'.")

    logging.info("Program finished.")


if __name__ == "__main__":
    main()
