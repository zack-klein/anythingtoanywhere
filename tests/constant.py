from uuid import uuid4

from dotenv import load_dotenv
from faker import Faker

load_dotenv()
FAKE = Faker()
RUN_ID = str(uuid4())
