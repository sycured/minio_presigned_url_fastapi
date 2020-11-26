"""Config used by minio client."""

from distutils.util import strtobool
from os import getenv


access_key: str = getenv(key='MINIO_ACCESS_KEY', default='minio')
endpoint: str = getenv(key='MINIO_ENDPOINT', default='127.0.0.1:9000')
secret_key: str = getenv(key='MINIO_SECRET_KEY', default='miniominio')
ssl: bool = strtobool(getenv(key='MINIO_SSL', default='true'))
