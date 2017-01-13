import csv

# Searches for key words within the expression, and checks them against thermo key words.
def keywordss(keywordfile):
    keywordmatrix = []
    #try:
    with open(keywordfile, 'rb') as csvfile:
        valreader = csv.reader(csvfile)
        for row in valreader:
            keywordmatrix.append(row)
    #except:
    #    logging.warning('Error.  File not found. Returning empty keyword matrix')
    # Now treat keywords Matrix,
    #replace all key variables:
    for i in range(0, len(keywordmatrix)):
        keywordmatrix[i][5] = len(keywordmatrix[i][0])
        for j in range(0, len(keywordmatrix)):
            if keywordmatrix[i][j] == 'apo':
                keywordmatrix[i][j] = "'"
    return keywordmatrix

all = keywordss('/Users/Josh/Sites/thetechnicalshed.com/therm/Keywords.csv')
