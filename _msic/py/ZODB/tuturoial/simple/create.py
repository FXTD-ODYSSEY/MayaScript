from ZODB import FileStorage, DB
import transaction
import os

DIR = os.path.dirname(os.path.abspath(__file__))


storage = FileStorage.FileStorage(os.path.join(DIR,'mydatabase.fs'))
db = DB(storage)
connection = db.open()
root = connection.root()

root['employees'] = ['Mary', 'Jo', 'Bob']

transaction.commit()
connection.close()


