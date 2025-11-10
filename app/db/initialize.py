from app.db.database import Base, engine

def initialize_db():
    Base.metadata.create_all(bind=engine)