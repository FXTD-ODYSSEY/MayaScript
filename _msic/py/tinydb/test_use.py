from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
import os
from addict import Dict

DIR = os.path.dirname(__file__)

db = TinyDB(storage=MemoryStorage)
# db = TinyDB(os.path.join(DIR,"test.json"))
User = Query()

data = Dict()
data.name = "John"
data.age = 22

db.insert(data)
res = db.search(User.name == 'John')
print(res)
print(res[0] is data)



