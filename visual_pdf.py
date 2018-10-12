#import pandas as pd
import pdfplumber
from pdfplumber import utils
import sys, os

import logging
logging.disable(logging.ERROR)

HERE = os.path.abspath(os.path.dirname("./"))

path = os.path.join(
            HERE,
            "test/rnod.pdf"
        )
page = pdfplumber.open(path).pages[5]
im = page.to_image(resolution=200)
rects = []
with open('test/cer.txt', 'r') as f:
    k = f.readlines()
    for line in k:
        x, y, w , h = line.split(',')
        print(x, y , w, h)
        rects.append((utils.decimalize(float(x)), 
                    utils.decimalize(float(y)), 
                    utils.decimalize(float(x)+float(w)), 
                    utils.decimalize(float(y)+float(h))))

#im.draw_rects(page.extract_textboxes())
im.draw_rects(rects)
im.save("test/test.png")
#print('-'*100)
#print(page._objects.keys())
# for obj in x:
#     #if not isinstance(obj, LTChar):
#     print(obj)

