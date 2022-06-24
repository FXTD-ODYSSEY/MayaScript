import io
import os
import codecs

DIR = os.path.dirname(os.path.abspath(__file__))
# dna_file = io.BytesIO(os.path.join(DIR, 'test.dna').encode("ASCII"))
# dna_file = codecs.open(os.path.join(DIR, 'test.dna'),'w') 
# print(dna_file.buffer)
file = io.BytesIO()
string_value = "hello"
byte_string = string_value.encode("ASCII")
file.write(byte_string)
file.write(b'change')
data = file.getvalue()
print("data",data)
data = (1).to_bytes()
print(data)
