from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
    status,
    BackgroundTasks,
    UploadFile,
    File,
)
from slowapi import Limiter
from slowapi.util import get_remote_address


from src.conf.config import settings
from src.core.depend_service import (
    get_auth_service,
    get_user_service,
    get_admin_user,
)
from src.core.email_token import get_email_from_token
from src.core.security import verify_access_token
from src.entity.models import User
from src.schemas.email import RequestEmail
from src.schemas.user import UserResponse, RequestPasswordReset, ResetPassword
from src.services.auth import AuthService, oauth2_scheme
from src.services.email import send_verification_email, send_password_reset_email
from src.services.upload_file_service import UploadFileService
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=UserResponse)
@limiter.limit("10/minute")
async def me(
    request: Request,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(token)


@router.get("/confirmed_email/{token}")
async def confirmed_email(
    token: str, user_service: UserService = Depends(get_user_service)
):
    email = get_email_from_token(token)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await user_service.confirmed_email(email)
    return {"message": "Email confirmed successfully"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_email(str(body.email))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    
    background_tasks.add_task(
        send_verification_email,
        user.email,
        user.username,
        str(request.base_url)
    )
    return {"message": "Verification email sent successfully"}


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar_user(
    file: UploadFile = File(),
    user: User = Depends(get_admin_user),
    user_service: UserService = Depends(get_user_service),
):
    avatar_url = UploadFileService(
        settings.CLD_NAME, settings.CLD_API_KEY, settings.CLD_API_SECRET
    ).upload_file(file, user.username)

    user = await user_service.update_avatar_url(user.email, avatar_url)
    return user


@router.post("/request-password-reset")
async def request_password_reset(
    body: RequestPasswordReset,
    background_tasks: BackgroundTasks,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    token = await user_service.create_password_reset_token(body.email)
    if token:
        reset_url = f"{str(request.base_url)}users/reset-password/{token}"
        background_tasks.add_task(
            send_password_reset_email,
            body.email,
            reset_url
        )
    return {"message": "Password reset email sent successfully"}


@router.post("/reset-password/{token}")
async def reset_password(
    token: str,
    body: ResetPassword,
    user_service: UserService = Depends(get_user_service),
):
    try:
        token_data = verify_access_token(token)
        if token_data.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
        email = token_data.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
        
        user = await user_service.reset_password(email, body.new_password)
        return {"message": "Password reset successfully"}
    
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )