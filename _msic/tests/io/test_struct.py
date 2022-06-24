import io
import os
import struct

s = struct.pack('i', 5) # b'\x05\x00\x00\x00'
print("s",s)
value, = struct.unpack('i', s)
print(value)
# byte_int=int(int_value).to_bytes(length=length,byteorder=byteorder,signed=signed)
# int_val = int.from_bytes(CurrentByte, "big")
