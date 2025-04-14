from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

print(hash_password("user1"))
print(hash_password("user2"))