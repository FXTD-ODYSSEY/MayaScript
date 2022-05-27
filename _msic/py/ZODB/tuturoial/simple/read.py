from ZODB import FileStorage, DB
import os
DIR = os.path.dirname(os.path.abspath(__file__))
storage = FileStorage.FileStorage(os.path.join(DIR,'mydatabase.fs'))
db = DB(storage)
connection = db.open()
root = connection.root()
items = root.items()
print(items)
