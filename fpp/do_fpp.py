#!/usr/bin/env python
from __future__ import print_function, division

import sys

from k2fpp.fpp import K2_FPPCalculation
from k2fpp.contrast import all_ccs

import logging

import warnings
warnings.simplefilter("error")
warnings.simplefilter("ignore", DeprecationWarning)

epic_id = int(sys.argv[1])
index = int(sys.argv[2])
recalc = sys.argv[-1] == '--recalc'

print('calculating FPP for {}, planet {}...'.format(epic_id, index))
fpp = K2_FPPCalculation(epic_id, i=index, recalc=recalc)
fpp.set_maxrad(8)
ccs = all_ccs(epic_id)
for cc in ccs:
    fpp.apply_cc(cc)
fpp.FPPplots()

