# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-26 12:31:13'

"""

"""

import struct
import binascii

# value = 10.0

# a = struct.pack('>f', value)
# b = binascii.hexlify(a)

# f32 = int(b, 16)
# f16 = f32 >> 16
# sign = (f32 >> 16) & 0x8000

# print("a",type(a),a)
# print("b",type(b),b)
# print("f32",type(f32),f32)
# print("f16",type(f16),f16)
# print("sign",type(sign),sign)

from math import copysign, frexp, isinf, isnan, trunc

NEGATIVE_INFINITY = b'\x00\xfc'
POSITIVE_INFINITY = b'\x00\x7c'
POSITIVE_ZERO = b'\x00\x00'
NEGATIVE_ZERO = b'\x00\x80'
# exp=2**5-1 and significand non-zero
EXAMPLE_NAN = struct.pack('<H', (0b11111 << 10) | 1)


def binary16(f):
    # NOTE https://gist.github.com/zed/59a413ae2ed4141d2037
    """Convert Python float to IEEE 754-2008 (binary16) format.
    https://en.wikipedia.org/wiki/Half-precision_floating-point_format
    """
    if isnan(f):
        return EXAMPLE_NAN

    sign = copysign(1, f) < 0
    if isinf(f):
        return NEGATIVE_INFINITY if sign else POSITIVE_INFINITY

    #           1bit        10bits             5bits
    # f = (-1)**sign * (1 + f16 / 2**10) * 2**(e16 - 15)
    # f = (m * 2)                        * 2**(e - 1)
    m, e = frexp(f)
    assert not (isnan(m) or isinf(m))
    if e == 0 and m == 0:  # zero
        return NEGATIVE_ZERO if sign else POSITIVE_ZERO

    f16 = trunc((2 * abs(m) - 1) * 2**10)  # XXX round toward zero
    assert 0 <= f16 < 2**10
    e16 = e + 14
    if e16 <= 0:  # subnormal
        # f = (-1)**sign * fraction / 2**10 * 2**(-14)
        f16 = int(2**14 * 2**10 * abs(f) + .5)  # XXX round
        e16 = 0
    elif e16 >= 0b11111:  # infinite
        return NEGATIVE_INFINITY if sign else POSITIVE_INFINITY
    else:
        # normalized value
        assert 0b00001 <= e16 < 0b11111, (f, sign, e16, f16)
    """
    http://blogs.perl.org/users/rurban/2012/09/reading-binary-floating-point-numbers-numbers-part2.html
    sign    1 bit  15
    exp     5 bits 14-10     bias 15
    frac   10 bits 9-0
    (-1)**sign * (1 + fraction / 2**10) * 2**(exp - 15)
    +-+-----[1]+----------[0]+ # little endian
    |S| exp    |    fraction |
    +-+--------+-------------+
    |1|<---5-->|<---10bits-->|
    <--------16 bits--------->
    """
    return  (sign << 15) | (e16 << 10) | f16
    
def pack_half(value):
    # NOTE 将传入的 浮点数 转换为 half 类型
    # NOTE IEEE 754-2008 https://stackoverflow.com/questions/31464022/
    # NOTE 参考文章 https://blog.csdn.net/qq_30638831/article/details/80421019
    F16_EXPONENT_BITS = 0x1F
    F16_EXPONENT_SHIFT = 10
    F16_EXPONENT_BIAS = 15
    F16_MANTISSA_BITS = 0x3ff
    F16_MANTISSA_SHIFT = (23 - F16_EXPONENT_SHIFT)
    F16_MAX_EXPONENT = (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

    a = struct.pack('>f', value)
    b = binascii.hexlify(a)

    f32 = int(b, 16)
    f16 = 0
    sign = (f32 >> 16) & 0x8000
    exponent = ((f32 >> 23) & 0xff) - 127 
    mantissa = f32 & 0x007fffff

    if exponent == 128:
        f16 = sign | F16_MAX_EXPONENT
        if mantissa:
            f16 |= (mantissa & F16_MANTISSA_BITS)
    elif exponent > 15:
        f16 = sign | F16_MAX_EXPONENT
    elif exponent > -15:
        exponent += F16_EXPONENT_BIAS
        mantissa >>= F16_MANTISSA_SHIFT
        f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
    else:
        f16 = sign

    return f16

if __name__ == "__main__":
    f = 1
    print([pack_half(f)])
    print([binary16(f)])
    print(pack_half(f) == binary16(f))

