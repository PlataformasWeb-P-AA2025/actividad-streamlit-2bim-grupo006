# db.py
from sqlalchemy.orm import sessionmaker
from clases2 import engine
from config2 import cadena_base_datos2

# Creamos el sessionmaker
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    """
    Retorna una nueva sesión de SQLAlchemy.
    """
    return SessionLocal()
