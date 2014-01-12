import requests
import time
import numpy
import smtplib
from local_settings import *

buyapi = 'https://coinbase.com/api/v1/prices/buy'
sellapi = 'https://coinbase.com/api/v1/prices/sell'

lastbuy = []
lastsell = []

backoff = 1
x = 1

def sendmail(length, arr, price):
    msg = 'Hello world.'
    server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromemail , pwd)
    server.sendmail(fromemail , toemail, "The price is " + str(price) + " with array length " + str(length) + "\n array: " + str(arr))
    server.close()



def memoize(func):
    memo = dict()
    def decorated(n):
        if n not in memo:
            memo[n] = func(n)
        return memo[n]

    return decorated

@memoize
def fib(n):
    if n<=1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def getbuy():
    global lastbuy
    global backoff
    price = requests.get(buyapi).json()['total']['amount']

    if len(lastbuy) == 0 or len(lastbuy) > 0 and float(price) != lastbuy[0]:
        backoff = 1
        print "new buy price: " + price
        lastbuy.insert(0,float(price))
        print "buy history: " + str(lastbuy)


def getsell():
    global lastsell
    global backoff
    price = requests.get(sellapi).json()['total']['amount']
    if len(lastsell) == 0 or len(lastsell) > 0 and float(price) != lastsell[0]:
        backoff = 1
        print "new sell price: " + price
        lastsell.insert(0, float(price))
        print "sell history: " + str(lastsell)
        if len(lastsell) > 25:
            if price > 2 * numpy.std(lastsell) + numpy.mean(lastsell) or price > 2 * numpy.std(lastsell) + numpy.mean(lastsell):
                #alert!!!!
                sendmail(len(lastsell), lastsell, price)


while True:
    print "time: " + str(x) + " backoff: " + str(fib(backoff))

    x = x + 1

    getbuy()
    getsell()
    time.sleep(fib(backoff))
    backoff = backoff + 1
