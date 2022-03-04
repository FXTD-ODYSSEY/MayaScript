from textwrap import dedent

def indent(text, prefix, predicate=None):
    """Adds 'prefix' to the beginning of selected lines in 'text'.

    If 'predicate' is provided, 'prefix' will only be added to the lines
    where 'predicate(line)' is True. If 'predicate' is not provided,
    it will default to adding 'prefix' to all non-empty lines that do not
    consist solely of whitespace characters.
    """
    if predicate is None:
        def predicate(line):
            return line.strip()

    def prefixed_lines():
        for line in text.splitlines(True):
            res = (prefix + line if predicate(line) else line)
            print(res)
            yield res
    return ''.join(prefixed_lines())  
path = r"F:\repo\QBinder\QBinder\__init__.py"

with open(path, 'r') as f:
    content = f.read()
def main(content):
        
    code = dedent("""
    def main():
    {0}

    """).format(indent(content," "*4))
    return code

res = main(content)
print(res)


class Test(object):
    pass

bases = Test.__bases__
Test.__bases__ += (None,)

