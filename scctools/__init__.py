__all__ = ["cc608toscc", "sccconsolide", "SRTParser"]

from .common import *
from .eia608file import cc608toscc
from .sccconsolide import sccconsolide
from .srtparser import SRTParser


class SCCEncoder():
    def __init__(self, fps=29.97):
        self.captions = []

    def append(self, caption):
        self.captions.append(caption)

    def render(self):
        result = "Scenarist_SCC V1.0\n"
        for caption in self.captions:
            result += "{}\n\n".format(caption.render())
        result = reult.strip()
        return result
