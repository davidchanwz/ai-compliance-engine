import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Secret key for signing JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30