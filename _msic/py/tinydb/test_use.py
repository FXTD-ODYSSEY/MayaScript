# Import built-in modules
import json
import os

from typing import Iterable
from typing import List
from typing import Mapping


# Import third-party modules
from addict import Addict
import attr
from tinydb import Query
from tinydb import TinyDB
from tinydb.database import Document
from tinydb.storages import MemoryStorage
from tinydb.storages import Storage

class MyDb(TinyDB):

    def insert(self, document):
        """
        Insert a new document into the table.

        :param document: the document to insert
        :returns: the inserted document's ID
        """
        
        # Make sure the document implements the ``Mapping`` interface
        if not isinstance(document, Mapping):
            raise ValueError('Document is not a Mapping')

        # First, we get the document ID for the new document
        if isinstance(document, Document):
            # For a `Document` object we use the specified ID
            doc_id = document.doc_id

            # We also reset the stored next ID so the next insert won't
            # re-use document IDs by accident when storing an old value
            self._next_id = None
        else:
            # In all other cases we use the next free ID
            doc_id = self._get_next_id()

        # Now, we update the table and add the document
        def updater(table: dict):
            assert doc_id not in table, 'doc_id '+str(doc_id)+' already exists'

            # By calling ``dict(document)`` we convert the data we got to a
            # ``dict`` instance even if it was a different class that
            # implemented the ``Mapping`` interface
            table[doc_id] = document

        # See below for details on ``Table._update``
        self._update_table(updater)

        return doc_id

    def insert_multiple(self, documents: Iterable[Mapping]) -> List[int]:
        """
        Insert multiple documents into the table.

        :param documents: a Iterable of documents to insert
        :returns: a list containing the inserted documents' IDs
        """
        doc_ids = []

        def updater(table: dict):
            for document in documents:
                # Make sure the document implements the ``Mapping`` interface
                if not isinstance(document, Mapping):
                    raise ValueError('Document is not a Mapping')

                # Get the document ID for this document and store it so we
                # can return all document IDs later
                doc_id = self._get_next_id()
                doc_ids.append(doc_id)

                # Convert the document to a ``dict`` (see Table.insert) and
                # store it
                table[doc_id] = document

        # See below for details on ``Table._update``
        self._update_table(updater)

        return doc_ids


DIR = os.path.dirname(__file__)

db = MyDb(storage=MemoryStorage)
# db = TinyDB(os.path.join(DIR,"test.json"))
@attr.s
class MyData(Addict):
    name = attr.ib(default="")
    age = attr.ib(default=-1)

data = MyData()
data.name = "John"
data.age = 22
print(data)
db.insert(data)


User = Query()
res = db.search(User.name == 'John')
print(res)
print(res[0] is data)

print(db.storage.read())
print(db._read_table())



