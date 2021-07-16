# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-25 21:12:22'

"""
https://www.openexr.com/documentation/openexrfilelayout.pdf
https://www.openexr.com/documentation/TechnicalIntroduction.pdf
根据 OpenEXR 规范通过 Python struct 输出二进制
"""

# Written by user "Styler" on Tech-Artists

import os
import struct
import binascii

from math import copysign, frexp, isinf, isnan, trunc

NEGATIVE_INFINITY = b'\x00\xfc'
POSITIVE_INFINITY = b'\x00\x7c'
POSITIVE_ZERO = b'\x00\x00'
NEGATIVE_ZERO = b'\x00\x80'
# exp=2**5-1 and significand non-zero
EXAMPLE_NAN = struct.pack('<H', (0b11111 << 10) | 1)

def dump_to_exr_rgb16uncomp(height, width, data, filename):
    """
    :param height: Height of image
    :param width: Width of image
    :param data: A sequence (list/tuple) of float point values in format [r, g, b, r, g, b ...]
    :param filename: filename for output
    """
    def make_chlist_value(name, typ, linear=0, samx=1, samy=1):
        # NOTE 定义好了 chlist 输出格式 https://www.openexr.com/documentation/openexrfilelayout.pdf#page=14 
        return ''.join([
            # NOTE https://www.openexr.com/documentation/TechnicalIntroduction.pdf#page=7 
            # NOTE 包含 名称 和 类型
            name, '\x00',
            struct.pack('I', typ),
            struct.pack('B', linear),
            '\x00\x00\x00',             # reserved
            # NOTE RGBA 图片 为 1
            struct.pack('I', samx),
            struct.pack('I', samy)])

    def make_attr(name, typ, size, value):
        # NOTE Attribute Layout https://www.openexr.com/documentation/openexrfilelayout.pdf#page=8 
        return ''.join([
            name, '\x00',
            typ, '\x00',
            struct.pack('I', size),
            value])

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
        return (sign << 15) | (e16 << 10) | f16
        # return struct.pack('<H', (sign << 15) | (e16 << 10) | f16)
        
    def pack_half(value):
        # NOTE IEEE 754-2008 https://stackoverflow.com/questions/31464022/
        # NOTE 将传入的 浮点数 转换为 half 类型
        # NOTE 参考文章 https://akaedu.github.io/book/ch14s04.html
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

    depth = 3
    # NOTE https://www.openexr.com/documentation/openexrfilelayout.pdf#page=6 第 5 - 6 页有描述
    # NOTE \x76\x2f\x31\x01 固定数据 10 进制为 20000630 | 用来区分 OpenEXR 格式
    # NOTE \x02\x00\x00\x00 这四个数据为 Version Field  | \x02 表示 2.0 版本 
    fdata = ['\x76\x2f\x31\x01\x02\x00\x00\x00']  # magic and version

    if width*height*depth != len(data):
        raise ValueError('Data length does not fit with image size')

    # build header
    # NOTE https://www.openexr.com/documentation/openexrfilelayout.pdf#page=8
    # NOTE 定义属性通道描述
    channels = '%s\x00' % ''.join([make_chlist_value(name, typ) for name, typ in (('R', 1), ('G', 1), ('B', 1))])
    fdata.append(make_attr('channels', 'chlist', 18*depth+1, channels))

    # NOTE https://www.openexr.com/documentation/openexrfilelayout.pdf#page=15
    fdata.append(make_attr('compression', 'compression', 1, '\x00'))  # 0 - uncompressed

    # NOTE https://www.openexr.com/documentation/openexrfilelayout.pdf#page=14
    # NOTE box2i 包含 4 个 int | int 占用 4 个字节 | 前面 '\x00'*8 表示 0 , 0
    windata = ''.join(['\x00'*8, struct.pack('i', width-1), struct.pack('i', height-1)])
    fdata.append(make_attr('dataWindow', 'box2i', 16, windata))
    fdata.append(make_attr('displayWindow', 'box2i', 16, windata))

    # NOTE https://www.openexr.com/documentation/openexrfilelayout.pdf#page=15
    fdata.append(make_attr('lineOrder', 'lineOrder', 1, '\x00'))     # inc y
    # NOTE https://www.openexr.com/documentation/openexrfilelayout.pdf#page=8
    fdata.append(make_attr('pixelAspectRatio', 'float', 4, struct.pack('f', 1.0)))
    fdata.append(make_attr('screenWindowCenter', 'v2f', 8, struct.pack('ff', 0, 0)))
    fdata.append(make_attr('screenWindowWidth', 'float', 4, struct.pack('f', 1)))
    fdata.append('\x00')  # end of the header


    # NOTE https://www.openexr.com/documentation/openexrfilelayout.pdf#page=10
    # NOTE 计算 offset Tables | offset Tables 用来读取像素的映射表
    # NOTE offsetChunk 使用 unsigned long 类型 占 8 个字节 
    # NOTE 添加了 height 个 offsetChunk 数据(所以 + height*8)
    # calc lines offset
    offtab_size = sum([len(x) for x in fdata]) + height*8
    # NOTE 每个单元格像素包含 RGB 三个通道 depth | 2 代表 half 类型的大小(float 为 4 字节, half 为 2 字节)
    # NOTE 前面加 8 是因为 每行开始需要有 起始结束的描述数据 | 两个 int 类型共占 8 个字节 
    # NOTE https://www.openexr.com/documentation/TechnicalIntroduction.pdf#page=13
    line_size = 8 + width*2*depth
    # fill offsets table
    for i in xrange(height):
        fdata.append(struct.pack('Q', offtab_size + i*line_size))

    data_size = struct.pack('I', width*2*depth)

    # NOTE Scan Lines
    # add data by scanlines
    for j in xrange(height):
        # NOTE 起始和结束的行描述数据
        line = [struct.pack('i', j), data_size]
        n = j*width*depth

        for i in xrange(depth):
            # NOTE 读取传入的像素数据 转换为 half 类型
            chdata = [binary16(data[n+x+i]) for x in xrange(0, width*depth, depth)]
            # NOTE 使用 short 类型的长度代指 half 占用的空间
            line.append(struct.pack('%sH' % len(chdata), *chdata))
        fdata.append(''.join(line))

    # write to file
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, 'wb') as f:
        f.write(''.join(fdata))


if __name__ == "__main__":
    
    # NOTE 测试输出 400 * 400 蓝色的 exr 图片
    width = 10
    height = 10
    pixels = range(width*height*3)
    for w in range(width):
        for h in range(height):
            pos = (w+h*width)*3
            # NOTE RGB 的顺序是反过来的
            pixels[pos+2] = 0.0
            pixels[pos+1] = 0.0
            pixels[pos+0] = 255.0
    
    DIR = os.path.dirname(__file__)
    file_name = os.path.join(DIR,"test.exr")
    dump_to_exr_rgb16uncomp(width,height,pixels,file_name)