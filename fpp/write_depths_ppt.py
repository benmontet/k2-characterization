#! /usr/bin/env python
from __future__ import print_function, division

import re
import numpy as np

tablefile = 'paper1_tab-cand.tex'

last = 'foo'
for line in open(tablefile):
    line = line.split('&')
    try:
        epic_id = int(line[0])
        if epic_id == last:
            i=2
        else:
            i=1
        last = epic_id
        name = '{}.{:02.0f}'.format(epic_id,i)
        rprs_entry = line[5]
        m = re.search('(\d+\.\d+)_',rprs_entry)
        rprs = float(m.group(1))
        print(name,rprs**2 * 1000)
    except:
        pass
