#!/usr/bin/env python

import re
import os, os.path, glob

from k2fpp.fpp import max_secondary

def prob_entry(val):
    val = float(val)
    if val > 1e-4:
        return '${:.2g}$'.format(val)
    else:
        return '$< 10^{-4}$'

def format_line(line, fpp):
    fpp = float(fpp)
    newline = line
    if fpp < 0.01:
        newline = ''
        for v in line.split('&'):
            m = re.search('(.*)\s+\\\\',v)
            if m:
                newline += r' {\bf ' + m.group(1) + '} \\\\\n'
            else:
                newline += r' {\bf ' + v + '} &'
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
\begin{deluxetable*}{lcllllll}
\tablewidth{0pt}
\tabletypesize{\scriptsize}
\tablecaption{False Positive Probability Calculation Results}
\label{Tab:FPP}
\tablehead{
\colhead{EPIC} &
\colhead{Cand. Num.} &
\colhead{max($\delta_{\rm sec}$)} &
\colhead{${\rm Pr}_{\rm EB}$} &
\colhead{${\rm Pr}_{\rm BEB}$} &
\colhead{${\rm Pr}_{\rm HEB}$} &
\colhead{$f_{p}$} &
\colhead{FPP}
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
    line = '${}$ & ${}$ & '.format(epic_id,i)
    line += '${:.2f}$ & '.format(max_secondary(epic_id,i)*1e3)
    for val in [eb,beb,heb]:
        val = float(val)
        line += '{} & '.format(prob_entry(val))
    line += '${:.2f}$ & '.format(float(fp))
    line += '{} '.format(prob_entry(FPP))
    if f != folders[-1]:
        line += '\\\\'
    line += '\n'
    fout.write(format_line(line,FPP))


fout.write(r"""
\enddata
\tablecomments{blurgh.}
\end{deluxetable*}
""")

fout.close()
