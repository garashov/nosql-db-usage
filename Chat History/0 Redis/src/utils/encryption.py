import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_word(word: str, key: bytes) -> str:
    """
    Encrypts a given word using AES in ECB mode.

    Args:
        word (str): The word to be encrypted.
        key (bytes): The AES encryption key (must be 16, 24, or 32 bytes long).

    Returns:
        str: The encrypted word as a base64-encoded string.
    """
    # Ensure the key is of proper length
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 16, 24, or 32 bytes long")

    # Initialize the cipher
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the word to be a multiple of the block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_word = padder.update(word.encode()) + padder.finalize()

    # Encrypt the padded word
    encrypted_word = encryptor.update(padded_word) + encryptor.finalize()

    # Return the encrypted word as a base64-encoded string
    return base64.b64encode(encrypted_word).decode()


def decrypt_word(encrypted_word: str, key: bytes) -> str:
    """
    Decrypts a given word using AES in ECB mode.

    Args:
        encrypted_word (str): The base64-encoded encrypted word to be decrypted.
        key (bytes): The AES encryption key (must be 16, 24, or 32 bytes long).

    Returns:
        str: The decrypted word.
    """
    # Ensure the key is of proper length
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 16, 24, or 32 bytes long")

    # Initialize the cipher
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decode the base64-encoded encrypted word
    encrypted_word_bytes = base64.b64decode(encrypted_word)

    # Decrypt the word
    padded_word = decryptor.update(encrypted_word_bytes) + decryptor.finalize()

    # Unpad the word
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    word = unpadder.update(padded_word) + unpadder.finalize()

    return word.decode()


# Example of usage
if __name__ == "__main__":
    key = b"TwdsadsadsaGTXAgYmiGW3URKaheufL="
    encrypted = encrypt_word("elnurqarashov@gmail.com", key)
    decrypted = decrypt_word(encrypted, key)
    print("Encryption:", encrypted)
    print("Decryption:", decrypted)
