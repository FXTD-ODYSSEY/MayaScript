import sys
import yaml
from ruamel.yaml import YAML,RoundTripDumper,RoundTripLoader

from ruamel.yaml import dump

yaml = YAML()

yaml_str = """\
# example
name:
  # details
  family: Smith   # very common
  given: Alice    # one of the siblings
"""

code = yaml.load(yaml_str)
code['name']['given'] = 'Bob'
code['name']['asd'] = '123'
code['y'] =123
code['x'] =12
yaml.dump(code, sys.stdout)
print(code)
res = dump(code)
print(res)
