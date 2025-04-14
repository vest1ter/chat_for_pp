from fastapi import Response
from core.config import settings


def set_cookie(response: Response, key: str, value: str, max_age: int, samesite: str = "Lax", secure: bool = False):
    response.set_cookie(
        key=key,
        value=f"Bearer {value}",
        httponly=True,
        max_age=max_age,
        expires=max_age,
        samesite=samesite,
        secure=secure
    )
def set_auth_cookie(response: Response, access_token: str, refresh_token: str):
    set_cookie(response, "access_token", access_token, settings.jwt.access_token_exp_minutes * 60)
    set_cookie(response, "refresh_token", refresh_token, settings.jwt.refresh_token_expire_days * 24 * 60 * 60)
