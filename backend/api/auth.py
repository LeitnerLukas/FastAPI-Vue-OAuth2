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
from schemas.user import Create
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


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: UserCRUD = Depends(get_user_crud),
):
    return "deprecated"
    user = await validate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"username": form_data.username})
    refresh_token = await create_refresh_token(data={"username": form_data.username})

    await db.update_user_login(username=form_data.username)
    expired_time = (
        int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        + timedelta(minutes=settings.access_token_expire_minutes).seconds * 1000
    )

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
    return "deprecated"
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise credentials_exception

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
    refresh_token = await create_refresh_token(data={"username": username})

    db.update_user_login(username)
    expired_time = (
        int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        + timedelta(minutes=settings.access_token_expire_minutes).seconds * 1000
    )

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

@router.get("/ms/login")
async def ms_login():
    print(REDIRECT_URI)
    auth_url = app_instance.get_authorization_request_url(
        SCOPES, redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(url=auth_url)


@router.get("/oauth2-redirect")
async def auth_callback(request: Request, db: UserCRUD = Depends(get_user_crud),):
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

        user_create = Create(username=preferred_username, name=preferred_username)
        db.create_user(user_create)

        access_token_project = await create_access_token(data={"sub": preferred_username})      
        return RedirectResponse(url=f"{FRONTEND_URL}/login?access_token={access_token_project}")
    
    return JSONResponse({"error": "Authentication failed"})


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logout successfully"}
