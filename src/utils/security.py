import bcrypt

def generate_salt():
    """
    Generates a random salt using bcrypt.
    """
    return bcrypt.gensalt()

def create_password_hash(password, salt):
    """
    Creates a hash of the password using the provided salt.

    :param password: The password to be hashed.
    :param salt: The salt to be used in the hashing process.
    :return: The hash of the password.
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8') 

def verify_password(password, password_hash):
    """
    Verifies if the provided password matches the stored password hash.

    :param password: The password to be verified.
    :param password_hash: The stored hash of the original password.
    :return: True if the password matches the hash, False otherwise.
    """
    password_bytes = password.encode('utf-8')
    password_hash_bytes = password_hash.encode('utf-8')  # Certifique-se de que o hash também esteja em bytes
    return bcrypt.checkpw(password_bytes, password_hash_bytes)


