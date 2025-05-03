import random
import string
from django.contrib.auth.hashers import make_password

def generate_password(length=8):
    """Generates a random password"""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))

def assign_login_id(user, prefix):
    """Assigns a unique Login ID (e.g., P00001 for Parents, T00001 for Teachers)"""
    if not user.login_id:
        user.login_id = f"{prefix}{user.id:05d}"
        user.password = make_password(generate_password())  # Hash Password
        user.save()
