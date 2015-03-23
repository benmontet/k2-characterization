#!/usr/bin/env python
from __future__ import print_function, division

from k2fpp.tables import MAGS
from k2fpp.starmodels import get_starmodel, EPIC_StarModel

import logging

import sys

STARMODEL_DIR = 'starmodels_inflated_nogri'

for i,epic_id in enumerate(MAGS.index):
    print('{} of {}: {}'.format(i+1,len(MAGS),epic_id))
    #if epic_id <= 201565013:
    #    continue
    try:
        mod = EPIC_StarModel(epic_id)
        mod.fit_mcmc()
        mod.triangle_plots('{}/{}'.format(STARMODEL_DIR,epic_id))
    except KeyboardInterrupt:
        raise
    except:
        raise
        logging.error('Fit for {} broke.'.format(epic_id))

