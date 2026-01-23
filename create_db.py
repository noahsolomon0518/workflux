from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db
from urllib.parse import quote_plus
from models import Customer, Group, BaseStock, LatheStock
from make_dummy_data import generate

# Postgres connection string
DATABASE_URL = f"postgresql://noahsolomon:Mqv4ZJXyFzsphw1B9sX5sImVx29OJZpJ@dpg-d5pee6p4tr6s73aq6qng-a.oregon-postgres.render.com/workflux"

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