import logging
import csv

# Top of the script to make this universally accessible.
# Searches for key words within the expression, and checks them against thermo key words.
def keywords(keywordfile):
    keywordmatrix = []
    try:
        with open(keywordfile, 'rb') as csvfile:
            valreader = csv.reader(csvfile)
            for row in valreader:
                keywordmatrix.append(row)
    except:
        logging.warning('Error.  File not found. Returning empty keyword matrix')
    # Now treat keywords Matrix,
    #replace all key variables:
    for i in range(0, len(keywordmatrix)):
        for j in range(0, len(keywordmatrix)):
            if keywordmatrix[i][j] == 'apo':
                keywordmatrix[i][j] = "'"
    return keywordmatrix