from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.dependencies import get_db
from app.repositories.user import UserRepository
from app.schemas.user import LoginRequest, Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    # Check username not already taken
    existing_username = await repo.get_by_username(user.username)
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already taken")

    # Check email not already registered
    existing_email = await repo.get_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already registered")

    return await repo.create(user)


@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    # Find the user
    user = await repo.get_by_username(credentials.username)

    # Deliberately vague error — don't tell attacker if username exists
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Check account is active
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    # Create and return token
    token = create_access_token(
        {"sub": str(user.id), "username": user.username, "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}
