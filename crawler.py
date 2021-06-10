import requests
from bs4 import BeautifulSoup
import time, uuid
from datetime import datetime, timedelta
from database import connectToDatabase



def time24hrsback():             #gives the timestamp before 24 hrs             
    before24Hours = datetime.today() - timedelta(days=1)                 
    return before24Hours

def alreadycrawled(link):        #to check if the link is already cralwed between last 24 hrs
    db = connectToDatabase()
    condition = { '$and' : [{"link":link},{"time": {"$gte": time24hrsback()}}] }
    if (db.Links.count_documents(condition) > 0) :                                               
        db.Links.update_many({"link":link}, {"$set" : { 'isCrawled': True,
                'lastCrawlDt': datetime.today().replace(microsecond=0)}})
               
        return True
    else :
        return False


def getResponse(link):
    response = requests.get(link)
    return(response)

def saveFile(link):
    response = getResponse(link)
    random_file = str(uuid.uuid4())           #gives random name to the file
    with open ("html/{}.html".format(random_file), 'w') as file:
       file.write(response.content)
    filePath= ("html/{}.html".format(random_file))                                         
    return filePath
    
    
def validLinks(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html5lib')
    atags = soup.find_all("a", href=True)             #to find all anchor tags with 'href' attribute
    
    Links =[]
    no_of_links = 0
    
    for i in atags:
        href = i['href']
        
        if(i.get('href') == '#' ):
            #invalid Link
            continue
        
        if(i.get('href') =='javascript:'):
           #invalid Link
           continue
       
        if(i.get('href') ==''):
           #Invalid Link
           continue
       
        if(i.get('href') =='#xyz'):
           #Invalid Link
           continue
       
        if(i.get('href') =='http://'):
           #valid Link
           #absolute Link 
           Links.append(href)
           no_of_links += 1
           continue
           
        if(i.get('href') =='//'):
           #valid link
           #append
           Links.append('https:' + href)
           no_of_links += 1
           continue
           
        

    if(no_of_links == 0):
        print('All links crawled')
           
time.sleep(10)    


