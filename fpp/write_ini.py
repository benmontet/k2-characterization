#!/usr/bin/env python
from __future__ import print_function, division

import numpy as np
import os, os.path, re, glob
from configobj import ConfigObj

from k2fpp.tables import PAPER1_TABLE, MAGS
from k2fpp.photometry import all_mags
from k2fpp.transitsignal import get_trsig

cands = np.loadtxt('allcands.list', dtype=str)

FOLDER = os.path.expanduser('~/repositories/k2-characterization/fpp/fppmodels')

def write_ini(epic_id, i=1, maxrad=12):
    filename ='{}/{}.{}/fpp.ini'.format(FOLDER, epic_id, i)
    config = ConfigObj()
    config.filename = filename

    config['name'] = '{}.{}'.format(epic_id, i)
        
    ra = PAPER1_TABLE.ix[epic_id,'ra']
    dec = PAPER1_TABLE.ix[epic_id,'dec']
    rprs = PAPER1_TABLE.ix[epic_id,'rprs']
    period = PAPER1_TABLE.ix[epic_id,'period']
    if np.size(ra) > 1:
        ra = ra.iloc[0]
        dec = dec.iloc[0]
        rprs = rprs.iloc[i-1]    
        period = period.iloc[i-1]

    config['ra'] = ra
    config['dec'] = dec
    config['rprs'] = rprs
    config['period'] = period

    mags = all_mags(epic_id)
    config['mags'] = {}
    for b in ['B','V','J','H','K',
              'W1','W2','W3']:
        mag, err = (mags[b], mags['{}err'.format(b)])
        config['mags'][b] = [mag,err]
    config['mags']['Kepler'] = mags['Kepler']

    config['constraints'] = {}
    config['constraints']['maxrad'] = maxrad
    ccfiles = glob.glob('{}/{}/*.cc'.format(FOLDER,config['name']))
    config['constraints']['ccfiles'] = [os.path.basename(f)
                                        for f in ccfiles]
    config.write()

def write_trsig(epic_id, i=1):
    trsig = get_trsig(epic_id, i)
    trsig.save('{}/{}.{}/trsig.pkl'.format(FOLDER, epic_id, i))
    
if __name__=='__main__':

    for cand in cands:
        m = re.search('(\d+)\.(\d)',cand)
        if m:
            epic_id = int(m.group(1))
            i = int(m.group(2))
            write_ini(epic_id, i)
            write_trsig(epic_id, i)
