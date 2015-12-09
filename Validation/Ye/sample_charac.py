import sys
import pandas as pd

sys.path.append('../../')
from mcmc import *

sys.path.append('../../10-Prior')
from fit_prior import read_prior_par

import iodata

VARS = [
    'eff',
    'D_max',
    'D_apr',
    'D_may',
    'D_jun',
    'ET_apr',
    'ET_may',
    'ET_jun',
    'PT_apr',
    'PT_may',
    'PT_jun',
    'PT_jul',
    'PDO_win',
]
Y = 'rec'
NS = 1000
THIN = 2000

if __name__ == '__main__':
    # Read the data
    inFileName = 'seymour.csv'
    data, x, y = iodata.read_data(
        ylabel=Y, xlabels=VARS, in_fname=inFileName,
    )
    prior_par = read_prior_par(sys.argv[1])

    # Get the output file ready
    outfname = 'sample_charac__%s__%s' % (inFileName,sys.argv[1].split('/')[-1])
    npar = outfname[outfname.find('.np') + 3:]
    npar = int(npar[:npar.find('.')])
    outf = open(outfname, 'w')
    print >> outf, '#', prior_par
    
    # Initialize
    t = Tree(
        variables=VARS,
        parameters=['a%d' % i for i in range(npar)],
        x=x, y=y,
        prior_par=prior_par,
    )
    print >> outf, '# Variables: ', t.variables
    print >> outf, '# Parameters:', t.parameters, '\n#'

    # Burnin
    for i in range(100):
        t.mcmc_step()

    # MCMC
    vprob = dict([(v, 0) for v in VARS])
    sizeprob = dict([(s, 0) for s in range(t.max_size+1)])
    nparprob = dict([(n, 0) for n in range(npar+1)])
    for i in range(NS):
        print >> outf, i+1, t.E, t.bic, t
        outf.flush()
        t.BT = 10.
        for kk in range(THIN/3):
            t.mcmc_step()
        t.BT = 1.
        t.get_energy(bic=True, reset=True)
        for kk in range(THIN):
            t.mcmc_step()
        for v in VARS:
            if v in [n.value for n in t.ets[0]]:
                vprob[v] += 1
        nparprob[len(set([n.value for n in t.ets[0]
                          if n.value in t.parameters]))] += 1
        sizeprob[t.size] += 1
        
    # Report
    print >> outf, '\n# formula size' 
    for s in sizeprob:
        print >> outf, s, sizeprob[s] / float(NS)

    print >> outf, '\n# variable use' 
    for v in vprob:
        print >> outf, v, vprob[v] / float(NS)

    print >> outf, '\n# parameters' 
    for n in nparprob:
        print >> outf, n, nparprob[n] / float(NS)

    # Done
    outf.close()
