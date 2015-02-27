from __future__ import print_function, division

import numpy as np
import pandas as pd
import os, os.path, shutil

import logging

from vespa.transitsignal import TransitSignal_FromSamples

from .tables import PAPER1_TABLE

URLBASE = 'http://bbq.dfm.io/~dfm/research/ketu/trap/'
SAMPLEDIR = 'samples'
if not os.path.exists(SAMPLEDIR):
    os.makedirs(SAMPLEDIR)

def get_samples(epic_id):
    url = URLBASE + '{:.0f}.h5'.format(epic_id)
    filename = os.path.join(SAMPLEDIR, '{:.0f}.h5'.format(epic_id))

    try:
        samples = pd.read_hdf(filename, 'samples')
    except:
        logging.error(filename)
        raise
        raise RuntimeError('You need to download file.')

    return samples

class TransitSignal(TransitSignal_FromSamples):
    def __init__(self, epic_id):
        samples = get_samples(epic_id)
        
