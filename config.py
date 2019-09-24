import os

# Importing PostgreSQL configuration from environment variables

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']

# Database connection string using psycopg2 adapter

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
