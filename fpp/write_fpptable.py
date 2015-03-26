#!/usr/bin/env python

import re
import os, os.path, glob
import numpy as np

from k2fpp.fpp import max_secondary
from k2fpp.contrast import AO_contrast_curves

FP_OVERRIDE = ['201555883.01']

notes = {'1': 'Maximum depth [ppt] of potential secondary eclipse signal.',
         '2': 'Whether adaptive optics imaging has been obtained.',
         '3': 'Integrated planet occurrence rate assumed between 0.7$\times$'+\
              'and 1.3$\times$ the candidate\'s radius',
         '4': 'Declared a false positive because of epoch match' +\
              'to XXXXXXXX'}

def note(key):
    return '\tablenotemark{{}}'.format(key)

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

def format_line(line, fpp, force_fp=False):
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
    if fpp > 0.9 or force_fp:
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
\colhead{max($\delta_{\rm sec}$) [ppt]\tablenotemark{1}} &
\colhead{AO?\tablenotemark{2}} &
\colhead{${\rm Pr}_{\rm EB}$} &
\colhead{${\rm Pr}_{\rm BEB}$} &
\colhead{${\rm Pr}_{\rm HEB}$} &
\colhead{$f_{p}$\tablenotemark{3}} &
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
    cand_name = '{}.{:02.0f}'.format(epic_id, i)

    line = '{} & '.format(cand_name)  # EPIC, Cand. Num.
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
    if cand_name in FP_OVERRIDE:
        disp = 'FP'
        if cand_name=='201555883.01':
            disp = r'FP\tablenotemark{a}'
    else:
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
    force_fp = cand_name in FP_OVERRIDE

    fout.write(format_line(line,FPP,force_fp=force_fp))


fout.write(r"""
\enddata
\tablecomments{Results of the \texttt{vespa} astrophysical 
false positive probability calculations for all candidates.  
Likely false positives (FPP $> 0.9$, or otherwise designated)
 are marked in red.  
Candidates are declared to be validated planets if FPP $< 0.01$.  
EB, BEB, and HEB refer to the three considered astrophysical 
false positive scenarios, and the relative probability of 
each is listed in the appropriate column.}
\tablenotetext{1}{Maximum depth of potential secondary eclipse signal.}
\tablenotetext{2}{Whether adaptive optics observation is presented in this paper.}
\tablenotetext{3}{Integrated planet occurrence rate assumed between 0.7$\times$ and 1.3$\times$ the candidate radius}
\tablenotetext{a}{Declared a false positive because of epoch match to 201569483.01 (see \S\ref{sec:ephemmatch}).}
\end{deluxetable*}
""")

fout.close()
