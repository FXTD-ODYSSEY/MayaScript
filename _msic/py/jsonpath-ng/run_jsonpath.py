from addict import Addict
import attr
from jsonpath_ng.ext import parser


@attr.s
class Person(Addict):
    name = attr.ib()
    age = attr.ib()


person_data = [("Tony", "35"), ("Lisa", "32"), ("Michael", "37"), ("Gabe", "30")]
data = [Person(name=name, age=age) for name, age in person_data]

# jsonpath_expr = parse("$.name")

# data = { "store": {
#     "book": [
#       { "category": "reference",
#         "author": "Nigel Rees",
#         "title": "Sayings of the Century",
#         "price": 8.95
#       },
#       { "category": "fiction",
#         "author": "Evelyn Waugh",
#         "title": "Sword of Honour",
#         "price": 12.99
#       },
#       { "category": "fiction",
#         "author": "Herman Melville",
#         "title": "Moby Dick",
#         "isbn": "0-553-21311-3",
#         "price": 8.99
#       },
#       { "category": "fiction",
#         "author": "J. R. R. Tolkien",
#         "title": "The Lord of the Rings",
#         "isbn": "0-395-19395-8",
#         "price": 22.99
#       }
#     ],
#     "bicycle": {
#       "color": "red",
#       "price": 19.95
#     }
#   }
# }

# data = {'objects': ['alpha', 'gamma', 'beta']}
jsonpath_expr = parser.parse("$[?(@.age<33)]")
for match in jsonpath_expr.find([d for d in data]):
    print(match.value)
