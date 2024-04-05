from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
import bcrypt

ALGORITHM = "HS256"

def create_access_token(
    subject: Union[str, Any], expire: datetime, secret_key: str
) -> str:
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    #return pwd_context.verify(plain_password, hashed_password)
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    #return pwd_context.hash(password)
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
