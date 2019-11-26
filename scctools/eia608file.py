#!/usr/bin/env python3

import os

from .common import *
from .eia608codes import *

class CC608File():
    def __init__(self, path, fps=29.97, channel=False):
        self.captions = []
        self.path = str(path)
        self.fps = fps
        if not os.path.exists(self.path):
            logging.error("Requested file {} does not exist".format(self.path))
            return
        logging.info("Parsing EIA-608 file {}".format(self.path))

        self.rawlines = open(self.path).readlines()

        header = self.rawlines[0].strip()
        if header[18:25] != "CEA-608":
            logging.error("{} is not a valid 608 file".format(self.path))
            return
        if header[-10:-3] != "Channel":
            logging.error("{} is not a valid 608 file".format(self.path))
            return
        try:
            parsed_channel = int(header[-1])
        except ValueError:
            logging.error("{} is not a valid 608 file".format(self.path))
            return

        # override parsed channel
        self.id_channel = channel or parsed_channel

        if self.id_channel not in [1,2,3,4]:
            logging.error("Invalid Channel ID {}".format(self.id_channel))
            return
        else:
            logging.debug("Parsed Channel ID {}".format(self.id_channel))

        for row in self.rawlines[1:]:
            row = row.strip()
            stc, txt = row.split(" - ", 1)
            if stc[8] == ",":
                sh, sm, ss = stc.replace(",", ".").split(":")
                tc = 0
                tc+= int(sh) * 3600
                tc+= int(sm) * 60
                tc+= float(ss)
            elif stc[8] == ":":
                #TODO
                logging.error("Parsing non-drop-frame timecode is not implemeted")
                return

            elif stc[8] == ";":
                #TODO
                logging.error("Parsing non-drop-frame timecode is not implemeted")
                return

            else:
                logging.error("Unsupported timecode format {}".format(stc))
                return

            self.captions.append([tc, txt])


    def __len__(self):
        return len(self.captions)


    def dumpscc(self):
        if not self:
            logging.error("No captions available")

        result = "Scenarist_SCC V1.0\n\n"
        for tc, text in self.captions:

            text = text.replace("\"", "")
            selements = text.split(" ")
            telements = []
            fspace = ""
            for sel in selements:

                if not sel:
                    continue
                if sel[0] == "{" and sel[-1] == "}":
                    key = sel[1:-1]

                    if len(key.split(":")) > 1:
                        okey = key
                        key = ""
                        for n in okey.split(":"):
                            if n[0] in ["R", "C"]:
                                n = n[1:].zfill(2)
                            elif n == "UL":
                                n = "U"
                            else:
                                logging.warning("Parsing {} element of key {} is not supported".format(n, okey))
                            key += n

                    if key in EIA608CODES:
                        telements.append(EIA608CODES[key][self.id_channel-1])
                    elif key in ["AOF", "AON"]:
                        continue
                    else:
                        logging.warning("Unsupported key ", sel)
                        continue
                else:
                    telements.append(
                               str2scc(fspace + sel).strip()
                            )
                    fspace = " "
            text = " ".join(telements)



            result += "{}\t{}\n\n".format(
                    s2tc(tc, self.fps),
                    text
                )
        return result



def cc608toscc(fin, fout):
    c = CC608File(fin)
    fout = str(fout)
    if not c:
        return False
    scc = c.dumpscc()
    with open(fout, "w") as f:
        f.write(scc)
    return True
