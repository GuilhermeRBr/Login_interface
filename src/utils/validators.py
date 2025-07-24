import re
import random
import string

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_length(password: str, min_length: int = 6) -> bool:
    return len(password) >= min_length

def passwords_match(password: str, confirm_password: str) -> bool:
    return password == confirm_password

def generate_verification_code(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))