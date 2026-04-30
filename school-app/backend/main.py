import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    decode_token,
    hash_password,
    validate_nhps_email,
    verify_password,
)
from database import Base, engine, get_db
from models import User, UserRole
from schemas import Token, UserCreate, UserLogin, UserOut

load_dotenv()

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NHPS School App")

# ── CORS ──────────────────────────────────────────────────────────────────────
# Add your Netlify URL here once deployed, e.g. "https://nhps-app.netlify.app"
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://clementeleadershipacadamy.netlify.app/",  # ← replace with your real Netlify URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "NHPS API is running"}


@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Validate NHPS email format
    valid, role = validate_nhps_email(user.email)
    if not valid:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only NHPS email addresses are allowed. "
                "Students: 123456@nhps.net | Staff: firstname.lastname@nhps.net"
            ),
        )

    # Check password length
    if len(user.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters."
        )

    # Check if email already registered
    existing = db.query(User).filter(User.email == user.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="This email is already registered.")

    # Create user
    new_user = User(
        email=user.email.lower(),
        hashed_password=hash_password(user.password),
        role=UserRole(role),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "role": role})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email.lower()).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_access_token({"sub": db_user.email, "role": db_user.role.value})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=UserOut)
def get_me(token: str, db: Session = Depends(get_db)):
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user
