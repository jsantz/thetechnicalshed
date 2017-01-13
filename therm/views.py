#from django.http import HttpResponse
#from django.http import Http404
from django.shortcuts import render, get_object_or_404
import keywords
import express
import functions
#import matrix of stored values
# Top of the script to make this universally accessible.
# Searches for key words within the expression, and checks them against thermo key words.

keywords = keywords.all
#################### Main Requests...################################
#
##################################################################

def index(request):
    response = ""
    inputmsg = "Enter Command"
    context = {
        'inputmsg': inputmsg,
        'response': response,
    }
    return render(request, 'therm/index.html', context)

def computetherm(request):
    #try:
    initial = request.POST['inputstring']
    response = interpreter(initial)
    inputmsg = initial
    #except:
    #    response = "unrecognized..."
    #    inputmsg = "Enter Command"
    context = {
        'inputmsg': inputmsg,
        'response': response,
    }
    return render(request, 'therm/index.html', context)

# The most Broad interpreter of user input.
def interpreter(response):
    #1.  -Count the number of elements in a string
    length = len(response)
    #2.  -Count the number of ( in a string
    LP = express.getcharindex(response, "(")
    #3.  -Count the number of ) in a string
    RP = express.getcharindex(response, ")")
    #4.  -Count the number of spaces in a string
    SP = express.getcharindex(response, " ")
    #5.  -Count the number of ' in string
    APo = express.getcharindex(response, "'")
    #6.  -Match Each () set and parse out each expression
    Matchsets = express.expressionclosure(response, LP, RP)
    #7.  -Execute Expressions:
    expressions = express.expressionparser(response, Matchsets)
    responses = functions.expressioncalc(expressions)
    #responses
    newresponse = "<pre style='text-align:center;'>"
    count = 1
    for response in responses:
        if count == len(responses):
            newresponse += "Final: " + response[1] + "<br> = " + response[0] + "<br><br>"
            break
        newresponse += str(count) +": "+ response[1] + "<br> = " + response[0] + "<br><br>"
        count+=1
    #newresponse += "( = " + str(LP) + "<br>"
    #newresponse += ") = " + str(RP) + "<br>"
    #newresponse += "spaces = " + str(SP) + "<br>"
    #newresponse += "' = " + str(APo) + "<br>"
    #newresponse += "Expression Sets = " + str(Matchsets) + "<br>"
    #newresponse += "Expressions = " + str(Expressions) + "<br>"
    newresponse += "</pre>"
    return newresponse