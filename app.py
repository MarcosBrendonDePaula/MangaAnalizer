import os
import cloudscraper
import time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

from MangasDatabase.DB import *

Database = DB.getDB()

def syncLink(link=""):
        session = cloudscraper.create_scraper(browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        })
        temp = Database.findManga(url=link)
        if temp == None:
            success = False
            sleepTime = 0
            while not success:
                try:
                    if sleepTime>15:
                        print("Forced:", link)
                        success=True
                        session = cloudscraper.create_scraper(browser={
                            'browser': 'firefox',
                            'platform': 'windows',
                            'mobile': False
                        })
                        break

                    manga_page = session.get(link, headers=headers)

                    Soup_manga = BeautifulSoup(manga_page.text, 'html.parser')
                    image = Soup_manga.find(class_="img-thumbnail")['src']
                    name = Soup_manga.find(class_="tamanho-bloco-perfil").findAll(class_="row")[0].find("h2").get_text()
                    generos = ""
                    for genero in Soup_manga.find_all(class_="media-heading")[1].find_all("a"):
                        generos+="┴"+genero.get_text()
                    
                    sinopse = Soup_manga.find(class_="panel-body").get_text()
                    print(link ,name , generos)
                    manga = Manga(sinopse,generos,name,link,image)
                    Database.addManga(manga)
                    success = True
                    return manga
                except Exception as e:
                    print("erro:" , e)
                    print("Dromindo por:",sleepTime,"para: ",link)
                    time.sleep(sleepTime)
                    sleepTime += 5
                    success = False
                    pass
        else:
            return temp

def getPages():
    unionLink = "https://unionmangas.top/lista-mangas/a-z/{page}/*"
    MaxPages = 317
    ActualPage = 0
    session = cloudscraper.create_scraper(browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        })
    for it in range(ActualPage,MaxPages):
        ActualPage = session.get(unionLink.format(page=it))
        
        Soup = BeautifulSoup(ActualPage.text, 'html.parser')
        
        Blocos_manga = Soup.findAll(class_="lista-mangas-novos")
        for ActualManga in Blocos_manga:
            name = ActualManga.findAll('a')[1].get_text()
            link = ActualManga.findAll('a')[1]['href']
            temp = Database.findManga(name=name)
            if temp == None:
                success = False
                sleepTime = 0
                while not success:
                    try:
                        if sleepTime>15:
                            print("Forced:", link)
                            success=True
                            session = cloudscraper.create_scraper(browser={
                                'browser': 'firefox',
                                'platform': 'windows',
                                'mobile': False
                            })
                            break

                        manga_page = session.get(link)
                        print(manga_page.status_code)

                        Soup_manga = BeautifulSoup(manga_page.text, 'html.parser')

                        generos = ""
                        for genero in Soup_manga.find_all(class_="media-heading")[1].find_all("a"):
                            generos+="┴"+genero.get_text()
                        
                        sinopse = Soup_manga.find(class_="panel-body").get_text()
                        print(link ,name , generos)

                        image = ActualManga.find(class_="img-thumbnail")['src']

                        Database.addManga(Manga(sinopse,generos,name,link,image))
                        success = True
                    except Exception as e:
                        print("erro:" , e)
                        print("Dromindo por:",sleepTime,"para: ",link)
                        time.sleep(sleepTime)
                        sleepTime += 5
                        success = False
                        pass
        print(it)
    pass

def AnlizeTags() :
    tagsCounter = {}
    for manga in Database.MangaList:
        for tag in manga.getTagsFlags():
            if not tag == '':
                if tagsCounter.get(tag) == None:
                    tagsCounter[tag] = 1
                else:
                    tagsCounter[tag] += 1
    name = []
    size = []
    for key in tagsCounter:
        name.append(key)
        size.append(tagsCounter[key])

    print(tagsCounter)
    # plt.barh(name, size)
    #plt.bar(name, size)
    #plt.pie(size, labels=name)
    #plt.show()
# print(len(Database.mapName))

def LoadMymangas():
    mangas = []
    with open('MangasLidos.csv','r') as mymangas:
        mangas = mymangas.readlines()
        for link in range(len(mangas)):
            mangas[link] = mangas[link].split('\n')[0]
        mymangas.close()
    return mangas

def GetLinktoMangas(links = []):
    mangas=[]
    for link in links:
        mangas.append(Database.findManga(None,url=link))
    return mangas

def analizeMymangas(MyMangas = []):
    tagsCounter = {}
    for manga in MyMangas:
        if manga==None:
            break
        for tag in manga.getTagsFlags():
            if not tag == '':
                if tagsCounter.get(tag) == None:
                    tagsCounter[tag] = 1
                else:
                    tagsCounter[tag] += 1
    name = []
    size = []
    for key in tagsCounter:
        name.append(key)
        size.append(tagsCounter[key])

    return tagsCounter

def calcPonctuations(MyTags = []):
    
    pontuations = []

    for manga in Database.MangaList:
        ponto = 0
        for tag in manga.getTagsFlags():
            if not tag == '':
                if not MyTags.get(tag) == None:
                    ponto += MyTags[tag]
                else:
                    ponto += 0.5
        pontuations.append((manga,ponto))
    return pontuations

getPages()
from flask import Flask,jsonify,render_template,request


app = Flask('flaskapp', static_url_path='/', static_folder='public')

@app.route("/gen",methods=['POST'])
def gen():
    return None
    pass

@app.route("/getList",methods=['GET'])
def getList():
    mangas = []
    for manga in Database.MangaList[1:]:
        flags = []

        for key in manga.getTagsFlags():
            if len(key)>1:
                flags.append(key)
        mangas.append({"name":manga.name,"img":manga.img,"link":manga.link,"flags":flags})
    return jsonify(mangas)

@app.route("/proclink",methods=['POST'])
def ProcLink():
    content = request.get_json()
    mangas = []
    for manga in [syncLink(content['link'])]:
        flags = []
        for key in manga.getTagsFlags():
            if len(key)>1:
                flags.append(key)
        mangas.append({"name":manga.name,"img":manga.img,"link":manga.link,"flags":flags,'description':manga.description})
    return jsonify(mangas)

@app.route("/analize",methods=['POST'])
def Analize():
    content = request.get_json()
    mangas = []
    MyTags=analizeMymangas(GetLinktoMangas(content['links']))
    Ponctuations = calcPonctuations(MyTags)
    Ordened = sorted(Ponctuations,key=lambda manga: manga[1])
    for best in Ordened[len(Ordened)-100:len(Ordened)]:
        mangas.append({"link":best[0].link,"pontuation":best[1]})
    return jsonify({'mangas':mangas,'MyTags':MyTags})

@app.route("/",methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',debug=False,port=port)