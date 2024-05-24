from cryptography.fernet import Fernet
import base64
import hashlib
from datetime import datetime
from .models import db, Item

def check_tasks():
        now = datetime.now()
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        print(formatted_date)
        tasks = Item.query.all() 
        for task in tasks:
            if datetime.strptime(task.date_livraison, "%Y-%m-%d") < now and task.status != 'Terminée' and task.status != 'En retard':
                task.status = 'En retard'
                db.session.commit()

def generate_key(common_password: str) -> bytes:
            # Hash le mot de passe commun pour obtenir une clé de 32 bytes
            key = hashlib.sha256(common_password.encode()).digest()
            # Encode la clé en base64 pour l'utiliser avec Fernet
            return base64.urlsafe_b64encode(key)
        
def encrypt_password(password: str, common_password: str) -> str:
            key = generate_key(common_password)
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(password.encode())
            return encrypted_password.decode()

def decrypt_password(encrypted_password: str, common_password: str) -> str:
            key = generate_key(common_password)
            fernet = Fernet(key)
            decrypted_password = fernet.decrypt(encrypted_password.encode())
            return decrypted_password.decode()