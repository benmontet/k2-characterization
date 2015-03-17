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
        m = re.search('_epic\d+_(\w+)_sat_medcomb_qlconprofiles.sav', f)
        if m:
            data = readsav(f)
            band = m.group(1).upper()
            if band=='KS':
                band = 'K'
            bins = data['angscalearr']
            dmags = data['fivesigqlconprof']
            coverage = data['corfraccoverage']
            coverage[0] = 1.
            if len(bins)==1 + len(dmags):
                bin_centers = (bins[1:]+bins[:-1])/2
            else:
                bin_centers = bins
            ccs.append(ContrastCurve(bin_centers,dmags,band,
                                     name='PHARO {} band'.format(band)))
    return ccs

def SDSS_contrast(epic_id):
    """fwhm 1.4", lim. mag r=22.2
    """
    mags = all_mags(epic_id)
    rs = [2.8,4,8,12] #blah blah
    dmag = 22.2-mags['r']
    dmags = [dmag]*len(rs)
    return ContrastCurve(rs,dmags,'r',name='SDSS r band')

def all_ccs(epic_id):
    ccs = AO_contrast_curves(epic_id)
    ccs.append(SDSS_contrast(epic_id))
    return  ccs

    
