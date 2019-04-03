from grammar import CFG

variables = [
    's',
    'np',
    'vp',
    'det',
    'n',
    'v',
    'pp',
    'p'
    ]

S = 's'

rules = [
    's -> np, vp',
    'np -> det, n',
    'vp -> vp, pp',
    'vp -> v, np',
    'vp -> eats',
    'pp -> p, np',
    'np -> det n',
    'np -> she',
    'v -> eats',
    'p -> with',
    'n -> fish',
    'n -> fork',
    'det -> a'
    ]
    

gram = CFG(variables, rules, S)





























