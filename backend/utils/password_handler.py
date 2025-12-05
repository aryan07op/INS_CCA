# backend/utils/password_handler.py
import hashlib
import os
import bcrypt

class PasswordHandler:
    @staticmethod
    def hash_without_salt(password: str) -> str:
        """Unsalted SHA-256 (insecure)"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return hashlib.sha256(password).hexdigest()

    @staticmethod
    def generate_salt(length: int = 16) -> str:
        """Return a cryptographically random salt as a hex string."""
        return os.urandom(length).hex()

    @staticmethod
    def hash_with_given_salt(password: str, salt_hex: str) -> str:
        """
        Hash with a provided salt (salt_hex is hex string).
        Returns hex digest of SHA-256(salt || password).
        """
        salt = bytes.fromhex(salt_hex)
        if isinstance(password, str):
            password_bytes = password.encode('utf-8')
        else:
            password_bytes = password
        return hashlib.sha256(salt + password_bytes).hexdigest()

    @staticmethod
    def hash_with_custom_salt(password: str) -> dict:
        """
        Generate a random salt, prepend to password and return { salt, hash }.
        salt: hex string, hash: sha256 hex digest.
        """
        salt_hex = PasswordHandler.generate_salt()
        hash_hex = PasswordHandler.hash_with_given_salt(password, salt_hex)
        return {'salt': salt_hex, 'hash': hash_hex}

    @staticmethod
    def hash_with_bcrypt(password: str, rounds: int = 12) -> dict:
        """
        Hash using bcrypt. Returns dict with 'salt' and 'hash' (both strings).
        Note: bcrypt.hashpw returns the full hash string which includes salt and cost.
        """
        if isinstance(password, str):
            password_bytes = password.encode('utf-8')
        else:
            password_bytes = password
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return {'salt': salt.decode('utf-8'), 'hash': hashed.decode('utf-8')}

    @staticmethod
    def verify_bcrypt(password: str, hashed: str) -> bool:
        """Verify a password against a bcrypt hash string."""
        if not hashed:
            return False
        if isinstance(password, str):
            password_bytes = password.encode('utf-8')
        else:
            password_bytes = password
        try:
            return bcrypt.checkpw(password_bytes, hashed.encode('utf-8'))
        except Exception:
            return False

    @staticmethod
    def simulate_rainbow_table_attack(target_hash_hex: str) -> dict:
        """
        Demo-only: check a small list of common passwords to 'crack' an unsalted sha256.
        Returns { found: bool, password: str | None }.
        """
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'letmein', 'welcome', 'admin', 'iloveyou', 'monkey'
        ]
        for candidate in common_passwords:
            candidate_hash = hashlib.sha256(candidate.encode('utf-8')).hexdigest()
            if candidate_hash == target_hash_hex:
                return {'found': True, 'password': candidate}
        return {'found': False, 'password': None}
