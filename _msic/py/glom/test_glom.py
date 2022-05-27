from glom import glom
from pprint import pprint
from glom import SKIP

target = {"galaxy": {"system": {"planet": "jupiter"}}}
spec = "galaxy.system.planet"
res = glom(target, spec)
print(res)


target = {"system": {"planets": [{"name": "earth"}, {"name": "jupiter"}]}}
res = glom(target, ("system.planets", ["name"]))
print(res)
# ['earth', 'jupiter']


target = {
    "system": {
        "planets": [{"name": "earth", "moons": 1}, {"name": "jupiter", "moons": 69}]
    }
}
spec = {"names": ("system.planets", ["name"]), "moons": ("system.planets", ["moons"])}
pprint(glom(target, spec))


target = {
    "system": {
        "planets": [
            {"name": "earth", "moons": [{"name": "luna"}]},
            {"name": "jupiter", "moons": [{"name": "io"}, {"name": "europa"}]},
        ]
    }
}
spec = {
    "planet_names": ("system.planets", ["name"]),
    "moon_names": ("system.planets", [("moons", ["name"])]),
}
pprint(glom(target, spec))


res = glom([1, 2, 3, 4, 5, 6], [lambda i: i if i % 2 else SKIP])
print(res)