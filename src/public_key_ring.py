import time

class PublicKeyRing:
    def __init__(self, public_key, email) -> None:
        self.timestamp = time.time()
        self.id = public_key[:-8]
        self.public_key = public_key
        self.owner_trust = None
        self.user_id = email
        self.key_legitimacy = None
        self.signature = None
        self.signature_trust = None