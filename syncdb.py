from enum import Flag
from MangasDatabase.DB import DB
from Models.DB import *
#description, tags, name, link, img=""
Database = DB.getDB()
for manga in Database.MangaList:
    m_atual = Manga(Nome=manga.name, Img=manga.img, Description=manga.description)
    session.add(m_atual)
    for flag in manga.getTagsFlags():
        session.add(Tag(Nome=flag,Manga=m_atual.id))
    
    pass
session.commit()