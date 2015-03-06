from __future__ import print_function, division

import numpy as np
import pandas as pd
import h5py
import os, os.path, shutil

import logging

from vespa.transitsignal import TransitSignal_FromSamples

from .tables import PAPER1_TABLE

URLBASE = 'http://bbq.dfm.io/~dfm/research/ketu/trap/'
SAMPLEDIR = 'trap_samples'
if not os.path.exists(SAMPLEDIR):
    os.makedirs(SAMPLEDIR)

def get_samples(epic_id):
    url = URLBASE + '{:.0f}.h5'.format(epic_id)
    filename = os.path.join(SAMPLEDIR, '{:.0f}.h5'.format(epic_id))

    try:
        f = h5py.File(filename, 'r')
        samples = f['samples'][...]
        cols = ["T", "delta", "T_tau", "period", "t0"]
        if samples.shape[1] > 5:
            df = []
            for i in range(0, samples.shape[1], 5):
                df.append(pd.DataFrame.from_items(zip(cols, 
                                                      samples[:, i:i+5].T)))
        else:
            df = pd.DataFrame.from_items(zip(cols, samples[:, :5].T))
    except:
        logging.error(filename)
        raise
        raise RuntimeError('You need to download file.')

    return df

class K2_TransitSignal(TransitSignal_FromSamples):
    def __init__(self, epic_id, i=None):
        samples = get_samples(epic_id)
        
        if(type(samples)==list):
            #integer nunmber must be passed
            samples = samples[i-1]
            period = PAPER1_TABLE.ix[epic_id, 'period'].iloc[i-1]
        else:
            period = PAPER1_TABLE.ix[epic_id, 'period']

        name = '{}'.format(epic_id)
        if i is None:
            name += '.1'
        else:
            name += '{:.0f}'.format(i)

        super(type(self),self).__init__(period, 
                                        samples['T'],
                                        samples['delta'],
                                        samples['T_tau'])
        self.name = name

