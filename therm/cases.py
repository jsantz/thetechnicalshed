### Go through Acentric Cases.
def acentric(case, expression, op):
    import acentric
    if case == 2:
        return acentric.LKomega(expression, op)
    if case == 3:
        return acentric.omegacasrn(expression, op)
    if case == 4:
        return acentric.omegamix(expression, op)
    if case == 5:
        return acentric.StielPol(expression, op)
