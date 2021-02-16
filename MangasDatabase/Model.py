import re 

class Manga:
    
    def __init__(self, description, tags, name, link, img="") -> None:
        self.description = description
        self.tags = tags
        self.name = name
        self.link = link
        self.img = img

    def getDescriptonTokens(self):
        self.description_flags = {}
        for flag in re.split("\s",self.description):
            if not (self.description_flags.get(flag) == None) :
                self.description_flags[flag]+=1
                pass
            else :
                self.description_flags[flag] = 1
        return self.description_flags  

    def getTagsFlags(self):
        self.Tags_flags = {}
        for flag in str(self.tags).split("┴"):
            if not (self.Tags_flags.get(flag) == None) :
                self.Tags_flags[flag]+=1
                pass
            else :
                self.Tags_flags[flag] = 1
        return self.Tags_flags 