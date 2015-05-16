#!/usr/bin/env python

import numpy as np
import os, os.path, shutil

dest_folder = 'starmodels'

all_cands = np.unique(np.loadtxt('all.list').astype(int))

for cand in all_cands:
    folder = '{}.1'.format(cand)
    h5file = '{}/dartmouth_starmodel_single.h5'.format(folder)
    triangle1 = '{}/dartmouth_triangle_single_physical.png'.format(folder)
    triangle2 = '{}/dartmouth_triangle_single_observed.png'.format(folder)

    shutil.copy(h5file, '{}/{}.h5'.format(dest_folder, cand))
    shutil.copy(triangle1, '{}/{}_physical.png'.format(dest_folder, cand))
    shutil.copy(triangle2, '{}/{}_observed.png'.format(dest_folder, cand))

