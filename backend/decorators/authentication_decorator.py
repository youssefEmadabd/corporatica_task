import os, jwt
from functools import wraps
from typing import Any, Dict, Optional
from flask import request
from http import HTTPStatus
from jose import JWTError

from backend.utilities.api_exception import APIException

secret_key = os.environ.get("JWT_SECRET")
hashing_algorithm = os.environ.get("HASHING_ALGORITHM")

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=[hashing_algorithm])
        return payload
    except JWTError:
        raise APIException(status_code=HTTPStatus.UNAUTHORIZED, message="Invalid token")


def protected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None

        # Check if token is in the request headers
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            raise APIException(status_code=401, message="Unauthorized access")

        token = token[len("Bearer "):]  # Remove "Bearer " prefix
        payload = decode_token(token)  # Validate the token
        return func(payload=payload, *args, **kwargs)
    return wrapper
