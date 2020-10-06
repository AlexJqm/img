import pymongo

def db_connect():
    db_client = pymongo.MongoClient("mongodb+srv://discordjs:aqwzsx08@among-us-france.jh76m.mongodb.net/among-us-france?retryWrites=true&w=majority")
    db = db_client['among-us-france']
    return db["servers"]