#!/usr/bin/env python

import re
import os, os.path, glob
import numpy as np

from k2fpp.fpp import max_secondary
from k2fpp.contrast import AO_contrast_curves

notes = {'a': 'Maximum depth [ppt] of potential secondary eclipse signal.',
         'b': 'Whether adaptive optics imaging has been obtained.',
         'c': 'Integrated planet occurrence rate assumed between 0.7$\times$'+\
              'and 1.3$\times$ the candidate\'s radius',
         'd': 'Declared a false positive because of epoch match' +\
              'to XXXXXXXX'}

def prob_entry(val):
    val = float(val)
    if val > 1e-4:
        if val < 0.01:
            lv = -np.floor(np.log10(val))
            return '${:.1f}\\times10^{{-{:.0f}}}$'.format(val*10**lv,lv)
        else:
            return '${:.3f}$'.format(val)
    else:
        return '$< 10^{-4}$'

def format_line(line, fpp):
    fpp = float(fpp)
    newline = line
    if fpp < 0.01 and False: #not bothering to bold.
        newline = ''
        for v in line.split('&'):
            m = re.search('\$(.*)\$\s+\\\\',v)
            if m:
                newline += r' $\mathbf{' + m.group(1) + '}$ \\\\\n'
            else:
                m = re.search('\$(.*)\$',v)
                if m:
                    newline += r' $\mathbf{ ' + m.group(1) + '}$ &'
    if fpp > 0.9:
        newline = ''
        for v in line.split('&'):
            m = re.search('(.*)\s+\\\\',v)
            if m:
                newline += r' \color{red} ' + m.group(1) + '\\\\\n'
            else:
                newline += r' \color{red} ' + v + ' &'
        
    return newline
        

fout = open('../table_fpp.tex','w')

fout.write(r"""
\clearpage
%\LongTables
\begin{deluxetable*}{ccccccccc}
\tablewidth{0pt}
\tabletypesize{\scriptsize}
\tablecaption{False Positive Probability Calculation Results}
\label{Table:FPP}
\tablehead{
\colhead{Candidate} &
\colhead{max($\delta_{\rm sec}$)} &
\colhead{AO?} &
\colhead{${\rm Pr}_{\rm EB}$} &
\colhead{${\rm Pr}_{\rm BEB}$} &
\colhead{${\rm Pr}_{\rm HEB}$} &
\colhead{$f_{p}$} &
\colhead{FPP} &
\colhead{Disposition}
}
\startdata
""")

folders = glob.glob('fppmodels/*')
folders.sort()
for f in folders:
    resultsfile = f + '/results.txt'
    for line in open(resultsfile,'r'):
        line = line.split()
    beb,eb,heb,pl,fpV,fp,FPP = line

    m = re.search('(\d+)\.(\d)',f)
    epic_id = int(m.group(1))
    i = int(m.group(2))
    line = '{}.{:02.0f} & '.format(epic_id, i)  # EPIC, Cand. Num.
    line += '${:.2f}$ & '.format(max_secondary(epic_id,i)*1e3) #max(delta_sec)
    ccs = AO_contrast_curves(epic_id)
    if len(ccs)>0:
        line += ' Y & '
    else:                #AO?
        line += ' - & '

    for val in [eb,beb,heb]:
        val = float(val)
        line += '{} & '.format(prob_entry(val))  #pEB, pBEB, pHEB
    line += '${:.2f}$ & '.format(float(fp)) #fp_specific
    line += '{} & '.format(prob_entry(FPP)) #FPP
    FPP = float(FPP)
    if FPP < 0.01:
        disp = 'Planet'
    elif FPP > 0.9:
        disp = 'FP'
    else:
        disp = 'Candidate'
    line += '{} '.format(disp)  #Disposition
    if f != folders[-1]:
        line += '\\\\'
    line += '\n'
    #fout.write(line)
    fout.write(format_line(line,FPP))


fout.write(r"""
\enddata
\tablecomments{blurgh.}
\end{deluxetable*}
""")

fout.close()
