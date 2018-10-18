import os
import time
import pickle
import shutil
import random
import argparse
from urllib.request import urlopen
import socks
import socket
from utils import Config
import pdb


parser = argparse.ArgumentParser()
parser.add_argument('--use-proxy', action="store_true", default=False, help='if use socks proxy')
parser.add_argument('--timeout', type=int, default=30, help='socket timeout ')
            
args = parser.parse_args()

if args.use_proxy:
    # set sock5 proxy
    socks.set_default_proxy(socks.SOCKS5, "localhost", 2080)
    socket.socket = socks.socksocket


timeout_secs = args.timeout  # after this many seconds we give up on a paper
if not os.path.exists(Config.pdf_dir):
    os.makedirs(Config.pdf_dir)
have = set(os.listdir(Config.pdf_dir))  # get list of all pdfs we already have

numok = 0
numtot = 0
db = pickle.load(open(Config.db_path, 'rb'))
for pid, j in db.items():
    pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
    pdb.set_trace()
    assert len(pdfs) == 1
    pdf_url = pdfs[0] + '.pdf'
    basename = pdf_url.split('/')[-1]
    fname = os.path.join(Config.pdf_dir, basename)

    # try retrieve the pdf
    numtot += 1
    try:
        if not basename in have:
            print('fetching %s into %s' % (pdf_url, fname))
            req = urlopen(pdf_url, None, timeout_secs)
            with open(fname, 'wb') as fp:
                shutil.copyfileobj(req, fp)
            time.sleep(0.05 + random.uniform(0, 0.1))
        else:
            print('%s exists, skipping' % (fname, ))
        numok += 1
    except Exception as e:
        print('error downloading: ', pdf_url)
        print(e)

    print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db)))

print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))
