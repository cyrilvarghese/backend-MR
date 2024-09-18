import chromadb
from  dotenv import load_dotenv
 
from config import DB_NAME
import os
load_dotenv()

 

async def setup_chroma(is_reset=False):
    try:    
        # persisten_client= chromadb.PersistentClient(path="chroma_db") # type: ignore
        chroma_client = chromadb.HttpClient(host='localhost', port=3001)
        collection = chroma_client.get_or_create_collection(name=DB_NAME)
        print("collection created with docs:",collection.count())




    except Exception as e:
        print("An error occurred:", str(e))
    
 