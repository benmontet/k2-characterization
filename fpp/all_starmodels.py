#!/usr/bin/env python
from __future__ import print_function, division

from k2fpp.tables import MAGS
from k2fpp.starmodels import get_starmodel

import logging

for epic_id in MAGS.index:
    try:
        mod = get_starmodel(epic_id)
    except:
        logging.error('Fit for {} broke.'.format(epic_id))

