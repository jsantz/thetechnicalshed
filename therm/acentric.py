from thermo import acentric
import logging
import re
import keywords
import copy
import express

keywords = keywords.all
################################################################
# 1. Acentric Module
#       These perform the acentric module tasks.
################################################################
def casrn(expression, op):
    CASRN = keywords[1][0]
    # Check if omega is in same expression. (keywords 2,0)
    if expression.find(keywords[3][0]) != -1 \
            or expression.find(keywords[5][0]) != -1:
        return expression
    else:
        # Extract the CASRN function:
        casrn = expression.find(CASRN)
        end = keywords[1][2]
        start = keywords[1][1]
        delimeter = keywords[1][3]
        startindex = expression.find(start, casrn)
        endindex = expression.find(end, startindex + 1)
        element = copy.copy(expression[casrn:endindex])
        expression.replace(element, "")

# Kind of a useless function.
def omegacasrn(expression, op):
    # Check for CASRN (keywords 1, 0)
    CASRN = keywords[1][0]
    omegas = op[0]
    if expression.find(str(CASRN)) == -1:
        logging.warning('Error, omega function requires CASRN variable.')
        return expression
    else:
        # Extract the CASRN function:
        casrn = expression.find(CASRN)
        end = keywords[1][2]
        start = keywords[1][1]
        delimeter = keywords[1][3]
        startindex = expression.find(start, casrn)
        endindex = expression.find(end, startindex + 1)
        arg = copy.copy(expression[startindex + 1:endindex])
    # Extract the omega function
    om = expression.find(omegas)
    e = op[2]
    s = op[1]
    d = op[3]
    si = expression.find(s, om)
    ei = expression.find(e, si + 1)
    # Execute the function omega(CASRN='args')
    returnval = acentric.omega(CASRN=arg)
    express = copy.copy(expression[om:ei + 1])
    expression = expression[:om] + str(returnval) + s[ei + 1:]
    return expression

def omegamix(expression, op):
    arg = express.extractargs(expression, op)
    arrays = express.extractarrays(arg)
    if len(arrays) != 2:
        logging.warning("Too Many/Few Arguments for omega_mixture{}")
        return expression
    try:
        return acentric.omega_mixture(arrays[0], arrays[1])
    except:
        return express.cacfailure(expression,op)

def LKomega(expression, op):
    # Get LKomega syntax from csv.
    # Extract Extract args
    arg = express.extractargs(expression, op)
    args = arg.split(op[3])  # 3 Args
    if len(args) != 3:
        return expression
    try:
        return acentric.LK_omega(float(args[0]), float(args[1]), float(args[2]))
    except:
        return express.cacfailure(expression, op)

#Calculation of the stiel polar factor...
def StielPol(expression, op):
    arg = express.extractargs(expression, op)
    casrn = express.extractargs(arg, keywords[1])
    array = re.findall(r"[-+]?\d*\.\d+|\d+", arg)
    if(len(array) != 6):
        logging.warning("Error, Too many/few arguments")
        return expression
    try:
        return acentric.StielPolar(float(array[0]), float(array[1]), float(array[2]), CASRN=casrn)
    except:
        return express.cacfailure(expression, op)
