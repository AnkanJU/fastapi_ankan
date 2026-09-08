from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from app.config import settings
from app.database import get_db
from app.models import DBUser
from app.schemas import TokenData

# OAuth2 scheme points FastAPI's Swagger UI to the login URL for token authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> DBUser:
    """Extracts JWT token, validates payload, and fetches the current user from DB."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token payload
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception

    # Query user from DB
    user = db.query(DBUser).filter(DBUser.email == token_data.email).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_current_active_user(
    current_user: DBUser = Depends(get_current_user)
) -> DBUser:
    """Ensures the authenticated user is marked as active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user
    