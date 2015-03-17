from __future__ import print_function, division

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import logging

import os,os.path,sys,re

from .tables import MAGS, DARTMOUTH_PARS, PADOVA_PARS, PAPER1_TABLE

def mags(epic_id):
    """returns dictionary of magnitudes
    """
    s = MAGS.ix[epic_id]
    d = {b:s[b] for b in s.index}
    del d['name']
    return d



