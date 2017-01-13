import copy
import logging
import re
#### Expression Functions
# these functions perform basic tasks related to strings
########################################################

# Retrieves the number of occurrences and indexes them all.
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

# Closes Expressions by finding likely () sets, orders them for operation.
def expressionclosure(response, LP, RP):
    #Case 1: There are exactly the same number of LP and RP
    if len(LP) == len(RP):
        Set = matcher(LP, RP)
    #Case 2: There are more LP than RP, behaves same as same number, excludes leftmost LP:
    #Case 3: There are more LP than RP, behaves same as same number, excludes rightmost RP:
    return Set

#Starts by finding the closest set of LP and RP, excludes, and recurses.
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

def extractargs(expression, op):
    si = expression.find(op[1],expression.find(op[0]))
    ei = expression.find(op[2],si+1)
    arg = copy.copy(expression[si+1:ei])
    return arg

#Extracts the array sets enclosed in []
def extractarrays(expression):
    arrays = []
    indexL = getcharindex(expression, "[")
    indexR = getcharindex(expression, "]")
    while(len(indexL) != len(indexR)):
        if len(indexL) > len(indexR):
            indexL.pop(0)
        if len(indexL) < len(indexR):
            indexR.pop()
        if len(indexL) < 1 or len(indexR) < 1:
            logging.warning("array Sizing Error has occured...")
            return []
    matchsets = matcher(indexL, indexR)
    matchsets.sort()
    for pair in matchsets:
        temp = copy.copy(expression[pair[0]+1:pair[1]])
        arrays.append(re.findall(r"[-+]?\d*\.\d+|\d+",temp))
    for i in range(0, len(arrays)):
        for j in range(0, len(arrays[i])):
            arrays[i][j] = float(arrays[i][j])
    return arrays

#If the calculation Fails, do not replace the whole string, leave uncalculated string
def cacfailure(expression, row):
    newexpress = row[0] + row[1] + expression.extractargs(expression, row) + row[2]
    return newexpress