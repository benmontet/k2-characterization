from __future__ import print_function, division

import re
import numpy as np
import pandas as pd

from isochrones.starmodel import StarModel
from isochrones.dartmouth import Dartmouth_Isochrone

from .photometry import all_mags

DARTMOUTH = Dartmouth_Isochrone()

STARMODEL_DIR = 'starmodels'

class EPIC_StarModel(StarModel):
    def __init__(self, epic_id, exclude_bands=['B','V','g','r','i','W4'],
                 maxAV=0.1, refit=False, **kwargs):

        self.epic_id = epic_id

        filename = os.path.join(STARMODEL_DIR,'{}.h5'.format(epic_id))
        if os.path.exists(filename) and not refit:
            self = StarModel.load_hdf(filename)
            self.epic_id = epic_id #hack-y
        else:
            mags = all_mags(epic_id)
            kws = {}
            for k,v in mags.items():
                if re.search('err',k):
                    continue
                if k not in exclude_bands:
                    kws[k] = (v, mags['{}err'.format(k)])

            super(type(self),self).__init__(DARTMOUTH, maxAV=maxAV,
                                            **kws)

    def save_hdf(self,filename=None, path=''):
        if filename is None:
            filename = os.path.join(STARMODEL_DIR,
                                    '{}.h5'.format(self.epic_id))
        StarModel.save_hdf(self, filename, path=path)

    @classmethod
    def load_hdf(cls, filename, path=''):
        return StarModel.load_hdf(filename, path=path)

