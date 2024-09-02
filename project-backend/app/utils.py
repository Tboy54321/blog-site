from passlib.context import CryptContext
from passlib.exc import UnknownHashError

# Initialize CryptContext for handling password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """
    Hash a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verify if a plaintext password matches the hashed password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plaintext password matches the hashed password, otherwise False.

    Raises:
        UnknownHashError: If the hashed password is not recognized or has an invalid format.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError as e:
        print(e)