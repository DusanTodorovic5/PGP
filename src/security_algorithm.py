class SecurityAlgorithm:
    def encrypt(self, plaintext, key) -> str:
        """Virtual method for encryption"""
        return ""

    def decrypt(self, ciphertext, key) -> str:
        """Virtual method for decryption"""
        return ""
    
    def sign(self, message, key) -> str:
        """Virtual method for signing message"""
        return ""
    
    def verify(self, message, key) -> bool:
        """Virtual method for verifying signature"""
        return True