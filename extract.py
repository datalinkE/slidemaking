#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crop slides.
ffmpeg -i Meyers-Type-Deduction.mp4 -vsync 0 -vf select="eq(pict_type\,PICT_TYPE_I)" -f image2 foo-%04d.png
"""

import os
from subprocess import Popen, PIPE
from PIL import Image

INPUT_FOLDER = "./Meyers-Type-Deduction"

print os.path.exists(INPUT_FOLDER)

cropped = []

for file in os.listdir(INPUT_FOLDER):
    if "png" in file:
        path = "/".join((INPUT_FOLDER, file))
        img = Image.open(path)
        crop = img.crop( (0 + 190, 0 + 30, img.size[0] - 73, img.size[1] - 65) )
        crop_name = "/".join((INPUT_FOLDER, "crop", file))
        done_name = "/".join((INPUT_FOLDER, "done", file))
        metric = -1.0
        crop.save(crop_name, "PNG")

        if len(cropped) > 0:
            #os.popen("").read()
            cmd = "compare -metric AE -fuzz 20% {0} {1} /dev/null".format(cropped[-1], crop_name)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            text, err = p.communicate()
            metric = float(err.split()[0])
            if metric > 10.0:
                crop.save(done_name, "PNG")
        else:
            crop.save(done_name, "PNG")

        print path, metric
        cropped.append(crop_name)

