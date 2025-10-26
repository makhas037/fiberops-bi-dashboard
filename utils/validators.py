import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not email:
        return False, "Email is required"
    if not re.match(pattern, email):
        return False, "Invalid email address"
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""


def validate_file_type(filename: str, allowed: list) -> Tuple[bool, str]:
    if not filename:
        return False, "Filename required"
    ext = filename.lower().split('.')[-1]
    if ext not in [a.lstrip('.').lower() for a in allowed]:
        return False, f"Invalid file type: .{ext}"
    return True, ""


def validate_file_size(size_bytes: int, max_mb: int) -> Tuple[bool, str]:
    if size_bytes is None:
        return False, "Invalid file size"
    if size_bytes > max_mb * 1024 * 1024:
        return False, f"File exceeds {max_mb} MB limit"
    return True, ""
