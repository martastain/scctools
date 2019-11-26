from nxtools import *
from .eia608codes import EIA608CODES

def eia608code(code, channel=1):
    return EIA608CODES[code][channel-1]

def odd_parity(b):
    result = b
    bit_count = 0
    while b > 0:
        if b and 0x01 == 0x01:
            bit_count += 1
        b = b >> 1
    if bit_count % 2 == 0:
        result  |= 0x80
    return result


def str2eia608(s, channel=1):
    response = []
    length_counter = 0
    for b in s:
        if b != "\n":
            length_counter += 1
    buff = ""
    for b in s:
        if b == "\n":
            if buff:
                response.append(buff + "80")
                buff = ""
            response.append("94f0")
            continue
        buff += "{:x}".format(
                odd_parity(
                    ord(b)
                )
            )
        if len(buff) == 4:
            response.append(buff)
            buff = ""

    if buff:
        response.append(buff + "80")
    return response



def str2scc(s):
    response = ""
    length_counter = 0
    for b in s:
        if b != "\n":
            length_counter += 1
    counter = 0
    for b in s:
        if b == "\n":
            response += "94ad "
            continue
        response += "{:x}".format(
                odd_parity(
                    ord(b)
                )
            )
        counter += 1
        if counter % 2 == 0:
            response += " "

    if length_counter % 2 == 1:
        response += "80 "
    return response




