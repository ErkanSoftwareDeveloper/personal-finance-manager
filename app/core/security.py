from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    # plain text password is hashed using bcrypt algorithm
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # verify the plain text password against the hashed password
    return pwd_context.verify(plain_password, hashed_password)
