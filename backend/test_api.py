import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("YOUTUBE_API_KEY"))