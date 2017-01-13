import copy
from thermo import *
import logging
import re
import functions

#import matrix of stored values
keywords = functions.keywords('../Keywords.csv')

def getcharindex(response, char):
    indexes = []
    ind = 0
    start = 0
    while start < len(response):
        try:
            ind = response.index(char, start)
        except:
            break
        indexes.extend([ind])
        start = ind + 1
    return indexes


def matcher(LP, RP):
    tLP = copy.copy(LP)
    tRP = copy.copy(RP)
    Sets = []
    for z in range(0, len(tRP)):
        minval = 99999
        for x in range(0, len(tRP)):
            for y in range(0, len(tLP)):
                test = tRP[x] - tLP[y]
                if abs(test) < minval and tRP[x] > tLP[y]:
                    minval = test
                    index = y
                    indes = x
        Sets.append([copy.copy(tLP[index]), copy.copy(tRP[indes])])
        tRP[indes] = 100000
        tLP[index] = 0
    return Sets

#parses out each individual expression.
def expressionparser(response, Sets):
    expressions = []
    for x in Sets:
        expressions.append(copy.copy(response[x[0]+1:x[1]]))
    return expressions

### Checking each of the key words in th expression
def execkeyword(keywords, expression):
    for row in keywords:
        expression = str(expression)
        test = expression.find(row[0])
        length = expression.find(row[1],test)
        if test != -1 and expression[test - 1] != "_" \
                and expression[test - 1].isalpha() is False \
                and length-test == int(row[5]):
            expression = cases(row[4], expression, row)
    return expression

#Executor for basic Maths.
def execbasicmaths(expression):
    #basic Operators
    operators = ['+', '-', '*', '/']
    #Extract every digit, floats and ints and store them.
    ints = map(int, re.findall(r'\d+', expression))
    floats = re.findall("\d+\.\d+", expression)
    for op in operators:
        test = expression.find(op)
        #if test != -1:
    return expression

### Writing each of the cases for protected words.
#Case 1
def casrn(expression, op):
    CASRN = keywords[1][0]
    # Check if omega is in same expression. (keywords 2,0)
    if expression.find(keywords[3][0]) != -1 \
            or expression.find('StielPolar'):
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

#Case 2
def omegacasrn(expression, op):
    #Check for CASRN (keywords 1, 0)
    CASRN = keywords[1][0]
    omegas = op[0]
    if expression.find(str(CASRN)) == -1:
        logging.warning('Error, omega function requires CASRN variable.')
        return expression
    else:
        #Extract the CASRN function:
        casrn = expression.find(CASRN)
        end = keywords[1][2]
        start = keywords[1][1]
        delimeter = keywords[1][3]
        startindex = expression.find(start, casrn)
        endindex = expression.find(end, startindex + 1)
        arg = copy.copy(expression[startindex+1:endindex])
    #Extract the omega function
    om = expression.find(omegas)
    e = op[2]
    s = op[1]
    d = op[3]
    si = expression.find(s, om)
    ei = expression.find(e, si + 1)
    #Execute the function omega(CASRN='args')
    returnval = omega(CASRN=arg)
    express = copy.copy(expression[om:ei+1])
    expression = expression[:om] + str(returnval) + s[ei+1:]
    return expression

#def case 3 takes in args as LKomega(arg, arg, arg)
def LKomega(expression, op):
    #Get LKomega syntax from csv.
    LKom = op[0]
    #Extract LKomega
    LK = expression.find(LKom)
    e = op[2]
    s = op[1]
    d = op[3]
    si = expression.find(s,LK)
    ei = expression.find(e,si+1)
    arg = copy.copy(expression[si+1:ei])
    args = arg.split(d) #3 Args
    if len(args) != 3:
        return expression
    return LK_omega(float(args[0]), float(args[1]), float(args[2]))

### The Cases placed into an object
def cases(case, expression, op):
    if int(case) == 1:
        return casrn(expression, op)
    if int(case) == 2:
        return LKomega(expression, op)
    if int(case) == 3:
        return omegacasrn(expression, op)


#lol = "(jo(rjr (asdf)(asdf) 0're)r# t r(sdfsdflk))'"
lol = "((omega{CASRN='64-17-5'})*(LK_omega{425.6, 631.1, 32.1E5}))"

LP = getcharindex(lol, "(")
RP = getcharindex(lol, ")")
sets = matcher(LP, RP)
expressions = expressionparser(lol, sets)
Casrntest = execkeyword(keywords, expressions[0])
lkomegatest = execkeyword(keywords, expressions[1])

lol=2349234


