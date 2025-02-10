from datetime import datetime, timedelta, timezone

from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
import requests

from auth.action import validate_user
from auth.utils import create_access_token, create_refresh_token
from crud.dependencies import get_user_crud
from crud.user import UserCRUD
from schemas.token import Token
from schemas.user import Create, DB
from setting.config import get_settings
from os import getenv
from msal import ConfidentialClientApplication

MS_TENANT_ID = str(getenv("MS_TENANT_ID"))
MS_CLIENT_ID =str(getenv("MS_CLIENT_ID"))
MS_CLIENT_SECRET = str(getenv("MS_CLIENT_SECRET"))
REDIRECT_URI = str(getenv("BACKEND_URL")) + "/oauth2-redirect"
AUTHORITY = "https://login.microsoftonline.com/" + MS_TENANT_ID
FRONTEND_URL = str(getenv("FRONTEND_URL"))

print("Authority: ", AUTHORITY)

app_instance = ConfidentialClientApplication(
    MS_CLIENT_ID, authority=AUTHORITY, client_credential=MS_CLIENT_SECRET
)

settings = get_settings()
router = APIRouter(tags=["auth"])
SCOPES = ["User.Read"]

@router.post("/superuser-login", response_model=Token)
async def superuser_login(
    response: Response,
    api_key: str,
    db: UserCRUD = Depends(get_user_crud),
):
    user: DB = await db.get_user_by_username("superuser")
    if not user:
        user: DB = db.create_user(Create(username="superuser", name="superuser"))
    
    superuser_api_key = settings.superuser_api_key
    if api_key != superuser_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    username = "superuser"
    access_token = await create_access_token(data={"username": username})
    refresh_token = await create_refresh_token(data={"username": username})

    db.update_user_login(username)
    expires_at = (datetime.now() + timedelta(minutes=settings.refresh_token_expire_minutes)).timestamp()

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        path="/",  # Explicitly set path
        domain="localhost"
    )

    return Token(
        access_token=access_token,
        expires_in=int(expires_at),
        token_type="Bearer",
    )

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    api_key: str,
    db: UserCRUD = Depends(get_user_crud),
):
    return "depricated"

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="strict",
        secure=False,
        expires=timedelta(settings.refresh_token_expire_minutes),
    )

    return Token(
        access_token=access_token,
        expires_in=expired_time,
        token_type="Bearer",
    )


@router.post("/refresh", response_model=Token)
async def refresh(
    request: Request,
    response: Response,
    db: UserCRUD = Depends(get_user_crud),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(detail="No refresh token", status_code=401)
        
        payload = jwt.decode(
            refresh_token,
            settings.refresh_token_secret,
            algorithms=["HS256"],
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

    except Exception as e:
        credentials_exception.detail = str(e)
        raise credentials_exception

    access_token = await create_access_token(data={"username": username})
    new_refresh_token = await create_refresh_token(data={"username": username})

    db.update_user_login(username)
    expires_at = (datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)).timestamp()

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        path="/",  # Explicitly set path
        domain="localhost"
    )

    return Token(
        access_token=access_token,
        expires_in=int(expires_at),
        token_type="Bearer",
    )

@router.get("/check-cookie")
async def check_cookie(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        return {"message": "Cookie is set!", "refresh_token": refresh_token}
    return {"message": "No cookie found"}

@router.get("/ms/login")
async def ms_login():
    print(REDIRECT_URI)
    auth_url = app_instance.get_authorization_request_url(
        SCOPES, redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(url=auth_url)


@router.get("/oauth2-redirect")
async def auth_callback(response: Response, request: Request, db: UserCRUD = Depends(get_user_crud)):
    code = request.query_params.get("code")
    
    result = app_instance.acquire_token_by_authorization_code(
        code, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    
    if "access_token" in result:
        access_token = result["access_token"]
        print(access_token)
        
        headers = {"Authorization": f"Bearer {access_token}"}
        user_data = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
        
        preferred_username = user_data.get("userPrincipalName")  # Or use "mail" if preferred
        displayName = user_data.get("displayName")
        print(f"preferred_username: {preferred_username}")
        user_create = Create(username=preferred_username, name=displayName)
        if not await db.get_user_by_username(preferred_username):
            await db.create_user(user_create)

        access_token_project = await create_access_token(data={"username": preferred_username})
        refresh_token = await create_refresh_token(data={"username": preferred_username})

        print(refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            path="/",  # Explicitly set path
            domain="localhost"
        )

        # Debugging: Print response headers
        print(response.headers)

        return JSONResponse(
            content={"access_token": access_token_project, "redirect_url": f"{FRONTEND_URL}/login"},
            status_code=200
        )
    return JSONResponse({"error": "Authentication failed"})


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logout successfully"}
