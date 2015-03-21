#!/usr/bin/env python
from __future__ import print_function, division

import pandas as pd
import numpy as np

from k2fpp.tables import PAPER1_TABLE

import logging

import warnings
warnings.simplefilter("error")
warnings.simplefilter("ignore", DeprecationWarning)


ids = []
inds = []
for epic_id in PAPER1_TABLE.index:
    name = PAPER1_TABLE.ix[epic_id,'epic_id']
    if type(name)==pd.Series:
        for i in range(1,len(name)+1):
            ids.append(epic_id)
            inds.append(i)
    else:
        ids.append(epic_id)
        inds.append(1)

for epic_id, i in zip(ids, inds):
    print('./do_fpp.py {} {}'.format(epic_id,i))


