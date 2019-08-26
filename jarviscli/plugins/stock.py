import requests
from plugin import plugin
from colorama import Fore
import re


@plugin('stock')
class Stock:

    def __call__(self, jarvis, s):
        if not s:
            self.usage(jarvis)
        else:
            ps = s.split()
            if ps[0] == 'getid':
                ps.pop(0)
                if ps:
                    name = ' '.join(ps)
                else:
                    name = jarvis.input("Enter the name of the stock: ")
                self.get_stock_id(jarvis, name)
            elif ps[0] == 'help':
                self.usage(jarvis)
            elif ps[0] == 'profile':
                if(len(ps) != 2):
                    jarvis.say("You forgot to mention the symbol", Fore.RED)
                else:
                    symbol = ps[1]
                    self.get_profile(jarvis, symbol)
            elif ps[0] == 'fstatement':
                if(len(ps) != 2):
                    jarvis.say("You forgot to mention the symbol", Fore.RED)
                else:
                    symbol = ps[1]
                    self.get_financial_stmt(jarvis, symbol)
            elif ps[0] == 'gainers':
                self.get_gainers(jarvis)
            elif ps[0] == 'losers':
                self.get_losers(jarvis)
            # anything else is treated as a stock symbol
            else:
                self.get_stock_data(jarvis, s)

    def usage(self, jarvis):
        ''' Print the usage for stock command '''
        jarvis.say("stock <stock_id>\t : Get details of stock identified by <stock_id>(one id at a time)", Fore.GREEN)
        jarvis.say("stock getid\t\t : Search stock id", Fore.GREEN)
        jarvis.say("stock profile <stock_id>\t : Get company profile", Fore.GREEN)
        jarvis.say("stock fstatement <stock_id>\t : Get latest ANNUAL finincial statement of the company", Fore.GREEN)
        jarvis.say("stock gainers\t\t : Most gainers in NYSE", Fore.GREEN)
        jarvis.say("stock losers\t\t : Most losers in NYSE", Fore.GREEN)
        jarvis.say("stock help\t\t : Prints help", Fore.GREEN)
        jarvis.say("*** AVAILABLE ONLY FOR US EQUITIES ***", Fore.GREEN)

    def get_stock_data(self, jarvis, quote):
        ''' Given a stock symbol, get the real time price of the stock '''
        url = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/' + quote
        resp = requests.get(url)

        if(resp.status_code == 200):
            data = resp.json()
            if('symbol' in data.keys()):
                jarvis.say("Symbol: " + str(data['symbol']), Fore.GREEN)
                jarvis.say("Price: " + str(data['price']), Fore.GREEN)
            elif('Error' in data.keys()):
                jarvis.say("Invalid stock symbol name", Fore.RED)
            else:
                jarvis.say("Error. Please retry")
        else:
            jarvis.say("Cannot find the name. Try again later\n", Fore.RED)

    def get_stock_id(self, jarvis, name):
        ''' Get the list of stock IDs given a company name or part of the company name '''
        url = 'https://financialmodelingprep.com/api/v3/company/stock/list'
        resp = requests.get(url)

        if(resp.status_code == 200):
            data = resp.json()
            found = False

            # Add try block. Somtimes the endpoint does not work or has unexcepted behaviour
            try:
                for stock in data['symbolsList']:
                    if(re.match(name.lower(), stock['name'].lower())):
                        found = True
                        jarvis.say(stock['symbol'] + "\t\t" + stock['name'], Fore.GREEN)

                if not found:
                    jarvis.say("The given name could not be found\n", Fore.RED)
            except KeyError:
                jarvis.say("The endpoint is not working at the moment. Try again later", Fore.RED)
        else:
            jarvis.say("Cannot find the name at this time. Try again later\n", Fore.RED)

    def get_profile(self, jarvis, symbol):
        ''' Given a stock symbol get the company profile '''
        url = 'https://financialmodelingprep.com/api/v3/company/profile/' + symbol
        resp = requests.get(url)

        if(resp.status_code == 200):
            data = resp.json()
            if(not data):
                jarvis.say("Cannot find details for " + symbol, Fore.RED)
            else:
                jarvis.say(" Symbol      : " + data['symbol'], Fore.GREEN)
                jarvis.say(" Company     : " + data['profile']['companyName'], Fore.GREEN)
                jarvis.say(" Industry    : " + data['profile']['industry'], Fore.GREEN)
                jarvis.say(" Sector      : " + data['profile']['sector'], Fore.GREEN)
                jarvis.say(" Website     : " + data['profile']['website'], Fore.GREEN)
                jarvis.say(" Exchange    : " + data['profile']['exchange'], Fore.GREEN)
                jarvis.say(" Description : " + data['profile']['description'], Fore.GREEN)

        else:
            jarvis.say("Cannot find details for " + symbol, Fore.RED)

    def get_financial_stmt(self, jarvis, symbol):
        ''' Get the last annual financial statement of a company given it's stock symbol '''
        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/' + symbol
        resp = requests.get(url)

        if(resp.status_code == 200):
            data = resp.json()
            if(not data):
                jarvis.say("Cannot find details for: " + symbol, Fore.RED)
            else:
                for key in data['financials'][0].keys():
                    jarvis.say(key + " => " + data['financials'][0][key], Fore.GREEN)
        else:
            jarvis.say("Cannot find details for " + symbol, Fore.RED)

    def get_gainers(self, jarvis):
        ''' Get the most gainers of the day '''
        url = 'https://financialmodelingprep.com/api/v3/stock/gainers'
        resp = requests.get(url)

        if(resp.status_code == 200):
            data = resp.json()
            if(not data):
                jarvis.say("Cannot find details at this moment.", Fore.RED)
            else:
                for gainer in data['mostGainerStock']:
                    jarvis.say("Ticker: " + gainer['ticker'] + " | Company: " + gainer['companyName'] + " | Price: " + str(gainer['price']) + " | Change: " + str(gainer['changes']) + " | Change %: " + str(gainer['changesPercentage']), Fore.GREEN)
        else:
            jarvis.say("Cannot get gainers list at the moment")

    def get_losers(self, jarvis):
        ''' Get the most losers of the day '''
        url = 'https://financialmodelingprep.com/api/v3/stock/losers'
        resp = requests.get(url)

        if(resp.status_code == 200):
            data = resp.json()
            if(not data):
                jarvis.say("Cannot find details at the moment.", Fore.RED)
            else:
                for loser in data['mostLoserStock']:
                    jarvis.say("Ticker: " + loser['ticker'] + " | Company: " + loser['companyName'] + " | Price: " + str(loser['price']) + " | Change: " + str(loser['changes']) + " | Change %: " + str(loser['changesPercentage']), Fore.GREEN)
        else:
            jarvis.say("Cannot get losers list at the moment")
