from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
import base64
from cryptography.fernet import Fernet

class User(AbstractUser):
    face_encoding = models.BinaryField(null=True, blank=True)
    face_encoding_key = models.BinaryField(null=True, blank=True)
    
    def set_face_encoding(self, encoding):
        """
        Encrypt and store face encoding
        """
        if encoding is not None:
            # Generate a unique encryption key for this user's face data
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            # Convert numpy array to bytes and encrypt
            encoded_data = base64.b64encode(encoding.tobytes())
            encrypted_data = cipher_suite.encrypt(encoded_data)
            
            self.face_encoding = encrypted_data
            self.face_encoding_key = key
    
    def get_face_encoding(self):
        """
        Decrypt and return face encoding
        """
        if self.face_encoding and self.face_encoding_key:
            cipher_suite = Fernet(self.face_encoding_key)
            decrypted_data = cipher_suite.decrypt(self.face_encoding)
            return base64.b64decode(decrypted_data)
        return None

    class Meta:
        db_table = 'auth_user'
        app_label = 'accounts'
