from distutils.command.config import config
from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("EE_DB_URL", cast=str, default="")