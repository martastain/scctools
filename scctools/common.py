import re
import textwrap
import unidecode

from nxtools import *

from .eia608codes import EIA608CODES
from .eia608chars import EIA608CHARS



def caption_reformat(text, width=32):
    lines = []
    buff = ""
    for line in text.split("\n"):
        line = line.strip()
        line = unidecode.unidecode(line)
        if line.startswith("-"):
            lines.append(buff)
            buff = ""
        buff += " " + line
    if buff:
        lines.append(buff)
    output = []
    for line in lines:
        line = line.strip()
        line = textwrap.wrap(line.strip(), width)
        if not line:
            continue
        output.extend([l for l in line if l])
    return output


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
        ch = "{:x}".format(
                odd_parity(
                    ord(b)
                )
            )
        buff += ch
        if len(buff) == 4:
            response.append(buff)
            buff = ""

    if buff:
        response.append(buff + "80")
    return response


def validate_string(string):
    string = string.replace("’", "'")
    return re.sub("[^{}]".format(
                re.escape(EIA608CHARS)
            ), "", string)


def str2scc(s):
    logging.warning("Call to deprecated function str2scc")
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




class Caption():
    def __init__(self, text, **kwargs):
        self.text = text
        self.start = kwargs.get("start", 0)
        self.stop = kwargs.get("stop", 0)
        self.channel = kwargs.get("channel", 1)

    @property
    def lines(self):
        return [line.strip() for line in self.text.split("\n")]

    def eia608cmds(self, mode="rollup"):
        result = [
                eia608code("EDM"),
                eia608code("EDM"),
                eia608code("ENM"),
                eia608code("ENM"),
                eia608code("RCL"),
                eia608code("RCL"),
            ]

        lines = [validate_string(f) for f in caption_reformat(self.text)]

        num_lines = len(lines)
        if num_lines == 1:
            result.extend([eia608code("RU2")]*2)
        elif num_lines == 2:
            result.extend([eia608code("RU2")]*2)
        elif num_lines == 3:
            result.extend([eia608code("RU3")]*2)
        else:
            result.extend([eia608code("RU4")]*2)

        for i, line in enumerate(lines):
            line = line.strip()
            result.extend(str2eia608(line, self.channel))
            if i < len(lines) -1:
                result.append(eia608code("CR", self.channel))

        result.append(eia608code("EOC", self.channel))
        result.append(eia608code("EOC", self.channel))
        return result
