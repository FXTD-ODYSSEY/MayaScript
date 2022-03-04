import inspect
class SchemaEntity(object):

    def dumps(self, *args, **kwargs):
        data, err = self.schema.dumps(self, *args, **kwargs)
        assert not err, err
        return data

    def loads(self, data, *args, **kwargs):
        data, err = self.schema.loads(data, *args, **kwargs)
        assert not err, err
        return data

    def dump(self, *args, **kwargs):
        data, err = self.schema.dump(self, *args, **kwargs)
        assert not err, err
        return data

    def load(self, data, *args, **kwargs):
        data, err = self.schema.load(data, *args, **kwargs)
        assert not err, err
        return data

    def write(self, path, *args, **kwargs):
        data = self.dumps(*args, **kwargs)
        with open(path, "w") as f:
            f.write(data)

    def read(self, path, *args, **kwargs):
        with open(path, "r") as f:
            data = f.read()
        return self.loads(data, *args, **kwargs)
    # __slots__ = ["dumps", "loads", "dump", "load", "write", "read"]
    __slots__ = ["a"]

print(inspect.getmembers(SchemaEntity,inspect.ismethod))