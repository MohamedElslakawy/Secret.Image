#Version 1.0
#Author: Mohamed Elslakawy
#this class is responsible for managing the encryption and decryption of the data using AES encryption
import os
# Import the Fernet class from the cryptography library for symmetric encryption and decryption
from cryptography.fernet import Fernet


class EncryptionManager:
    def __init__(self, key=None):
        self.key = key if key else Fernet.generate_key()  # Generate a random key if not provided
        self.cipher = Fernet(self.key)  # Initialize the Fernet cipher
    
    # Encrypt the plain text using Fernet encryption to cipher text
    def encrypt_text(self, plain_text: str) -> bytes:
        
        return self.cipher.encrypt(plain_text.encode('utf-8'))
    
    # Decrypt the cipher text using Fernet decryption to plain text
    def decrypt_text(self, ciphertext) -> str:
        return self.cipher.decrypt(ciphertext).decode('utf-8')
    
    # Get the encryption key used for encryption and decryption
    def get_key(self) -> bytes:
        return self.key
    
   
