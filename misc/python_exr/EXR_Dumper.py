# Written by user "Styler" on Tech-Artists

import os
import struct
import binascii


def dump_to_exr_rgb16uncomp(height, width, data, filename):
    """
    :param height: Height of image
    :param width: Width of image
    :param data: A sequence (list/tuple) of float point values in format [r, g, b, r, g, b ...]
    :param filename: filename for output
    """
    def make_chlist_value(name, typ, linear=0, samx=1, samy=1):
        return ''.join([
            name, '\x00',
            struct.pack('I', typ),
            struct.pack('B', linear),
            '\x00\x00\x00',             # reserved
            struct.pack('I', samx),
            struct.pack('I', samy)])

    def make_attr(name, typ, size, value):
        return ''.join([
            name, '\x00',
            typ, '\x00',
            struct.pack('I', size),
            value])

    def pack_half(value):
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
    # NOTE 固定数值 https://www.openexr.com/documentation/openexrfilelayout.pdf 第5页有描述
    fdata = ['\x76\x2f\x31\x01\x02\x00\x00\x00']  # magic and version

    if width*height*depth != len(data):
        raise ValueError('Data length does not fit with image size')

    # build header
    channels = '%s\x00' % ''.join([make_chlist_value(name, typ) for name, typ in (('R', 1), ('G', 1), ('B', 1))])
    fdata.append(make_attr('channels', 'chlist', 18*depth+1, channels))
    fdata.append(make_attr('compression', 'compression', 1, '\x00'))  # 0 - uncompressed

    windata = ''.join(['\x00'*8, struct.pack('i', width-1), struct.pack('i', height-1)])

    fdata.append(make_attr('dataWindow', 'box2i', 16, windata))
    fdata.append(make_attr('displayWindow', 'box2i', 16, windata))
    fdata.append(make_attr('lineOrder', 'lineOrder', 1, '\x00'))     # inc y
    fdata.append(make_attr('pixelAspectRatio', 'float', 4, struct.pack('f', 1.0)))
    fdata.append(make_attr('screenWindowCenter', 'v2f', 8, struct.pack('ff', 0, 0)))
    fdata.append(make_attr('screenWindowWidth', 'float', 4, struct.pack('f', 1)))
    fdata.append('\x00')  # end of the header

    # calc lines offset
    offtab_size = sum([len(x) for x in fdata]) + height*8
    line_size = 8 + width*2*depth

    # fill offsets table
    for i in xrange(height):
        fdata.append(struct.pack('Q', offtab_size + i*line_size))

    data_size = struct.pack('I', width*2*depth)

    # add data by scanlines
    for j in xrange(height):
        line = [struct.pack('i', j), data_size]
        n = j*width*depth

        for i in xrange(depth):
            chdata = [pack_half(data[n+x+i]) for x in xrange(0, width*depth, depth)]
            line.append(struct.pack('%sH' % len(chdata), *chdata))
        fdata.append(''.join(line))

    # write to file
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, 'wb') as f:
        f.write(''.join(fdata))


if __name__ == "__main__":
    width = 400
    height = 400
    pixels = range(width*height*3)
    for w in range(width):
        for h in range(height):
            pos = (w+h*width)*3
            pixels[pos+0] = 0.0
            pixels[pos+1] = 0.0
            pixels[pos+2] = 255.0
    
    DIR = os.path.dirname(__file__)
    file_name = os.path.join(DIR,"test.exr")
    dump_to_exr_rgb16uncomp(width,height,pixels,file_name)