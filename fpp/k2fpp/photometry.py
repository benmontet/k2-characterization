from __future__ import print_function, division

from .tables import MAGS

def all_mags(epic_id):
    """returns dictionary of magnitudes
    """
    s = MAGS.ix[epic_id]
    d = {b:s[b] for b in s.index}
    del d['name']

    if (d['g'] - d['r']) <= 0.8:
        d['Kepler'] = 0.2*d['g'] + 0.8*d['r']
    else:
        d['Kepler'] = 0.1*d['g'] + 0.9*d['r']

    return d

