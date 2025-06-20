from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

oauth2_scheme = APIKeyHeader(name="Authorization")


def get_spotify_token_from_header(token: str = Depends(oauth2_scheme)):
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization header must start with 'Bearer '")
    return token.split(" ")[1]
