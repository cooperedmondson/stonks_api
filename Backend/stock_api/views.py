from rest_framework.response import Response
from rest_framework.decorators import api_view
import mechanicalsoup


@api_view(['GET'])
def get_stocks(request, stockQuery):
    print("THIS IS STOCK QUERY", stockQuery)
    browser = mechanicalsoup.StatefulBrowser()

    browser.open("https://finance.yahoo.com/")
    browser.select_form()
    browser.get_current_form().print_summary()

    # search_term = input("What would you like to search for?")
    search_term = stockQuery
    browser["yfin-usr-qry"] = search_term


    browser.launch_browser()
    response = browser.submit_selected()

    print('new url:', browser.get_url())
    print('my response:', response.text[:500])


    #getting the stock page data
    new_url = browser.get_url()
    browser.open(new_url)

    #getting the html
    page = browser.get_current_page()
