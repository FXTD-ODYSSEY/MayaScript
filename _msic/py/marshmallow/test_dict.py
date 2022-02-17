
from marshmallow import Schema, fields

class PackageSchema(Schema):
    scripts = fields.Dict(keys=fields.Str(), values=fields.Str())

schema = PackageSchema()

data = {
    "scripts":{
        2121:True
    }
}

# TODO wierd 
res,err = schema.dumps(data)
print(res,err)
res,err = schema.loads(res)
print(res,err)
