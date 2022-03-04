from eventsourcing.domain import Aggregate, event
from eventsourcing.application import Application
import os

# Enable aggregate caching.
os.environ['AGGREGATE_CACHE_MAXSIZE'] = '1000'

# Use SQLite.
os.environ['PERSISTENCE_MODULE'] = 'eventsourcing.sqlite'
os.environ['SQLITE_DBNAME'] = ':memory:'

class Dog(Aggregate):
    @event('Registered')
    def __init__(self, name):
        self.name = name
        self.tricks = []

    @event('TrickAdded')
    def add_trick(self, trick):
        self.tricks.append(trick)


class DogSchool(Application):
    def register_dog(self, name):
        dog = Dog(name)
        self.save(dog)
        return dog.id

    def add_trick(self, dog_id, trick):
        dog = self.repository.get(dog_id)
        dog.add_trick(trick)
        self.save(dog)

    def get_dog(self, dog_id):
        dog = self.repository.get(dog_id)
        return {'name': dog.name, 'tricks': tuple(dog.tricks)}
        


application = DogSchool()

dog_id = application.register_dog('Fido')
application.add_trick(dog_id, 'roll over')
application.add_trick(dog_id, 'fetch ball')
application.add_trick(dog_id, 'fetch asd')
dog_details = application.get_dog(dog_id)
# assert dog_details['name'] == 'Fido'
# assert dog_details['tricks'] == ('roll over', 'fetch ball')
notifications = application.notification_log.select(start=1, limit=10)
for notification in notifications:
    print(notification)
# assert len(notifications) == 3
# assert notifications[0].id == 1
# assert notifications[1].id == 2
# assert notifications[2].id == 3
