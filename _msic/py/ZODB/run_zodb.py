import ZODB, ZODB.FileStorage
import account, BTrees.OOBTree

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

root.accounts = BTrees.OOBTree.BTree()
root.accounts['account-1'] = account.Account()

