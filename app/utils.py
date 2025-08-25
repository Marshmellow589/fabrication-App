# Generic utility functions that don't belong to specific domain
# Keep this file for truly cross-cutting utilities
from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format datetime for consistent display"""
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

def generate_random_string(length: int = 8) -> str:
    """Generate random string for temporary IDs"""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def validate_email_format(email: str) -> bool:
    """Basic email format validation"""
    import re
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None
