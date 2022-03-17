"""Currency Converter Sytem
To calculate the value of one currency to another
using real-time rates from  https://api.exchangerate-api.com/v4/latest/USD

Base currency: USD    
"""

import urllib.request
import json

def loadRates():
        """
        read the data from the api
        return a dictionary of {currency code: rate}
        """
        exchangeRateApi = "https://api.exchangerate-api.com/v4/latest/USD"

        with urllib.request.urlopen(exchangeRateApi) as f:
            data = f.read()
        jsonData = json.loads(data)

        return dict(jsonData['rates']) 

def currencyCodes():
    """read the data from the api
    return a dictionay of {currency code: currency}
    """
    codesApi = "https://pkgstore.datahub.io/core/currency-codes/codes-all_json/data/029be9faf6547aba93d64384f7444774/codes-all_json.json"

    with urllib.request.urlopen(codesApi) as f:
        data = f.read()
        jsonData = json.loads(data)

    currencyCodes = {country["AlphabeticCode"]:country["Currency"] for country in jsonData}
    return currencyCodes


class CurrencyConverter: 
    def __init__(self):
        self.rates = loadRates()              

    def checkCurrency(self, currency):
        """Check if the currency is in the dictionary of rates
        """
        return currency in self.rates.keys()    

    def convert(self, src_currency, dest_currency, amount):
        if (self.checkCurrency(src_currency) and self.checkCurrency(dest_currency)):        
            # convert the src_currency to USD first if it's not USD (because the base currency is USD)
            if src_currency != "USD":
                amount = amount / self.rates[src_currency] 
            return round(amount * self.rates[dest_currency], 4)
        else:
            raise ValueError("Invalid currency")

    def getRates(self):
        return self.rates

def printHeader(converter):
    print("Welcome to Currency Convert System!")
    print("-"*80)
    print("List of currencies:")    
    for currency in converter.getRates().keys():
        print(currency, end="  ")    
    print()
    print("-"*80)


def main():    
    currencyConverter = CurrencyConverter()
    codes = currencyCodes()

    printHeader(currencyConverter)
    
    while True:        
        option = input("Please enter any key to continue or 'q' to quit > ")
        if option != 'q':
            try:
                print("-"*80)
                src_currency = str.upper(input("FROM currency: "))                
                dest_currency = str.upper(input("TO currency: "))
                amount = float(input("Amount: "))
                result = currencyConverter.convert(src_currency, dest_currency, amount)
            except ValueError as err:
                print(f'ERROR: {err}. Please try again!')
            else:              
                print("-"*80)
                print(f'{amount:,} {src_currency} ({codes[src_currency] if src_currency in codes else ""})\
                     = {result:,} {dest_currency} ({codes[dest_currency] if dest_currency in codes else ""})')
                print("-"*80)
        else:
            break    

if __name__ == "__main__":
    main()    






