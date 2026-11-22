"""Download the MH370-CAPTION map data files (not redistributed here; no licence stated by the authors).

Source: https://www.mh370-caption.net/index.php/armada-tracking/
"""
import urllib.request
from common import CAPTION

BASE = 'https://raw.githubusercontent.com/trise5631/trise5631.github.io/main/'
FILES = ['areas3.js', 'sc1.js', 'sc2.js', 'sc3.js', 'sc4.js', 'phase1.js', 'phase2.js', 'phase3.js']

if __name__ == '__main__':
    CAPTION.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        urllib.request.urlretrieve(BASE + f, CAPTION / f)
        print('downloaded', f)
