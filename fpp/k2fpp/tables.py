from __future__ import print_function, division
import re,sys,os
import pandas as pd

__all__ = ['parse_value', 'paper1_table', 'mag_table',
           'dartmouth_table', 'padova_table',
           'MAGS','DARTMOUTH_PARS',
           'PADOVA_PARS','PAPER1_TABLE']

def parse_value(entry):
    """parse latex table entry = number +/- stuff
    """
    m = re.search('\$\s*(\d+\.?\d+)_\{-(\d+\.?\d+)\}\^\{\+(\d+\.?\d+)\}\s*\$',entry)
    if m:
        return float(m.group(1)), float(m.group(2)), float(m.group(3))

def paper1_table(filename='paper1_tab-cand.tex'):
    epic_id = []
    ra = []
    dec = []
    period = []
    epoch = []
    rprs = []
    for line in open(filename):
        if re.search('EPIC', line):
            continue
        line = line.split('&')
        if len(line) < 6:
            continue
        epic_id.append(int(line[0]))
        ra.append(float(line[1]))
        dec.append(float(line[2]))
        per, lo, hi = parse_value(line[3])
        period.append(per)
        ep, lo, hi = parse_value(line[4])
        epoch.append(ep)
        r, lo, hi = parse_value(line[5])
        rprs.append(r)
    df = pd.DataFrame({'epic_id':epic_id,
                         'ra':ra,
                         'dec':dec,
                         'period':period,
                         'epoch':epoch,
                         'rprs':rprs})
    df.index = df['epic_id']
    return df

def padova_table(filename='../padova_params.txt'):
    df = pd.read_table(filename, delim_whitespace=True, skiprows=1,
                       names=['epic_id','teff','e_teff',
                              'radius','e_radius','distance',
                              'e_distance','mass','e_mass',
                              'feh','e_feh'])
    df.index = df['epic_id'].astype(int)
    return df

def dartmouth_table(filename='../dartmouth_params.txt'):
    df = pd.read_table(filename, delim_whitespace=True, skiprows=1,
                       names=['epic_id','teff','e_teff',
                              'radius','e_radius','distance',
                              'e_distance','mass','e_mass',
                              'feh','e_feh'])
    df.index = df['epic_id'].astype(int)
    return df

def mag_table(filename='../table_photometry.txt'):
    df = pd.read_table(filename, delim_whitespace=True)
    df.index = df['name']
    return df

MAGS = mag_table()
DARTMOUTH_PARS = dartmouth_table()
PADOVA_PARS = padova_table()
PAPER1_TABLE = paper1_table()

