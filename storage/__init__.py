from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqldb://root@localhost:3307/db_trabalho3B')
SessionLocal = sessionmaker(bind=engine) #Cria seções temporárias para fazer alterações, para cada usuário  

def obter_sessao():
    return SessionLocal()