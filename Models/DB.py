from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
#importar o campo ForeignKey e o relationship para fazer relaçoes entre tabelas
from sqlalchemy import Column, Integer, String, TEXT , ForeignKey 
from sqlalchemy.orm import relationship

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer,primary_key=True)
    Nome = Column(String)
    Manga_id = Column(Integer, ForeignKey('mangas.id'))

class Manga(Base):
    __tablename__ = 'mangas'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    Nome = Column(String)
    Img = Column(String(4000))
    Description = Column(TEXT)
    Link = Column(String(4000))
    Tags = relationship(Tag)


#precisa instalar o psycopg2
#criando Engine
Engine = create_engine('postgres://rrvznwyffrnnwy:c36ce11cdeff5bc46869e8ce2f58c08dc797e76568d547e961eb72440661185b@ec2-52-7-115-250.compute-1.amazonaws.com:5432/d9u1tdvdr7v3nh')
Base.metadata.create_all(Engine)

Session_class = sessionmaker(bind=Engine)
session = Session_class()

