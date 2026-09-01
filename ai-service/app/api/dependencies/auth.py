import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config.settings import get_settings
from app.domain.models.current_user import CurrentUser

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:

    settings = get_settings()
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=["HS256"],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )

        # User ID
        user_id = payload.get(
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"
        )

        # Username
        username = payload.get(
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"
        )

        # Email
        email = payload.get(
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
        )

        # Role
        role = payload.get(
            "http://schemas.microsoft.com/ws/2008/06/identity/claims/role"
        )

        # Make sure all required claims exist
        if not user_id or not username or not email or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Required user information not found in token",
            )

        return CurrentUser(
            user_id=int(user_id),
            username=username,
            email=email,
            role=role,
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
