import math

def sccconsolide(input_path, output_path, fps=29.97):
    header = ""
    captions = []
    last_frame = 0
    buff_tc = False
    buff = []
    qframes = 2

    with open(str(input_path)) as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if not header:
                header = line
                continue

            tc, data = line.split("\t")
            tc = tc.replace(";", ":")
            hh, mm, ss, ff = [int(e) for e in tc.split(":")]
            frame = math.floor( (hh*3600*fps) + (mm*60*fps) + (ss*fps) + ff)

            if not buff_tc:
                buff_tc = tc

            if frame - last_frame < qframes:
                buff.extend([e.strip() for e in data.split(" ") if e])

            else:
                captions.append("{}\t{}".format(
                        buff_tc,
                        " ".join(buff)
                    ))

                buff = [e.strip() for e in data.split(" ") if e]
                buff_tc = tc

            last_frame = frame

        if buff:
            captions.append("{}\t{}".format(
                    buff_tc,
                    " ".join(buff)
                ))

    with open(str(output_path), "w") as f:
        f.write(header)
        f.write("\n\n")
        f.write("\n\n".join(captions))
