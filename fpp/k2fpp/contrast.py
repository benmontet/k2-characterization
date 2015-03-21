from __future__ import print_function, division

import numpy as np
import os, os.path, glob
import re

from scipy.io.idl import readsav

from starutils.contrastcurve import ContrastCurve

from .photometry import all_mags

AODATA_DIR = os.path.expanduser('~/repositories/k2-characterization/aodata/proc')


def AO_contrast_curves(epic_id):
    ccs = []
    pattern = AODATA_DIR + '/*epic{}*'.format(epic_id)
    files = glob.glob(pattern)
    for f in files:
        m = re.search('_epic\d+_(\w+)_sat.*join.*_5sig.sav', f)
        if m:
            data = readsav(f)
            band = m.group(1).upper()
            if band=='KS':
                band = 'K'
            rs = data['conarr'][:,1]
            dmags = data['conarr'][:,0]
            coverage = data['conarr'][:,2]
            ok = coverage==1
            ccs.append(ContrastCurve(rs[ok],dmags[ok],band,
                                     name='PHARO'.format(band)))
    return ccs

def SDSS_contrast(epic_id):
    """fwhm 1.4", lim. mag r=22.2
    """
    mags = all_mags(epic_id)
    rs = [2.8,4,8,12] #blah blah
    dmag = 22.2-mags['r']
    dmags = [dmag]*len(rs)
    return ContrastCurve(rs,dmags,'r',name='SDSS')

def all_ccs(epic_id):
    ccs = AO_contrast_curves(epic_id)
    ccs.append(SDSS_contrast(epic_id))
    return  ccs


def write_ccs(epic_id, rootfolder=os.path.expanduser('~/repositories/k2-characterization/fpp/fppmodels')):
    ccs = all_ccs(epic_id)

    dirs = glob.glob('{}/{}.?'.format(rootfolder,epic_id))
    for dir in dirs:
        for cc in ccs:
            outfile = '{}/{}_{}.cc'.format(dir, cc.name, cc.band)
            np.savetxt(outfile, np.array([cc.rs,cc.dmags]).T)
    
