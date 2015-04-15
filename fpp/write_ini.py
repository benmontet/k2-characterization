#!/usr/bin/env python
from __future__ import print_function, division

import numpy as np
import pandas as pd
import os, os.path, re, glob
from configobj import ConfigObj

from k2fpp.tables import PAPER1_TABLE, MAGS, APERTURES
from k2fpp.photometry import all_mags
from k2fpp.transitsignal import get_trsig

SECONDARY_FILE = os.path.expanduser('~/repositories/k2-characterization'+
                                    '/fpp/secondary.csv')
SECONDARY = pd.read_csv(SECONDARY_FILE, 
                        names=['epic_id','period',
                               'primary','t0_1',
                               'secondary','t0_2'])
SECONDARY.index = SECONDARY['epic_id']


cands = np.loadtxt('allcands.list', dtype=str)

FOLDER = os.path.expanduser('~/repositories/k2-characterization/fpp/fppmodels')



def max_secondary(epic_id, i=1):
    secdepth = SECONDARY.ix[epic_id, 'secondary']
    if np.size(secdepth) > 1:
        secdepth = secdepth.iloc[i-1]
    return secdepth/1e3


def write_ini(epic_id, i=1, photerr_inflate=3):
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
    for b in ['B','V','g','r','i','J','H','K',
              'W1','W2','W3']:
        mag, err = (mags[b], mags['{}err'.format(b)])
        config['mags'][b] = [mag,err*photerr_inflate]
    config['mags']['Kepler'] = mags['Kepler']

    config['constraints'] = {}
    config['constraints']['maxrad'] = (APERTURES.ix[epic_id, 'radius'] + 1)*4
    config['constraints']['secthresh'] = max_secondary(epic_id, i)
    ccfiles = glob.glob('{}/{}/*.cc'.format(FOLDER,config['name']))
    if len(ccfiles) > 0:
        config['constraints']['ccfiles'] = [os.path.basename(f)
                                            for f in ccfiles]
    config.write()

def write_trsig(epic_id, i=1, redo=False):
    trsig_file = '{}/{}.{}/trsig.pkl'.format(FOLDER, epic_id, i)
    if not os.path.exists(trsig_file) and not redo:
        trsig = get_trsig(epic_id, i)
        trsig.save(trsig_file)
    
if __name__=='__main__':

    from k2fpp.contrast import write_all_ccs
    write_all_ccs()

    for cand in cands:
        m = re.search('(\d+)\.(\d)',cand)
        if m:
            epic_id = int(m.group(1))
            i = int(m.group(2))
            write_ini(epic_id, i)
            write_trsig(epic_id, i)
