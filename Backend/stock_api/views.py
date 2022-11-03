from rest_framework.response import Response
from rest_framework.decorators import api_view
import mechanicalsoup
from bs4 import BeautifulSoup
import requests

@api_view(['GET'])
def get_stonks(request, stockQuery):
    try:
        ResponseObject = {}
        # print("THIS IS STOCK QUERY", stockQuery)

        browser = mechanicalsoup.StatefulBrowser()
        browser.open("https://finance.yahoo.com/")
        browser.select_form()

        search_term = stockQuery
        browser["yfin-usr-qry"] = search_term
        response = browser.submit_selected()
        new_url = browser.get_url()
        browser.open(str(new_url))
        # print('new url:', browser.get_url())
        # print('my response:', response.text[:500])

        
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
        page = requests.get(new_url, headers=headers).text
        soup = BeautifulSoup(page, 'html.parser')
        price = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'})
        stock_price = price.contents[0]
        

        stock_name_element = soup.find("h1")
        stock_name = stock_name_element.contents[0]

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
        ResponseObject["stock_name"] = stock_name
        ResponseObject["stock_url"] = new_url
        ResponseObject["price"] = stock_price
        try:
            del ResponseObject["Volume"]
        except:
            pass
        return Response(ResponseObject)
    except:
        return Response({"message": "Query not found"})



@api_view(['GET'])
def get_stocks(request, stockTicker):
    upperStockTicker = stockTicker.upper()
    print(upperStockTicker)
    try:
        ResponseObject = {}
        page = requests.get(f'https://finance.yahoo.com/quote/{upperStockTicker}?p={upperStockTicker}&.tsrc=fin-srch')
        # print(page)

        # create object
        soup = BeautifulSoup(page.text, 'html.parser')

        # gets the element that holds the currentMarketPrice value
        stock_element_price = soup.find("fin-streamer", {"data-symbol": {upperStockTicker}, "data-field": "regularMarketPrice"})
        stock_price = stock_element_price.contents[0]
        # print(stock_price)

        # get the stock name
        stock_name_element = soup.find("h1")
        stock_name = stock_name_element.contents[0]

        # get table data for stock

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

