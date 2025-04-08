from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.pool import NullPool
from decouple import config

POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PW = config('POSTGRES_PASSWORD')
POSTGRESQL_HOST = config('POSTGRES_SERVER')
POSTGRESQL_PORT = config('POSTGRES_PORT')
POSTGRES_DB = config('POSTGRES_DB')


DB_URL = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'. \
    format(user=POSTGRES_USER, pw=POSTGRES_PW, host=POSTGRESQL_HOST, db=POSTGRES_DB, port=POSTGRESQL_PORT)
engine = create_engine(DB_URL, echo=False, poolclass=NullPool, isolation_level='READ UNCOMMITTED')
mapper_registry = orm.registry()
Base = mapper_registry.generate_base()
