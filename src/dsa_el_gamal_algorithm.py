from security_algorithm import SecurityAlgorithm

class DSAElGamalAlgorithm (SecurityAlgorithm):
    def encrypt(self, plaintext, key) -> str:
        """Method for encryption using El Gamal"""
        return ""

    def decrypt(self, ciphertext, key) -> str:
        """Method for decryption using El Gamal"""
        return ""
    
    def sign(self, message, key) -> str:
        """Method for signature using DSA"""
        return ""
    
    def verify(self, message, key) -> bool:
        """Method for verifying signature using DSA"""
        return True