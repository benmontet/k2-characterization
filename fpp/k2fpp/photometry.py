from __future__ import print_function, division

from .tables import MAGS

def mags(epic_id):
    """returns dictionary of magnitudes
    """
    s = MAGS.ix[epic_id]
    d = {b:s[b] for b in s.index}
    del d['name']
    return d

