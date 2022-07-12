import pickle as pickle
from MangasDatabase.Model import Manga

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename) :
    with open(filename, 'rb') as input:  # Overwrites any existing file.
        return pickle.load(input)



class DB:
    storage = "MangasDatabase/"
    formate = ".pkl"
    DBinstance = None
    @staticmethod
    def getDB():
        if not DB.DBinstance == None :
            return DB.DBinstance
        else :
            DB.DBinstance = DB()
            return DB.DBinstance

    def __init__(self) -> None:
        self.mapName = {}
        self.mapUrl = {}

        self.MangaList = []
        listFile = None

        try:
            listFile = open(DB.storage+"Mangas"+DB.formate,'rb')
        except IOError:
            listFile = None
        
        if listFile == None:
            save_object(self.MangaList,DB.storage+"Mangas"+DB.formate)
        else:
            listFile.close()
            self.MangaList = load_object(DB.storage+"Mangas"+DB.formate)
            self.update(save=False)
            
    def update(self, save = True):
        if save: 
            save_object(self.MangaList,DB.storage+"Mangas"+DB.formate)
        for obj in self.MangaList:
            self.mapName[obj.name] = obj
            self.mapUrl[obj.link] = obj
            pass
    
    def addManga(self, obj):
        self.MangaList.append(obj)
        self.update()
    
    def ReinterpretClass(self):
        newVector = []
        for map in self.MangaList:
            newVector.append(Manga(map.description,map.tags,map.name,map.link))
        self.MangaList = newVector
        self.update()
    
    def findManga(self, name=None, url=None):
        if name:
            if not self.mapName.get(name) == None :
                return self.mapName[name]
        if url:
            if not self.mapUrl.get(url) == None :
                return self.mapUrl[url]
        return None