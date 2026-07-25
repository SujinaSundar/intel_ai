"""
Password hashing utilities.

Provides helper functions
for securely hashing and
verifying user passwords.
"""

from pwdlib import PasswordHash

# -----------------------------------------------------
# Password Hasher
# -----------------------------------------------------

password_hasher = PasswordHash.recommended()

# -----------------------------------------------------
# Password Hashing
# -----------------------------------------------------


def hash_password(
    password: str,
) -> str:
    """
    Hash a plain-text password.

    Parameters
    ----------
    password : str
        Plain-text password.

    Returns
    -------
    str
        Secure password hash.
    """

    return password_hasher.hash(password)


# -----------------------------------------------------
# Password Verification
# -----------------------------------------------------


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password
    against its stored hash.

    Parameters
    ----------
    password : str
        Plain-text password.

    hashed_password : str
        Stored password hash.

    Returns
    -------
    bool
        True if the password
        matches the stored hash,
        otherwise False.
    """

    return password_hasher.verify(
        password,
        hashed_password,
    )