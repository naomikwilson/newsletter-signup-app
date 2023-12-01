import hashlib


def password_verification(password, hashed):
    """
    Return True if password is equivalent to hashed version
    """
    if hash_password(password) == hashed:
        return True
    else:
        return False


def hash_password(password):
    """
    Hash password
    """
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

def main():
    example_password = "banana" # Entered by user; not stored in database
    # Hash equivalent stored in the database
    stored_hash_password = "b493d48364afe44d11c0165cf470a4164d1e2609911ef998be868d46ade3de4e"
    print(password_verification(example_password, stored_hash_password)) # True

    false_example_password = "apple"
    print(password_verification(false_example_password, stored_hash_password)) # False


main()
