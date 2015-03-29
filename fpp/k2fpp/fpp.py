from __future__ import print_function, division

from vespa.fpp import FPPCalculation
from vespa.populations import PopulationSet
import os, os.path
import numpy as np
import pandas as pd
import logging

from .transitsignal import K2_TransitSignal
from .tables import PAPER1_TABLE
from .starmodels import get_starmodel
from .photometry import all_mags
from .utils import fp_fressin

#K2_FPPDIR = os.getenv('K2_FPPDIR',
#                      os.path.expanduser(os.path.join('~','.k2fpp')))
K2_FPPDIR = 'fppmodels'

from astropy import constants as const
RSUN = const.R_sun.cgs.value
REARTH = const.R_earth.cgs.value

SECONDARY_FILE = os.path.expanduser('~/repositories/k2-characterization'+
                                    '/fpp/secondary.csv')
SECONDARY = pd.read_csv(SECONDARY_FILE, 
                        names=['epic_id','period',
                               'primary','t0_1',
                               'secondary','t0_2'])
SECONDARY.index = SECONDARY['epic_id']

def max_secondary(epic_id, i=1):
    secdepth = SECONDARY.ix[epic_id, 'secondary']
    if np.size(secdepth) > 1:
        secdepth = secdepth.iloc[i-1]
    return secdepth/1e3

class K2_FPPCalculation(FPPCalculation):
    def __init__(self, epic_id, i=None,
                 recalc=False, **kwargs):
        
        name = '{}'.format(epic_id)
        if i is None:
            name += '.1'
        else:
            name += '.{:.0f}'.format(i)

        ra = PAPER1_TABLE.ix[epic_id,'ra']
        dec = PAPER1_TABLE.ix[epic_id,'dec']
        rprs = PAPER1_TABLE.ix[epic_id,'rprs']
        if np.size(ra) > 1:
            ra = ra.iloc[0]
            dec = dec.iloc[0]
            if i is None:
                raise ValueError('{} has {} candidates.  ' +\
                                     'Please provide index'.format(epic_id,
                                                                   len(ra)))
            rprs = rprs.iloc[i-1]
        folder = os.path.join(K2_FPPDIR,name)
        if not os.path.exists(folder):
            os.makedirs(folder)
        trsig = K2_TransitSignal(epic_id, i)
        period = trsig.period
        

        popsetfile = os.path.join(folder, 'popset.h5')
        if os.path.exists(popsetfile) and not recalc:
            popset = PopulationSet(popsetfile)

        else:
            starmodel = get_starmodel(epic_id)
            mags = all_mags(epic_id)

            rstar = np.median(starmodel.samples['radius'])
            rp = rstar * rprs * RSUN/REARTH
            fp_specific = fp_fressin(rp)

            trilegal_filename = os.path.join(folder,'starfield.h5')
            
            popset = PopulationSet(trilegal_filename=trilegal_filename,
                                   starmodel=starmodel, mags=mags,
                                   rprs=rprs, 
                                   period=period, ra=ra, dec=dec,
                                   savefile=popsetfile,
                                   pl_kws={'fp_specific':fp_specific},
                                   **kwargs)

        FPPCalculation.__init__(self, trsig, popset, folder=folder)
        self.apply_secthresh(max_secondary(epic_id, i))


