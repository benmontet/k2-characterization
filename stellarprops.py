import numpy as np
import pandas
import matplotlib.pyplot as plt


params = ['Teff', 'logg', 'mass', 'radius', 'feh', 'distance']

stars = ['201912552']
'''
stars =     ['201208431', '201257461', '201208431', '201257461', '201295312', '201338508', 
'201367065', '201384232', '201393098', '201403446', '201445392', '201465501', '201505350', 
'201546283', '201549860', '201555883', '201565013', '201569483', '201577035', '201596316', 
'201613023', '201617985', '201629650', '201635569', '201649426', '201702477', '201736247', 
'201754305', '201779067', '201828749', '201855371', '201912552', '201929294']
'''

for thisstar in stars:

    fname = 'starmodels/' + thisstar + '.h5'
    print fname
    data = pandas.read_hdf(fname, 'samples')


    for thisparam in params:
        samps = data[thisparam]    

        plt.hist(samps, np.linspace(np.min(samps), np.max(samps), 100))
        plt.xlabel(thisparam)
        
        stdm = np.percentile(samps, 15.8)
        stdp = np.percentile(samps, 84.2)
        medn = np.percentile(samps, 50.0)
        
        print medn, stdm-medn, stdp-medn
        
        
        plt.show()