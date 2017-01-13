import copy
import re
import keywords
import express
import cases
# Top of the script to make this universally accessible.
keywords = keywords.all

### Checking each of the key words in th expression
def execkeyword(keywords, expression):
    for row in keywords:
        #Check if the cases belong to ACENTRIC module.
        if str(row[6]) == 'acentric':
            expression = str(expression)
            if checkprotect(row, expression.find(row[0]), expression): #ignore CASRN Variable.
                calc = cases.acentric(int(row[4]), expression, row)
                expressval = row[0] + row[1] + express.extractargs(expression, row) + row[2]
                expression = expression.replace(expressval,str(calc))
    return expression

def checkprotect(row, test, expression):
    length = expression.find(row[1], test)
    if test != -1 and expression[test - 1] != "_" \
            and expression[test - 1].isalpha() is False \
            and length - test == int(row[5]) \
            and int(row[4]) != 1:  # ignore CASRN Variable.
        return True
    else:
        return False

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

def expressioncalc(expressions):
    responses = []
    for expression in expressions:
        orig = copy.copy(expression)
        calc = execkeyword(keywords, expression)
        responses.append([calc, orig])
    return responses


################################################################
# 2. Activity Module
#
################################################################

#lol = "(jo(rjr (asdf)(asdf) 0're)r# t r(sdfsdflk))'"
lol = "((omega{CASRN='64-17-5'})*(LK_omega{425.6, 631.1, 32.1E5})*(omega_mixture{[0.025, 0.12], [0.3, 0.7]})*(StielPolar{647.3, 22048321.0, 0.344, CASRN='7732-18-5'}))"

LP = express.getcharindex(lol, "(")
RP = express.getcharindex(lol, ")")
sets = express.expressionclosure(lol, LP, RP)
expressions = express.expressionparser(lol, sets)
response = expressioncalc(expressions)
#Casrntest = execkeyword(keywords, expressions[0])
#lkomegatest = execkeyword(keywords, expressions[1])
#omegamixtest = execkeyword(keywords, expressions[2])
#stieltest = execkeyword(keywords, expressions[3])

lol=2349234