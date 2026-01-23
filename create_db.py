from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db
from urllib.parse import quote_plus
from models import Customer, Group, BaseStock, LatheStock
from make_dummy_data import generate

# Postgres connection string
PW = quote_plus('temp')
DATABASE_URL = f"postgresql+psycopg2://noahsolomon:{PW}@10.0.0.122:5432/workflux"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)
print(engine.url)

# Optional session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create all tables
db.Model.metadata.drop_all(bind=engine)
db.Model.metadata.create_all(bind=engine)

# Create some dummy data
generate(10)

print("Tables created successfully!")