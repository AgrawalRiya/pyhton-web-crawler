from pymongo import MongoClient
from datetime import datetime 
from time import sleep



#connecting to Mongodb
#connecting to database 'crawler'  
def connectToDatabase():
    client = MongoClient('localhost', 27017)
    db = client.get_database('crawler')
    
    return db
    

def createLinktable(link, sourceLink, response, filePath, lastCrawlDt) :
    db = connectToDatabase()
    linkData = {
            'link': link,
            'sourceLink': sourceLink,
            'isCrawled': False,
            'lastCrawlDt': lastCrawlDt,
            'responseStatus': response.status_code if response else '',
            'contentType': response.headers['Content-Type'] if "Content-Type" in response.headers else '',
            'contentLength': response.headers['Content-Length']  if "Content-Length" in response.headers else '',
            'filePath': filePath,
            'createdAt': datetime.now()          
    }
    db.Links.insert_one(linkData)

    if db.Links.count_documents({}) >= 5000:             #count_documents gives the count of documents present under the collection
        print("Maximum limit reached")
        sleep(2000)
    

def getPendingLinks() :                          #to find the links which are yet to be crawled
    db = connectToDatabase()
    pendingLinks = []
    for links in db.Links.find({'isCrawled': False}):
        pendingLinks.append(links['link'])
    return pendingLinks