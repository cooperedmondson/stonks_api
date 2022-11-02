from rest_framework.response import Response
from rest_framework.decorators import api_view
import mechanicalsoup
from bs4 import BeautifulSoup

import requests
# @api_view(['GET'])
# def get_stocks(request, stockQuery):
#     print("THIS IS STOCK QUERY", stockQuery)
#     browser = mechanicalsoup.StatefulBrowser()

#     browser.open("https://finance.yahoo.com/")
#     browser.select_form()
#     browser.get_current_form().print_summary()

#     # search_term = input("What would you like to search for?")
#     search_term = stockQuery
#     browser["yfin-usr-qry"] = search_term


#     browser.launch_browser()
#     response = browser.submit_selected()

#     print('new url:', browser.get_url())
#     print('my response:', response.text[:500])


#     #getting the stock page data
#     new_url = browser.get_url()
#     browser.open(new_url)

#     #getting the html
#     page = browser.get_current_page()


@api_view(['GET'])
def get_stocks(request, stockTicker):
    upperStockTicker = stockTicker.upper()
    print(upperStockTicker)
    try:
        ResponseObject = {}
        page = requests.get(f'https://finance.yahoo.com/quote/{upperStockTicker}?p={upperStockTicker}&.tsrc=fin-srch')
        print(page)
        
        #create object
        soup = BeautifulSoup(page.text, 'html.parser')
        
        #gets the element that holds the currentMarketPrice value
        stock_element_price = soup.find("fin-streamer", {"data-symbol":{upperStockTicker}, "data-field": "regularMarketPrice"})
        stock_price = stock_element_price.contents[0]
        print(stock_price)

        #get the stock name
        stock_name_element = soup.find("h1")
        stock_name = stock_name_element.contents[0]
        
        #get table data for stock

        stock_table_element = soup.find("table")
        table_data = stock_table_element.find_all('td')
        
        try:
            for table_row in table_data:
                
                span_element = table_row.find_all('span')
                try:
                    temp_key = span_element[0].contents[0]
                except:
                    ResponseObject[temp_key] = table_row.contents[0]
        except:
            pass
                
        
        

        #building our responseObject
        
        ResponseObject["stock_name"] = stock_name
        ResponseObject["ticker"] = f'${upperStockTicker}'
        ResponseObject["price"] = stock_price
        try:
            del ResponseObject["Volume"]
        except:
            pass
        return Response(ResponseObject)
    except:
        return Response({"message": "Query not found"})

