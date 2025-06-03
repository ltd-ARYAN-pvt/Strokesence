from db.mongodb import mongodb

def get_collection(name: str):
    return mongodb.db.get_collection(name)
