from security_algorithm import SecurityAlgorithm

class DSAElGamalAlgorithm (SecurityAlgorithm):
    def encrypt(self, plaintext, key) -> str:
        """Method for encryption using RSA"""
        return ""

    def decrypt(self, ciphertext, key) -> str:
        """Method for decryption using RSA"""
        return ""
    
    def sign(self, message, key) -> str:
        """Method for signature using RSA"""
        return ""
    
    def verify(self, message, key) -> bool:
        """Method for verifying signature using RSA"""
        return True