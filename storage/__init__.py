from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqldb://root@localhost:3306/db_trabalho3B')
SessionLocal = sessionmaker(bind=engine) #Cria seções temporárias para fazer alterações, para cada usuário  


class Base(DeclarativeBase):
    pass

def obter_sessao():
    return SessionLocal()