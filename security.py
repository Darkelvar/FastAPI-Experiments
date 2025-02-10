from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "504095cd2d2d166d03aa0023d7d73eef5b321af2c0abf813dadb825a84df155d"
ALGORITHM = "HS256"

fake_users_db = {
    "mikewazowski": {
        "username": "mikewazowski",
        "full_name": "Mike Wazowski",
        "password": "$2b$12$tRq.ciSB6WUriUlV3EtC7OC2kcVV3B2EvKna8tVZXfw5XvuPs9njC",  # strongpassword123
        "disabled": False,
    },
}


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        bytes(plain_password, encoding="utf-8"),
        bytes(hashed_password, encoding="utf-8"),
    )


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_minutes: int | None = None):
    to_encode = data.copy()
    if not expires_minutes:
        expires_minutes = 15
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
