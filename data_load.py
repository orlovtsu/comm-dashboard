import yfinance as yf
from datetime import datetime

def fetch_data(commodities, start_date, end_date):

    data_dict = {}
    for name, ticker in commodities.items():
        data = yf.download(ticker, start=start_date, end=end_date)
        data.reset_index(inplace=True)
        data_dict[ticker] = data
        #print(ticker)
    return data_dict