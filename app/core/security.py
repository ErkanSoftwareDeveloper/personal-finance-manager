from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

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


SECRET_KEY = "change_this_secret_key_later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
