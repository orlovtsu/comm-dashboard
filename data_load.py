import yfinance as yf

def fetch_data(commodities, start_date, end_date):
    """
    Fetches historical data for a given list of commodities within a specified date range.

    Args:
        commodities (dict): A dictionary containing the names and ticker symbols of the commodities.
        start_date (datetime): The start date of the data range.
        end_date (datetime): The end date of the data range.

    Returns:
        dict: A dictionary containing the fetched data for each commodity.
    """

    # Create an empty dictionary to store the fetched data
    data_dict = {}

    # Iterate over each commodity in the given dictionary
    for name, ticker in commodities.items():

        # Download the historical data using yfinance library
        data = yf.download(ticker, start=start_date, end=end_date)

        # Reset the index of the DataFrame
        data.reset_index(inplace=True)

        # Store the data in the dictionary using the ticker symbol as the key
        data_dict[ticker] = data

    # Return the dictionary containing the fetched data
    return data_dict