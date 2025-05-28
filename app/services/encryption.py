from cryptography.fernet import Fernet
import logging
import base64

logger = logging.getLogger(__name__)


class EncryptionService:
    def __init__(self, key: str = None):
        if key:
            # Ensure key is valid Fernet key
            try:
                # Try to decode the key to ensure it's valid base64
                key_bytes = key.encode()
                Fernet(key_bytes)
                self.key = key
                logger.debug(f"Using provided key: {key[:10]}...")
            except Exception as e:
                logger.error(f"Invalid key provided: {str(e)}", exc_info=True)
                # If key is invalid, generate a new one
                self.key = Fernet.generate_key().decode()
                logger.info("Generated new key due to invalid provided key")
        else:
            # Generate a new key if none provided
            self.key = Fernet.generate_key().decode()
            logger.info("Generated new key")

    def encrypt(self, text: str) -> str:
        """Encrypt a string and return the encrypted bytes as a string."""
        if not text:
            logger.warning("Attempted to encrypt empty text")
            return None
        try:
            # Create Fernet instance with the key
            cipher_suite = Fernet(self.key.encode())
            # Encrypt the text
            encrypted_bytes = cipher_suite.encrypt(text.encode())
            # Convert to base64 string for storage
            encrypted_str = base64.b64encode(encrypted_bytes).decode()
            logger.debug(f"Successfully encrypted text of length {len(text)}")
            return encrypted_str
        except Exception as e:
            logger.error(f"Error encrypting: {str(e)}", exc_info=True)
            logger.error(f"Using key: {self.key[:10]}...")
            return None

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt an encrypted string and return the original string."""
        if not encrypted_text:
            logger.warning("Attempted to decrypt empty text")
            return None
        try:
            # Create Fernet instance with the key
            cipher_suite = Fernet(self.key.encode())

            # Handle base64 padding
            try:
                # First try direct decoding
                encrypted_bytes = base64.b64decode(encrypted_text.encode())
            except Exception as e:
                logger.debug(f"Direct base64 decoding failed: {str(e)}, trying with padding")
                # If that fails, try adding padding
                padding = 4 - (len(encrypted_text) % 4)
                if padding == 4:
                    padding = 0
                padded_text = encrypted_text + ('=' * padding)
                try:
                    encrypted_bytes = base64.b64decode(padded_text.encode())
                    logger.debug("Successfully decoded base64 with padding")
                except Exception as e:
                    logger.error(f"Failed to decode base64 even with padding: {str(e)}")
                    logger.error(f"Using key: {self.key[:10]}...")
                    return None

            # Decrypt the text
            decrypted_bytes = cipher_suite.decrypt(encrypted_bytes)
            decrypted_text = decrypted_bytes.decode()
            logger.debug(f"Successfully decrypted text of length {len(decrypted_text)}")
            return decrypted_text
        except Exception as e:
            logger.error(f"Error decrypting: {str(e)}", exc_info=True)
            logger.error(f"Using key: {self.key[:10]}...")
            return None