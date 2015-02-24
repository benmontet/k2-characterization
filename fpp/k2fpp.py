from __future__ import print_function, division

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import logging

import os,os.path,sys,re

import parse_tables as pt

MAGS = pt.mag_table()
DARTMOUTH_PARS = pt.dartmouth_table()
PADOVA_PARS = pt.padova_table()
PAPER1_TABLE = pt.paper1_table()

def mags(epic_id):
    """returns dictionary of magnitudes
    """
    s = MAGS.ix[epic_id]
    d = {b:s[b] for b in s.index}
    del d['name']
    return d

    
