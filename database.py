from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Trabalhos(Base):
	__tablename__ = 'trabalhos'
	id = Column(Integer(), primary_key = True)	
	titulo = Column(String(255),)
	instituicao = Column(String(255),)
	programa = Column(String(255),)
	autor = Column(String(255),)
	tipo = Column(String(255),)
	data = Column(Date())
	resumo = Column(String(5000),)
	pavavras_chaves = Column(String(255),)
	abstract = Column(String(5000),)	