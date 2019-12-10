from html.parser import HTMLParser
from .common import *

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_srt_lines(path):
    data = open(str(path), "r", errors="ignore", newline=None)
    buff = ""
    for ch in data.read():
        if ch == "\n":
            yield (buff)
            buff = ""
            continue
        buff += ch


class SRTParser():
    def __init__(self, path):
        self.captions = []
        self.problems = []

        start = stop = 0
        text = []
        for line in get_srt_lines(path):
            if not line.strip():
                if start and stop and text:
                    caption = Caption(
                            strip_tags("\n".join(text)),
                            start=start,
                            stop=stop
                        )
                    self.captions.append(caption)
                start = stop = 0
                text = []
                continue

            if (not text) and line.find("-->") > -1:
                tcs, tce = line.split("-->")
                start = tc2s(tcs.strip())
                stop = tc2s(tce.strip())
                continue

            if start and stop and line.strip():
                line = line.strip()
                text.append(line)
