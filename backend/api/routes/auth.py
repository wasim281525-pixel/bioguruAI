from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from models.database import get_db
from models.user import User
from config import settings
from api.middleware.auth_middleware import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    class_level: int = 11
    language: str = "en"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def create_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "class_level": user.class_level,
        "language": user.language,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@router.post("/register")
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=req.email,
        name=req.name,
        password_hash=pwd_context.hash(req.password),
        class_level=req.class_level,
        language=req.language,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(user.id), "name": user.name, "email": user.email,
                 "class_level": user.class_level, "role": user.role},
    }


@router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(user.id), "name": user.name, "email": user.email,
                 "class_level": user.class_level, "role": user.role},
    }


@router.get("/me")
async def me(user=Depends(get_current_user)):
    return user
