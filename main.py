from database import connectToDatabase, getPendingLinks, createLinktable
from crawler import validLinks, getResponse, saveFile
import concurrent



if __name__=='__main__':
    
    URL='https://flinkhub.com'
    connectToDatabase()
    response = getResponse(URL)
    createLinktable(URL, '', response, saveFile(URL), '')
    
    while True:
        
        pendingLinks= getPendingLinks()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(validLinks, pendingLinks)
        
        
       

