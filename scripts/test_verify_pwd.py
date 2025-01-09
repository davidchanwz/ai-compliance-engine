from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = "$2b$12$RhARjF0pbLSDI8HfOVVVcOLAksd0B7nPHHhWIFMzLU84eeyxClVcG"
assert pwd_context.verify("password", hashed_password)
print("Password verification passed")