from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Define the connection string
DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost/sqlAlchemy_db'

# Create the database engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# Now you can use the 'engine' object to interact with the PostgreSQL database.

Session = sessionmaker(bind=engine)
