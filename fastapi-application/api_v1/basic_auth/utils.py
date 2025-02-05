import secrets
import uuid
from typing import Annotated
from fastapi import Depends, HTTPException, status, Header, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic


security = HTTPBasic()

# an example of pass/tokens with out data base
user_name_and_pass_EXAMPLE = \
    {
        "admin":"adminpass",
        "John": "superpassw"
    }

user_name_and_token_EXAMPLE = \
    {
        "d5623277b5d85a7e220bcdd84f6": "admin",
        "41dc1cc8e5d8527f1a4f5d2619d": "John"
    }

COOKIES: dict[str, dict[str]] = {}
COOKIES_SESSION_ID_KEY = "web-app-session-id"

# an example of pass/tokens with out data base


def get_auth_user_basic(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print("type", type(credentials))
    print(credentials)
    return credentials


def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

    unauth_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid username or password",
                                    headers={"WWW-Authenticate": "Basic"}
    )

    if credentials.username not in user_name_and_pass_EXAMPLE.keys():
        raise unauth_exeption

    user_password = user_name_and_pass_EXAMPLE[credentials.username]

    # for password better to use secrets module, avoid Time attack

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        user_password.encode("utf-8")
    ):
        raise unauth_exeption

    return credentials.username



def get_auth_user_by_static_token(
        #static_token: str = Header(alias="static-auth-token")
        static_token: str = Header(alias="x-auth-token")
) -> str:

    unauth_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid token",)

    if static_token not in user_name_and_token_EXAMPLE:
        raise unauth_exeption

    return user_name_and_token_EXAMPLE[static_token]


# generate id session for cookies
def generate_session_id() -> str:
    return uuid.uuid4().hex

def get_session_data(
    session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY)
) -> dict:
    if session_id not in COOKIES.keys():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return COOKIES[session_id]