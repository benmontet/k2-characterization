#!/usr/bin/env python

import numpy as np
import os, os.path, shutil

dest_folder = os.path.expanduser('~/WWW/public/k2/starmodels')

all_cands = np.unique(np.loadtxt('all.list', dtype=int))

for cand in all_cands:
    folder = '{}.1'.format(cand)
    h5file = '{}/dartmouth_starmodel_single.h5'.format(folder)
    triangle = '{}/dartmouth_triangle_single_physical.png'.format(folder)

    
