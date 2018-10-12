#import pandas as pd
import pdfplumber
import sys, os

import logging
logging.disable(logging.ERROR)

HERE = os.path.abspath(os.path.dirname("./"))

path = os.path.join(
            HERE,
            "tests/pdfs/rnod.pdf"
        )
page = pdfplumber.open(path).pages[0]
# im = page.to_image()
# im.draw_lines(page.curves)
# im.draw_rects(page.extract_words())

x = page.extract_words()


print('-'*100)
print(page._objects.keys())
# for obj in x:
#     #if not isinstance(obj, LTChar):
#     print(obj)

