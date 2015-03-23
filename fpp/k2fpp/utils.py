import numpy as np
from scipy.integrate import quad

def fp_fressin(rp,dr=None):
    if dr is None:
        dr = rp*0.3
        fp = quad(fressin_occurrence,rp-dr,rp+dr)[0]
    return max(fp, 0.001) #to avoid zero

def fressin_occurrence(rp):
    """Occurrence rates per bin from Fressin+ (2013)
    """
    rp = np.atleast_1d(rp)
    sq2 = np.sqrt(2)
    bins = np.array([1/sq2,1,sq2,2,2*sq2,
                     4,4*sq2,8,8*sq2,
                     16,16*sq2])
    rates = np.array([0,0.155,0.155,0.165,0.17,0.065,0.02,0.01,0.012,0.01,0.002,0])
    return rates[np.digitize(rp,bins)]
