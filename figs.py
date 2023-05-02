import plotly.graph_objects as go
import pandas as pd

def plot1(df, ticker_name):
    """
    Create a candlestick chart for a given DataFrame containing stock price data.

    Args:
        df (pd.DataFrame): DataFrame containing the stock price data.
        ticker_name (str): Name of the ticker or stock.

    Returns:
        go.Figure: Figure object containing the candlestick chart.
    """

    # Create the Candlestick trace using the DataFrame columns
    Candlestick = go.Candlestick(x=df['Date'],
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Candlestick')

    # Create the figure with the Candlestick trace
    fig = go.Figure(data=[Candlestick])

    # Update the layout properties
    fig.update_layout(
        title=f'Price: {ticker_name}',
        xaxis_title='Date',
        xaxis=dict(
            type='date',
            tickfont=dict(size=10),
            nticks=10),
        yaxis=dict(
            title='Price',
            tickfont=dict(size=10)
        ),
        title_x=0.5,
        showlegend=False
    )

    # Return the figure
    return fig

def plot2(df, ticker_name):
    """
    Create a bar chart for the volume of a given DataFrame containing stock data.

    Args:
        df (pd.DataFrame): DataFrame containing the stock data.
        ticker_name (str): Name of the ticker or stock.

    Returns:
        go.Figure: Figure object containing the bar chart.
    """

    # Create the volume trace (bar chart) using the DataFrame columns
    volume = go.Bar(x=df['Date'],
                    y=df['Volume'],
                    yaxis='y2',  # Use the secondary y-axis for volume
                    name='Volume',
                    marker=dict(color='rgba(0, 0, 255, 1)'))  # Set the color and opacity

    # Create the figure with the volume trace
    fig = go.Figure(data=[volume])

    # Update the layout properties of the figure
    fig.update_layout(
        title=f'Volume: {ticker_name}',
        xaxis_title='Date',
        xaxis=dict(
            type='date',
            tickfont=dict(size=10),
            nticks=10),
        yaxis=dict(
            title='Volume',
            tickfont=dict(size=10)
        ),
        title_x=0.5,

        showlegend=False
    )

    # Return the figure
    return fig

def plot3(df, commodities, start_date, end_date):
    """
    Create a correlation heatmap for a given DataFrame containing stock price data.

    Args:
        df (pd.DataFrame): DataFrame containing the stock price data for multiple commodities.
        commodities (dict): Dictionary containing the names and ticker symbols of the commodities.
        start_date (datetime): The start date of the data range.
        end_date (datetime): The end date of the data range.

    Returns:
        go.Figure: Figure object containing the correlation heatmap.
    """

    # Create an empty DataFrame to store the close prices of the commodities
    close_prices = pd.DataFrame()

    # Iterate over each commodity in the given dictionary
    for name, ticker in commodities.items():
        data = df[ticker]
        close_prices[name] = data['Close']

    # Calculate the correlation matrix of the close prices
    correlation_matrix = close_prices.corr()

    # Create the heatmap using the correlation matrix
    heatmap = go.Heatmap(z=correlation_matrix,
                         x=correlation_matrix.columns,
                         y=correlation_matrix.index,
                         colorscale='Plasma',  # Choose a colorscale
                         zmin=-1, zmax=1)  # Set the color range to [-1, 1]

    # Create the figure with the heatmap trace
    fig = go.Figure(data=heatmap)

    # Update the layout properties of the figure
    fig.update_layout(
        title=f'Correlation Heatmap of Commodities using data from <br>{start_date} to {end_date}',
        xaxis_title='Commodity',
        yaxis_title='Commodity',
        title_x=0.5,
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        showlegend=False
    )

    # Return the figure
    return fig