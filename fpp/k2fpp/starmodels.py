from __future__ import print_function, division

import matplotlib.pyplot as plt
import re, os, os.path
import numpy as np
import pandas as pd

import logging

from isochrones.starmodel import StarModel
from isochrones.dartmouth import Dartmouth_Isochrone

from .photometry import all_mags

DARTMOUTH = Dartmouth_Isochrone()

STARMODEL_DIR = 'starmodels_inflated_nogri'

class EPIC_StarModel(StarModel):
    def __init__(self, epic_id, exclude_bands=['W4','g','r','i'],
                 maxAV=0.1, max_distance=2000, refit=False, inflate_error=3,
                 **kwargs):

        self.epic_id = epic_id

        mags = all_mags(epic_id)
        kws = {}
        for k,v in mags.items():
            if re.search('err',k) or k=='Kepler':
                continue
            if k not in exclude_bands:
                kws[k] = (v, mags['{}err'.format(k)]*inflate_error)
                
        super(type(self),self).__init__(DARTMOUTH, maxAV=maxAV,
                                        max_distance=max_distance,
                                        **kws)

    def fit_mcmc(self, save=True, **kwargs):
        super(type(self),self).fit_mcmc(**kwargs)
        filename = os.path.join(STARMODEL_DIR,
                                '{}.h5'.format(self.epic_id))
        if save:
            self.save_hdf(filename)

    def save_hdf(self,filename=None, path=''):
        if filename is None:
            filename = os.path.join(STARMODEL_DIR,
                                    '{}.h5'.format(self.epic_id))
        StarModel.save_hdf(self, filename, path=path)

    @classmethod
    def load_hdf(cls, filename, path=''):
        return StarModel.load_hdf(filename, path=path)

def get_starmodel(epic_id, refit=False, **kwargs):
    filename = os.path.join(STARMODEL_DIR,'{}.h5'.format(epic_id))
    try:
        if refit:
            raise ValueError
        return StarModel.load_hdf(filename)
    except:
        model = EPIC_StarModel(epic_id, **kwargs)
        logging.info('Fitting {} starmodel...'.format(epic_id))
        model.fit_mcmc()
        return model
