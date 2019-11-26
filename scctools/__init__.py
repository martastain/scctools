__all__ = ["cc608toscc", "sccconsolide"]

from .common import *
from .eia608file import cc608toscc
from .sccconsolide import sccconsolide



class Caption():
    def __init__(self, start, end, text, channel=1):
        self.start = start
        self.end = end
        self.text = text
        self.channel = channel

    @property
    def lines(self):
        return [line.strip() for line in self.text.split("\n")]


    @property
    def commands608(self):
        result = [
                eia608code("EDM"),
                eia608code("EDM"),
                eia608code("ENM"),
                eia608code("ENM"),
                eia608code("RCL"),
                eia608code("RCL"),
                eia608code("RU4"),
                eia608code("RU4"),
            ]
        lines = []
        for i, line in enumerate(self.lines):
            line = line.strip()
            result.extend(str2eia608(line, self.channel))
            if i < len(self.lines) -1:
                result.append(eia608code("CR", self.channel))

        result.append(eia608code("EOC", self.channel))
        result.append(eia608code("EOC", self.channel))
        return result




    def render(self):
        result = "{}\t".format(caption.start_tc)
        text = ""
        #            ENM  ENM  RCL  RCL  RU3  RU3
        result += "94ae 94ae 9420 9420 9426 9426 "
        for line in caption.lines:
            #TODO: pad-trim to 32 bytes
            text += line

        text = text.rstrip("\n")
        result += write_string(text)
        result += "\n"

        result += "{}\t942c 942c\n\n".format(caption.end_tc)

        return result



class SCCEncoder():
    def __init__(self, fps=29.97):
        self.captions = []

    def add(self, start, stop, text):
        pass

    def render(self):
        result = "Scenarist_SCC V1.0\n"
        for caption in self.captions:
            result += "{}\n\n".format(caption.render())
        result = reult.strip()
        return result


