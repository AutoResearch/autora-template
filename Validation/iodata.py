import sys
import numpy as np
import pandas as pd

XVARS = {
    'RoughPipes' : [
        'LogRe',
        'Drratio',
    ],
    'RDFunding' : [
        'Attractiveness',
        'Stickiness',
        'GDP',
        'GDPRD',
        'GDPPP',
    ],
    'Trepat' : [
        'CDH1',
        'CDH2',
        'CDH3',
        'ALPHACAT',
        'BETACAT',
        'P120',
        'ZO1',
    ],
    'Ye'     : [
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
    ],
    'LogYe'     : [
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
    ],
    'Hydrogenation' : [
        'Barrier',
        'DE',
        'NC',
        'diH',
        'Tr(R)',
        'Tr(P)',
        'DTr',
        'det(R)',
        'det(P)',
        'det(TS)',
        'RxP',
        'RxTS',
        'rank(R)',
        'rank(P)',
        'rank(TS)',
        'SpecRad(R)',
        'SpecRad(P)',
        'Type',
        'ID'
    ]
}
YLABS = {
    'RoughPipes'   : 'logf',
    'RDFunding'    : 'FinancialSuccessRate',
    'Trepat'       : 'Sxx',
    'Ye'           : 'rec',
    'LogYe'        : 'Logrec',
    'Hydrogenation':'Barrier',
}
FNAMES = {
    'RoughPipes'   : 'nikuradze.csv',
    'RDFunding'    : 'EU_nature_clean.csv',
    'Trepat'       : 'cadhesome_protein.csv',
    'Ye'           : 'seymour.csv',
    'LogYe'        : 'seymour.csv',
    'Hydrogenation':'H_features.csv',
}

def read_data(dset, ylabel=None, xlabels=None, in_fname=None):
    # Default values
    if ylabel == None:
        ylabel = YLABS[dset]
    if xlabels == None:
        xlabels = XVARS[dset]
    if in_fname == None:
        in_fname = '%s/data/%s' % (dset, FNAMES[dset])
    # Read 
    if (dset == 'RDFunding' or
        dset == 'RoughPipes' or
        dset == 'Trepat' or
        dset == 'Ye' or
        dset=='Hydrogenation'):
        data = pd.read_csv(in_fname)
        x = data[xlabels]
        y = data[ylabel]
    elif (dset == 'LogYe'):
        data = pd.read_csv(in_fname)
        data['Logrec'] = np.log(data['rec'])
        x = data[xlabels]
        y = data[ylabel]        
    else:
        raise

    # Done
    return data, x, y

# Test main
if __name__ == '__main__':
    data, x, y = read_data(sys.argv[1])
    print data
    print x
    print y
