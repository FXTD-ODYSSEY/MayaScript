from glom import glom
from pprint import pprint
from glom import Coalesce

target = {
    "system": {
        "planets": [{"name": "earth", "moons": 1}, {"name": "jupiter", "moons": 69}]
    }
}
spec = {
    "planets": (Coalesce("system.planets", "system.dwarf_planets"), ["name"]),
    "moons": (Coalesce("system.planets", "system.dwarf_planets"), ["moons"]),
}
pprint(glom(target, spec))

target = {
    "system": {
        "dwarf_planets": [{"name": "pluto", "moons": 5}, {"name": "ceres", "moons": 0}]
    }
}
pprint(glom(target, spec))



from glom import glom, T, Merge, Iter, Coalesce
target = {
   "pluto": {"moons": 6, "population": None},
   "venus": {"population": {"aliens": 5}},
   "earth": {"moons": 1, "population": {"humans": 7700000000, "aliens": 1}},
}
spec = {
    "moons": (
         T.items(),
         Iter({T[0]: (T[1], Coalesce("moons", default=0))}),
         Merge(),
    )
}
pprint(glom(target, spec))
# {'moons': {'earth': 1, 'pluto': 6, 'venus': 0}}
