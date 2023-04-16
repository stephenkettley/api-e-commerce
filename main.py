from src.database.database_connection import Base, engine

Base.metadata.create_all(bind=engine)  # creates the tables in postgres
