from time import time

from fastapi import APIRouter, Depends, Response, HTTPException, status, Header, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api_v1.basic_auth.utils import get_auth_user_username, get_auth_user_by_static_token, get_auth_user_basic, \
    generate_session_id, COOKIES, COOKIES_SESSION_ID_KEY, get_session_data

router = APIRouter(prefix="/demo-auth", tags=["Basic Auth"])


# Basic Auth fast api
@router.get("/basic_auth/")
def demo_basic_auth_credentials(
        credentials: HTTPBasicCredentials = Depends(get_auth_user_basic)):  # add Http basic func as authorisation

    return {
        "msg": "Auth success",
        "username": credentials.username,
        "password": credentials.password,
    }


@router.get("/basic_auth_username/")
def demo_basic_auth_username(
        auth_username: str = Depends(get_auth_user_username)):
    return {
        "msg": f"Auth success, hi {auth_username}",
        "username": auth_username,
    }


# Token Auth
@router.get("/basic_http_token_header/")
def demo_auth_http_token_header(
        auth_username: str = Depends(get_auth_user_by_static_token)):
    return {
        "msg": f"Auth with token success, hi {auth_username}",
        "username": auth_username,
    }


# Cookie Auth

@router.post("/login_cookie/")
def demo_auth_login_cookie(
        response: Response,
        auth_username=Depends(get_auth_user_username)
):
    session_id = generate_session_id()
    response.set_cookie(COOKIES_SESSION_ID_KEY, session_id)
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": float(time())
    }
    return {"msg": f"cookie Auth success, hi {auth_username}", }


@router.get("/check_cookie/")
def demo_auth_check_cookie(
        user_session_data: dict = Depends(get_session_data)
):
    username = user_session_data["username"]
    return {
        "msg": f"hello {username}",
        **user_session_data,
    }

@router.post("/logout_cookie/")
def demo_auth_logout_cookie(
        response: Response,
        session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY),
        user_session_data: dict = Depends(get_session_data)
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIES_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {"msg": f"cookie logout success, hi {username}", }