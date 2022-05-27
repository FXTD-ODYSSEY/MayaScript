from ZODB import DB
from ZODB.FileStorage import FileStorage

from ZODB.PersistentMapping import PersistentMapping
from persistent import Persistent
import transaction


class Employee(Persistent):
    """An employee"""

    def __init__(self, name, manager=None):
        self.name = name
        self.manager = manager


# setup the database
storage = FileStorage("employees.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

# get the employees mapping, creating an empty mapping if
# necessary
if "employees" not in root:
    root["employees"] = {}
employees = root["employees"]


def listEmployees():
    if len(employees.values()) == 0:
        print("There are no employees.")
        return
    for employee in employees.values():
        print(employee)
        print("Name: %s" % employee.name)
        if employee.manager is not None:
            print("Manager's name: %s" % employee.manager.name)


def addEmployee(name, manager_name=None):
    if name in employees:
        print("There is already an employee with this name.")
        return
    if manager_name:
        try:
            manager = employees[manager_name]
        except KeyError:
            print("No such manager")
            return
        employees[name] = Employee(name, manager)
    else:
        employees[name] = Employee(name)

    root["employees"] = employees  # reassign to change
    transaction.commit()
    print("Employee %s added." % name)


if __name__ == "__main__":
    while 1:
        choice = input(
            "Press 'L' to list employees, 'A' to add" "an employee, or 'Q' to quit:"
        )
        choice = choice.lower()
        if choice == "l":
            listEmployees()
        elif choice == "a":
            name = input("Employee name:")
            manager_name = input("Manager name:")
            addEmployee(name, manager_name)
        elif choice == "q":
            break

    # close database
    connection.close()
